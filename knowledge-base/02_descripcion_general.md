# Descripción General

## Resumen

`turnos-odontologia` es una **API/backend puro** (sin UI obligatoria) para la gestión de turnos de un **único consultorio odontológico** (mono-tenant), pensada para la realidad PyME argentina. Expone las reglas de dominio del agendamiento con recurso doble (profesional + sillón), duración por prestación y prevención de solapamientos, con una arquitectura en capas/hexagonal y tests automatizados estrictos.

> **Decisión de tipo de sistema (P0-sys):** API/backend puro. La consigna de la cátedra aclara que la implementación es **a nivel de lógica de dominio + API, con tests automatizados**. No se exige ni se incluye una interfaz gráfica propia.

## Stack tecnológico

| Capa | Tecnología | Versión objetivo | Notas |
|---|---|---|---|
| Lenguaje | Python | 3.12+ | Dominio puro, tipos explícitos |
| API REST | FastAPI + Pydantic | A fijar al implementar | Validación en la frontera; sin dependencias de framework en el dominio |
| Persistencia | SQLAlchemy + PostgreSQL | PostgreSQL 15+; SQLAlchemy a fijar | Modelos ORM y mappers en infraestructura; constraint de exclusión |
| Migraciones | Alembic | A fijar al implementar | Revisiones en `alembic/versions/` |
| Testing | pytest | A fijar al implementar | Unitarios con fakes; integración y concurrencia con PostgreSQL real |
| Dependencias | venv + pip + pyproject.toml | Según entorno Python | Versiones reproducibles a registrar al implementar |
| Autenticación | JWT | Planificada en C-14 | RBAC en C-15; no incorporado por este ajuste |
| Caché / trabajos | Redis | Cuando corresponda | No sustituye el constraint de PostgreSQL ni es requisito de los tests unitarios |
| Contenedores | Docker + Compose | Según entorno | App y PostgreSQL locales; Redis sólo si un change lo necesita |

Estas son decisiones de documentación, no una declaración de dependencias instaladas. React/TypeScript/Vite queda como contexto de un futuro cliente, fuera del change backend.

## Arquitectura general

```
            ┌──────────────────────────────────────────────────────────┐
            │                       API REST                            │
            │   (controllers + DTOs + validación de entrada)            │
            └───────────────────────────┬──────────────────────────────┘
                                        │
            ┌───────────────────────────▼──────────────────────────────┐
            │                   CAPA DE APLICACIÓN                      │
            │   casos de uso / servicios de aplicación, transacciones   │
            │   orquestan dominio + puertos (repositorios)             │
            └───────────────────────────┬──────────────────────────────┘
                                        │
            ┌───────────────────────────▼──────────────────────────────┐
            │                     DOMINIO (núcleo)                      │
            │   Turno, Profesional, Sillon, Prestacion, Recordatorio     │
            │   reglas RN-XX, cálculo de duración, anti-solapamiento    │
            │   SIN dependencias de framework                           │
            └───────────────────────────┬──────────────────────────────┘
                                        │  puertos
            ┌───────────────────────────▼──────────────────────────────┐
            │                  INFRAESTRUCTURA                          │
            │   SQLAlchemy/PostgreSQL, mappers, adaptadores WhatsApp/MercadoPago│
            │   Google Calendar, scheduler de recordatorios             │
            └──────────────────────────────────────────────────────────┘
```

El proyecto sigue una **arquitectura en capas o hexagonal limpia**: el dominio no conoce el framework ni la base de datos; la aplicación orquesta casos de uso transaccionales; la infraestructura implementa los puertos. Ver detalle en [`08_arquitectura_propuesta.md`](08_arquitectura_propuesta.md).

## Naturaleza mono-tenant y backend puro

- **Mono-tenant (single-tenant):** el sistema atiende a **un solo consultorio / equipo chico (<50 personas)**. Es una decisión explícita para concentrar el esfuerzo en la prevención de solapamientos y en la corrección de las reglas de dominio. **No se introduce multi-tenancy** ni aislamiento por organización, ni multi-sucursal en la v1.
- **Backend puro:** la entrega es una API REST + lógica de dominio con tests automatizados. No existe aplicación web, móvil ni panel de administración dentro del alcance. Cualquier cliente (portal de pacientes, mostrador) se asume como consumidor externo de la API.

> **Suposición:** al no incluir UI, se asume que la interfaz es responsabilidad de un cliente externo (o del propio frontend de la cátedra) que consume estos endpoints. La KB documenta la API y el dominio, no una interfaz gráfica.

## Integraciones externas

| Servicio | Propósito | Tipo | Estado en MVP |
|---|---|---|---|
| WhatsApp Business API | Recordatorios automáticos y confirmación de turnos | REST + webhook (entrante) | Núcleo del MVP (recordatorios) |
| Mercado Pago | Cobro de señas para reducir ausentismo | REST + webhook de pago | Planificado / depende de política de seña |
| Google Calendar | Sincronización de la agenda del profesional | REST (OAuth 2.0) | Post-estabilización del flujo de turnos |

El orden de valor de las integraciones es WhatsApp → Google Calendar → Mercado Pago (ver `09`).

## API REST (resumen)

Los endpoints se agrupan por recurso. Detalle de rutas públicas vs. autenticadas en [`03_actores_y_roles.md`](03_actores_y_roles.md).

| Recurso | Ejemplo de endpoints |
|---|---|
| Autenticación | `POST /api/auth/login`, `POST /api/auth/refresh` |
| Pacientes | `GET/POST /api/pacientes`, `GET /api/pacientes/{id}` |
| Profesionales | `GET/POST /api/profesionales`, `GET /api/profesionales/{id}/agenda` |
| Sillones | `GET/POST /api/sillones`, `GET /api/sillones/{id}/agenda` |
| Prestaciones | `GET/POST /api/prestaciones` |
| Turnos | `GET /api/turnos`, `POST /api/turnos`, `POST /api/turnos/{id}/cancelar`, `POST /api/turnos/{id}/reprogramar` |
| Disponibilidad | `GET /api/disponibilidad?prestacionId=&fecha=` |
| Recordatorios | `GET /api/turnos/{id}/recordatorio` |

> Las rutas exactas y los permisos por rol están especificados en `03`. No deben inventarse endpoints fuera de este conjunto sin registrarlos en `10_preguntas_abiertas.md`.

## Referencias

- Actores y RBAC: [`03_actores_y_roles.md`](03_actores_y_roles.md)
- Arquitectura detallada: [`08_arquitectura_propuesta.md`](08_arquitectura_propuesta.md)
- Decisiones y supuestos: [`09_decisiones_y_supuestos.md`](09_decisiones_y_supuestos.md)
