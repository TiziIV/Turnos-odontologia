# Arquitectura Propuesta

## Patrones aplicados

| Patrón | Dónde se usa | Por qué |
|---|---|---|
| Arquitectura en capas / **hexagonal** | Separación dominio / aplicación / infraestructura | Aísla las reglas `RN-NN` del framework y de la base, habilitando tests unitarios puros de dominio |
| Puertos y adaptadores | Repositorios y clientes externos como interfaces | Permite sustituir PostgreSQL por H2 en tests y mockear WhatsApp/MercadoPago |
| Transacción por caso de uso | Creación/cancelación/reprogramación de turnos | Garantiza atomicidad del recurso doble |
| Locking optimista + pesimista | Entidad `Turno` (`@Version`) y bloqueo de franja de recursos | Resuelve el agendamiento concurrente |
| Constraint de exclusión (DB) | PostgreSQL, sobre `profesional` y `sillon` con `tsrange` | Garantía anti-solapamiento a nivel base, no sólo aplicación |
| Scheduler | Job de recordatorios | Dispara los envíos de WhatsApp |
| DTO + Mapper | Frontera API ↔ dominio | Evita exponer el modelo de dominio y desacopla contratos |

Se optó por una **arquitectura hexagonal limpia** (equivalente a capas con dominio aislado): el paquete `domain` no importa Spring ni JPA.

## Estructura de directorios

```
turnos-odontologia/
├── pom.xml                         # (o build.gradle) — módulo raíz
├── docker-compose.yml              # PostgreSQL + la app (contenedor liviano)
├── src/
│   ├── main/
│   │   ├── java/ar/edu/consultorio/turnos/
│   │   │   ├── domain/                     # núcleo: sin framework
│   │   │   │   ├── model/                   # Turno, Profesional, Sillon, Prestacion, Paciente, Recordatorio
│   │   │   │   ├── rule/                    # reglas RN-NN (duración, solapamiento, transiciones)
│   │   │   │   ├── exception/               # errores de dominio
│   │   │   │   └── port/                    # interfaces de repositorio y servicios externos
│   │   │   ├── application/                 # casos de uso / orquestación
│   │   │   │   ├── service/                 # AgendaService, TurnoService, RecordatorioService
│   │   │   │   └── dto/                      # comandos y resultados de aplicación
│   │   │   ├── infrastructure/              # adaptadores
│   │   │   │   ├── persistence/             # entidades JPA, repositorios, mappers
│   │   │   │   ├── whatsapp/                # adaptador WhatsApp Business API
│   │   │   │   ├── mercadopago/             # adaptador Mercado Pago
│   │   │   │   ├── calendar/                # adaptador Google Calendar
│   │   │   │   └── scheduler/               # job de recordatorios
│   │   │   └── api/                         # controllers REST + DTOs + seguridad
│   │   │       ├── controller/
│   │   │       ├── dto/
│   │   │       └── security/                # filtros JWT, RBAC
│   │   └── resources/
│   │       ├── application.yml              # config base
│   │       ├── application-prod.yml         # PostgreSQL
│   │       ├── application-test.yml         # H2 en memoria
│   │       └── db/migration/                # Flyway/Liquibase (constraint de exclusión)
│   └── test/
│       └── java/ar/edu/consultorio/turnos/
│           ├── domain/                      # tests unitarios de reglas RN-NN
│           ├── application/                 # tests de casos de uso
│           ├── integration/                 # tests con H2
│           └── concurrency/                 # tests de doble reserva
```

## Módulos (Maven/Gradle)

Para un TP académico, se proponen dos alternativas:

- **Opción simple (recomendada):** un solo módulo con paquetes por capa (estructura de arriba). Menor fricción de build, suficiente para la consigna.
- **Opción modular:** módulos `domain`, `application`, `infrastructure`, `api` como módulos Maven/Gradle separados, con `domain` sin dependencias de Spring. Refuerza la separación a nivel compilación y evidencia la arquitectura hexagonal.

> **Suposición:** la cátedra no exige multi-módulo. Se documenta la opción modular como camino opcional; la implementación base usa paquetes por capa.

## Manejo de concurrencia

El riesgo principal del Discovery es el **agendamiento concurrente** (online vs. mostrador). Se ataca en tres niveles:

1. **Nivel aplicación — locking pesimista:** al confirmar un turno, se bloquean la franja del `Profesional` y la del `Sillon` dentro de la transacción (`SELECT ... FOR UPDATE` sobre un lock lógico por recurso, o bloqueo adoptivo sobre clave `(recursoId, fecha)`).
2. **Nivel aplicación — locking optimista:** la entidad `Turno` lleva `@Version`; los updates concurrentes sobre el mismo turno (p. ej. dos reprogramaciones) fallan con `OptimisticLockException` y se traducen a un error de dominio controlado.
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

> **Nota:** H2 no soporta `EXCLUDE USING gist`. Por eso el anti-solapamiento en tests se respalda con el locking de aplicación, y el constraint de exclusión se prueba en un perfil de integración con PostgreSQL/Testcontainers (ver estrategia de tests).

## Estrategia de tests

| Tipo | Herramienta | Cobertura |
|---|---|---|
| Unitarios de dominio | JUnit 5 + AssertJ (sin Spring) | Cada regla `RN-NN`: duración (RN-02), solapamiento y **fin == inicio** (RN-03), estados/transiciones (RN-07/RN-08), liberación de cupo (RN-04) |
| Casos de uso | JUnit 5 + Mockito | Orquestación transaccional, cancelación, reprogramación atómica (RN-15) |
| Integración persistencia | `@DataJpaTest` + **H2 en memoria** | Repositorios, mappers, derivación de `fin`, estados activos |
| Concurrencia | JUnit 5 + hilos/`ExecutorService` | Doble reserva simultánea → una gana, otra rechazo controlado (RN-16) |
| Constraint de exclusión | Testcontainers PostgreSQL | `EXCLUDE USING gist` bloquea solapamiento a nivel DB (RN-01/RN-03) |

Convención: **todo `RN-NN` tiene al menos un test que lo nombra** (trazabilidad regla → test).

## Seguridad

- **Autenticación:** JWT sin estado (stateless), firmado; `sub` + `rol` en claims.
- **Autorización:** RBAC a nivel de endpoint (filtros de seguridad) + verificación de propiedad en el dominio (paciente sólo accede a lo propio).
- **Validación de input:** Bean Validation en DTOs de frontera; invariantes también en el dominio (defensa en profundidad).
- **Secrets management:** credenciales de DB, WhatsApp, MercadoPago y Google Calendar por **variables de entorno**; nunca en el repositorio ni en `application.yml` versionado.
- **Ley 25.326:** datos personales mínimos; prohibido almacenar datos sensibles reales en repos/seeds/tests (RN-LG). Hashing de contraseñas; logs sin datos personales.

## Variables de entorno

| Variable | Descripción | Ejemplo | Sensible |
|---|---|---|---|
| `SPRING_DATASOURCE_URL` | URL de PostgreSQL | `jdbc:postgresql://localhost:5432/turnos` | N |
| `SPRING_DATASOURCE_USERNAME` | Usuario DB | `turnos` | N |
| `SPRING_DATASOURCE_PASSWORD` | Password DB | `********` | **S** |
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

Ejecución **local** (Maven/Gradle) o **contenedor Docker liviano** con `docker-compose.yml` (app + PostgreSQL). Sin infraestructura cloud compleja, según la restricción del stack.

## Referencias

- Modelo de datos y constraint: [`04_modelo_de_datos.md`](04_modelo_de_datos.md)
- Reglas: [`05_reglas_de_negocio.md`](05_reglas_de_negocio.md)
- Decisiones: [`09_decisiones_y_supuestos.md`](09_decisiones_y_supuestos.md)
