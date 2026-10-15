# Actores y Roles

## Actores del sistema

| Actor | Descripción | Cómo interactúa |
|---|---|---|
| Paciente | Persona que recibe la atención odontológica | Vía API (portal/cliente externo): reserva online 24/7, cancela, confirma por WhatsApp |
| Odontólogo (general o especialista) | Profesional que atiende y ocupa un sillón | Consulta su agenda; es uno de los dos recursos del turno |
| Recepcionista / Secretaria | Personal de mostrador del consultorio | Agenda en mostrador, gestiona cupos y reprograma sobre la misma fuente de disponibilidad |
| Administrador del consultorio | Rol de configuración del catálogo del dominio | Crea/edita prestaciones (con duración), sillones/boxes y profesionales |

> **Suposición:** el rol **Administrador del consultorio** se agrega para cubrir la configuración de prestaciones, sillones y profesionales. No viene explícito en el Discovery. Si en la cátedra la recepcionista concentra también la administración, ambos roles pueden unificarse (ver [`10_preguntas_abiertas.md`](10_preguntas_abiertas.md)).

## RBAC — Matriz de permisos

Permisos por convención CRUD (C=crear, R=leer, U=actualizar, D=borrar). El borrado lógico es preferido sobre el físico para entidades referenciadas por turnos.

| Rol \ Recurso | Turno | Disponibilidad | Paciente | Prestación | Sillón | Profesional | Recordatorio | Usuario |
|---|---|---|---|---|---|---|---|---|
| Paciente | C (propios), R (propios), U (cancelar/reprogramar propios) | R | R (propio) | R | — | R | R (propio) | — |
| Odontólogo | R (de su agenda) | R | R | R | R | R (propio) | R (de su turno) | — |
| Recepcionista | C, R, U (cancelar/reprogramar) | R | C, R, U | R | R | R | R | — |
| Administrador | C, R, U | R | R | C, R, U, D | C, R, U, D | C, R, U, D | R | C, R, U |

Notas:

- El **paciente** sólo opera sobre sus propios turnos y datos; nunca sobre los de otro paciente (filtro por identidad).
- El **odontólogo** tiene lectura de agenda y no modifica el catálogo.
- La **recepcionista** es el rol operativo de escritura sobre turnos; no administra el catálogo.
- El **administrador** administra el catálogo y los usuarios; puede también operar sobre turnos.
- Ningún rol accede a datos clínicos sensibles (fuera del alcance MVP; ver RN-LG en [`05_reglas_de_negocio.md`](05_reglas_de_negocio.md)).

## Rutas públicas

Accesibles **sin autenticación**:

| Ruta | Método | Motivo |
|---|---|---|
| `/api/auth/login` | POST | Emisión de credenciales |
| `/api/auth/refresh` | POST | Renovación de token |
| `/api/public/disponibilidad` | GET | Consulta de disponibilidad para reserva online 24/7 |
| `/api/public/turnos` | POST | Creación de turno por paciente no autenticado (reserva invitado) |
| `/api/webhooks/whatsapp` | POST | Recepción de mensajes/confirmaciones de WhatsApp |
| `/api/webhooks/mercadopago` | POST | Notificación de pago de seña |

> **Suposición:** la **reserva de invitado** (paciente sin cuenta) se expone como pública: el caso de uso "reservar online 24/7 sin llamar" no exige registro previo. La validación de identidad del paciente en ese flujo se registra como pregunta abierta en `10`.

## Rutas autenticadas (por rol)

| Ruta | Métodos | Roles habilitados |
|---|---|---|
| `/api/turnos` | GET, POST | Recepcionista, Administrador (POST/R); Paciente (propios), Odontólogo (propios, R) |
| `/api/turnos/{id}/cancelar` | POST | Paciente (propio), Recepcionista, Administrador |
| `/api/turnos/{id}/reprogramar` | POST | Paciente (propio), Recepcionista, Administrador |
| `/api/profesionales/**` | GET/POST/PUT/DELETE | GET: todos los roles; escritura: Administrador |
| `/api/sillones/**` | GET/POST/PUT/DELETE | GET: Odontólogo, Recepcionista, Administrador; escritura: Administrador |
| `/api/prestaciones/**` | GET/POST/PUT/DELETE | GET: todos; escritura: Administrador |
| `/api/pacientes/**` | GET/POST/PUT | Recepcionista, Administrador; Paciente (propio, R) |
| `/api/usuarios/**` | C/R/U | Administrador |

## Modelo de autenticación (alto nivel)

- **Esquema:** autenticación por token (JWT) con roles embebidos; sin estado de sesión en servidor.
- **Autorización:** por rol (RBAC) a nivel de endpoint y por propiedad del recurso en el dominio (un paciente sólo ve sus turnos).
- Los webhooks se validan por **firma/secret** del proveedor, no por token de usuario.

> Detalle de implementación de seguridad en [`08_arquitectura_propuesta.md`](08_arquitectura_propuesta.md).

## Referencias

- Reglas de negocio asociadas a permisos: [`05_reglas_de_negocio.md`](05_reglas_de_negocio.md)
- Flujo de autenticación: [`07_flujos_principales.md`](07_flujos_principales.md)
