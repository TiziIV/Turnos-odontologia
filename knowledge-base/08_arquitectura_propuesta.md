# Arquitectura Propuesta

## Patrones aplicados

| Patrón | Dónde se usa | Por qué |
|---|---|---|
| Arquitectura en capas / **hexagonal** | Separación dominio / aplicación / infraestructura | Aísla las reglas `RN-NN` del framework y de la base, habilitando tests unitarios puros de dominio |
| Puertos y adaptadores | Repositorios y clientes externos como interfaces | Permite fakes para tests unitarios y adaptadores externos; la integración de persistencia requiere PostgreSQL |
| Transacción por caso de uso | Creación/cancelación/reprogramación de turnos | Garantiza atomicidad del recurso doble |
| Locking optimista + pesimista | Adaptador SQLAlchemy de `Turno` (columna de versión) y bloqueo de franja de recursos | Resuelve el agendamiento concurrente |
| Constraint de exclusión (DB) | PostgreSQL, sobre `profesional` y `sillon` con `tsrange` | Garantía anti-solapamiento a nivel base, no sólo aplicación |
| Scheduler | Job de recordatorios | Dispara los envíos de WhatsApp |
| DTO + Mapper | Frontera API ↔ dominio | Evita exponer el modelo de dominio y desacopla contratos |

Se optó por una **arquitectura hexagonal limpia** (equivalente a capas con dominio aislado): el paquete `domain` no importa FastAPI, Pydantic ni SQLAlchemy.

## Estructura de directorios

```text
turnos-odontologia/
├── pyproject.toml                   # metadatos, dependencias y pytest
├── docker-compose.yml              # app + PostgreSQL; Redis cuando corresponda
├── .env.example                    # nombres de variables, sin credenciales reales
├── alembic/versions/                # migraciones SQLAlchemy/Alembic
├── src/turnos/
│   ├── domain/                     # núcleo Python puro, sin framework
│   │   ├── model/                  # entidades, dataclasses, enums
│   │   ├── rule/                   # reglas RN-NN
│   │   ├── exception/              # errores de dominio
│   │   └── port/                   # contratos de repositorios/servicios
│   ├── application/
│   │   ├── service/                # casos de uso; unidad de trabajo por puerto
│   │   └── dto/                    # comandos/resultados puros
│   ├── infrastructure/
│   │   ├── persistence/            # SQLAlchemy, repositorios y mappers
│   │   ├── whatsapp/               # adaptador futuro
│   │   ├── mercadopago/            # adaptador futuro
│   │   ├── calendar/               # adaptador futuro
│   │   └── scheduler/              # recordatorios
│   └── api/                       # FastAPI, composición de dependencias
│       ├── controller/             # routers REST
│       ├── dto/                    # modelos Pydantic de entrada/salida
│       └── security/               # JWT/RBAC (changes posteriores)
└── tests/
    ├── domain/                    # pytest puro
    ├── application/               # pytest + fakes
    ├── integration/               # pytest + PostgreSQL real
    └── concurrency/               # transacciones simultáneas en PostgreSQL
```

## Paquetes Python

Un solo proyecto Python con paquetes por capa. El dominio usa tipos estándar de Python y contratos de puertos; la API valida con Pydantic y la infraestructura traduce modelos SQLAlchemy. Las dependencias apuntan hacia adentro (`api → application → domain`, `infrastructure → domain`). La composición de adaptadores vive en el arranque de la API. Esta estructura es propuesta para implementar, no archivos ya existentes.

## Manejo de concurrencia

El riesgo principal del Discovery es el **agendamiento concurrente** (online vs. mostrador). Se ataca en tres niveles:

1. **Nivel aplicación — locking pesimista:** al confirmar un turno, se bloquean la franja del `Profesional` y la del `Sillon` dentro de la transacción (`SELECT ... FOR UPDATE` sobre un lock lógico por recurso, o bloqueo adoptivo sobre clave `(recursoId, fecha)`).
2. **Nivel aplicación — locking optimista:** el adaptador SQLAlchemy de `Turno` usa una columna de versión (`version_id_col`); los updates concurrentes sobre el mismo turno (p. ej. dos reprogramaciones) se detectan como `StaleDataError` y se traducen a un error de dominio controlado.
3. **Nivel base de datos — constraint de exclusión (PostgreSQL):** garantía dura contra el solapamiento, independiente de la aplicación:

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE turno
  ADD CONSTRAINT no_solape_profesional
  EXCLUDE USING gist (
    profesional_id WITH =,
    tsrange(inicio, fin, '[)') WITH &&
  ) WHERE (estado IN ('PENDIENTE','CONFIRMADO'));

ALTER TABLE turno
  ADD CONSTRAINT no_solape_sillon
  EXCLUDE USING gist (
    sillon_id WITH =,
    tsrange(inicio, fin, '[)') WITH &&
  ) WHERE (estado IN ('PENDIENTE','CONFIRMADO'));
```

El rango `[inicio, fin)` es **semiabierto**: permite encadenar exacto (fin de uno = inicio del siguiente) y bloquea el solapamiento estricto (RN-03). El `WHERE` con estados activos implementa RN-09 (los cancelados/libres no ocupan). Al recibir la violación del constraint (`23P01 exclusion_violation`), la API la traduce a `409 Conflict`.

> **Límite de verificación:** los tests unitarios con fakes prueban reglas secuenciales de dominio. No prueban transacciones, locking, constraints ni concurrencia de PostgreSQL. RN-16 y los constraints requieren tests separados sobre PostgreSQL real, por ejemplo con Docker Compose o Testcontainers para Python. No sustituirlos por SQLite ni por un repositorio en memoria. La política de zona horaria debe acordarse antes de la migración: `tsrange` requiere timestamps sin zona; si se usan timestamps con zona corresponde `tstzrange`. El ajuste de stack no decide esa política.

## Estrategia de tests

| Tipo | Herramienta | Cobertura |
|---|---|---|
| Unitarios de dominio | pytest sin FastAPI/ORM | Cada regla RN-NN: duración, solapamiento y fin == inicio, estados, liberación de cupo |
| Casos de uso | pytest + repositorios fake | Orquestación y contratos de puertos; no garantiza atomicidad real de la DB |
| API | pytest + cliente de prueba FastAPI | Validación Pydantic, contrato HTTP y traducción de errores |
| Integración persistencia | pytest + SQLAlchemy + PostgreSQL real | Repositorios, mappers, migraciones y estados activos |
| Concurrencia y constraints | pytest + transacciones simultáneas en PostgreSQL real | Una reserva gana y la otra se rechaza controladamente (RN-16); exclusión por ambos recursos |

Comando objetivo: `python -m pytest`. La implementación debe documentar instalación, configuración y comandos independientes para las pruebas con PostgreSQL en el README. No presentar integración pendiente como tests unitarios aprobados.

Convención: **todo `RN-NN` tiene al menos un test que lo nombra** (trazabilidad regla → test).

## Seguridad

- **Autenticación:** JWT sin estado (stateless), firmado; `sub` + `rol` en claims.
- **Autorización:** RBAC a nivel de endpoint (filtros de seguridad) + verificación de propiedad en el dominio (paciente sólo accede a lo propio).
- **Validación de input:** Pydantic en DTOs de frontera; invariantes también en el dominio (defensa en profundidad).
- **Secrets management:** credenciales de DB, WhatsApp, MercadoPago y Google Calendar por **variables de entorno**; nunca en el repositorio ni en archivos de configuración versionados.
- **Ley 25.326:** datos personales mínimos; prohibido almacenar datos sensibles reales en repos/seeds/tests (RN-LG). Hashing de contraseñas; logs sin datos personales.

## Variables de entorno

| Variable | Descripción | Ejemplo | Sensible |
|---|---|---|---|
| `DATABASE_URL` | URL SQLAlchemy de PostgreSQL; puede contener credenciales | `postgresql+psycopg://usuario:clave@localhost:5432/turnos` (sintético) | **S** |
| `REDIS_URL` | Conexión opcional para caché/trabajos | `redis://localhost:6379/0` | Según credenciales |
| `APP_RECORDATORIO_ANTICIPACION_MIN` | Anticipación del recordatorio | `1440` | N |
| `APP_AGENDA_APERTURA` | Hora de apertura | `08:00` | N |
| `APP_AGENDA_CIERRE` | Hora de cierre | `20:00` | N |
| `APP_TOLERANCIA_MIN` | Tolerancia de agendamiento (RN-14) | `0` | N |
| `WHATSAPP_API_TOKEN` | Token de WhatsApp Business API | `********` | **S** |
| `WHATSAPP_PHONE_ID` | ID del número de negocio | `123456` | N |
| `MERCADOPAGO_ACCESS_TOKEN` | Token de Mercado Pago | `********` | **S** |
| `GOOGLE_CALENDAR_CREDENTIALS` | JSON de credenciales OAuth | `********` | **S** |
| `JWT_SECRET` | Clave de firma del token | `********` | **S** |

> Los valores concretos de anticipación, franja y tolerancia son configurables; sus defaults se registran como pregunta abierta en [`10_preguntas_abiertas.md`](10_preguntas_abiertas.md).

## Despliegue

Ejecución **local** (entorno virtual Python, FastAPI mediante un servidor ASGI) o **contenedor Docker liviano** con `docker-compose.yml` (app + PostgreSQL). Sin infraestructura cloud compleja, según la restricción del stack.

## Referencias

- Modelo de datos y constraint: [`04_modelo_de_datos.md`](04_modelo_de_datos.md)
- Reglas: [`05_reglas_de_negocio.md`](05_reglas_de_negocio.md)
- Decisiones: [`09_decisiones_y_supuestos.md`](09_decisiones_y_supuestos.md)
