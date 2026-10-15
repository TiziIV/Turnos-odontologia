# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto **turnos-odontologia**.
> Cada change es atómico: un agente puede implementarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de ejecutar cualquier `/opsx:propose`.**

> **Ancla del MVP:** `C-06 crear-turno-anti-solapamiento` es el **change prioritario**. Es el primer change funcional del núcleo de agenda y el corazón del sistema: un turno que exige simultáneamente un `Profesional` libre **y** un `Sillon/box` libre en la franja, con duración derivada de la prestación y anti-solapamiento estricto (`fin == inicio` permitido). Los changes `C-01` y `C-02` son cimientos obligatorios y `C-03`/`C-04`/`C-05` **+ `C-05b`** (alta mínima de pacientes) sus prerequisitos directos de catálogo.

---

## Cómo usar este documento

1. Identificar el change a implementar (verificar que sus dependencias están en `openspec/changes/archive/`).
2. Leer los docs de la knowledge-base indicados en "Leer antes".
3. Ejecutar `/opsx:propose <nombre-del-change>`.
4. Al terminar el change, archivarlo con `/opsx:archive <nombre-del-change>`.
5. Marcar el checkbox `[x]` en este archivo.

---

## Árbol de dependencias

```
C-01 foundation-setup
  └── C-02 dominio-core-models
        │
        ├── C-03 gestionar-prestaciones ─────┐
        ├── C-04 gestionar-profesionales ────┼── C-06 crear-turno-anti-solapamiento ★ (PRIORITARIO)
        ├── C-05 gestionar-sillones ─────────┤          │
        └── C-05b gestionar-pacientes-basico ┘          │
        │                                               │
        │        ┌──────────────────────────────────────┼───────────────────────────────┐
        │        │                                      │                               │
        │        ▼                                      ▼                               ▼
        │  C-07 programar-recordatorio     C-08 consultar-disponibilidad     C-09 estados-y-transiciones
        │        │                                      │                               │
        │        │                                      │              ┌────────────────┤
        │        │                                      │              ▼                ▼
        │        │                                      │      C-10 cancelar-turno   C-12 agenda-por-profesional
        │        │                                      │              │
        │        │                                      │              ▼
        │        │                                      │      C-11 reprogramar-turno
        │        │                                      │
        │        └────────── C-13 concurrencia-y-constraint-exclusion ◄── C-06 + C-08 + C-09
        │
        ├── C-14 auth-jwt
        │     └── C-15 rbac-por-rol
        │           └── C-16 gestionar-pacientes (+ C-05b)
        │
        ═══════════ ETAPA POSTERIOR (integraciones externas + fuera del core de turnos) ═══════════
        C-07 + C-16 ──┐
                      ├── C-17 whatsapp-adapter-y-webhook   (integración WhatsApp Business API)
        C-14 + C-16 ──┘
        C-14 + C-16 ────── C-18 mercado-pago-sena          (integración Mercado Pago)
        C-06 ───────────── C-19 google-calendar-sync       (integración Google Calendar, opcional)
```

### Paralelismo por fase

> Cada "gate" es un punto de sincronización. Los changes dentro de un grupo pueden ejecutarse en paralelo.

```
GATE 0: ninguna
  → C-01 foundation-setup                (solo)

GATE 1: C-01 ✓
  → C-02 dominio-core-models             (solo)

GATE 2: C-02 ✓                           ← PRIMER FORK (sólo C-02 requerido)
  → C-03 gestionar-prestaciones          [Agente A]
  → C-04 gestionar-profesionales         [Agente B]
  → C-05 gestionar-sillones              [Agente C]
  → C-14 auth-jwt                        [Agente C — arranca en paralelo, sólo depende de C-02]

GATE 3: C-03 + C-04 + C-05 ✓             ← catálogo listo
  → C-05b gestionar-pacientes-basico     [Agente A]
  → C-15 rbac-por-rol                    [Agente C — requiere C-14 ✓]

GATE 4: C-05b ✓                          ← núcleo habilitado (C-03 + C-04 + C-05 + C-05b)
  → C-06 crear-turno-anti-solapamiento ★ (solo)

GATE 5: C-06 ✓                           ← FORK (3 paralelos)
  → C-07 programar-recordatorio          [Agente A]
  → C-08 consultar-disponibilidad        [Agente B]
  → C-09 estados-y-transiciones-turno    [Agente C]

GATE 6: C-07 + C-09 ✓
  → C-10 cancelar-turno                  [Agente A]
  → C-12 agenda-por-profesional          [Agente B]
  → C-16 gestionar-pacientes (RBAC)      [Agente C — requiere C-05b + C-14 + C-15 ✓]

GATE 7: C-10 ✓
  → C-11 reprogramar-turno               [Agente A]
  → C-13 concurrencia-y-constraint-exclusion  [Agente B — requiere C-06 + C-08 + C-09 ✓]

GATE 8 (POSTERIOR): C-07 + C-16 ✓        ← FORK (integraciones externas)
  → C-17 whatsapp-adapter-y-webhook      [Agente A]
  → C-18 mercado-pago-sena               [Agente B]
  → C-19 google-calendar-sync            [Agente C]
```

### Camino crítico (5 changes — mínimo irreducible)

```
C-01 → C-02 → C-03 → C-06 ★ → C-08
```

> C-04, C-05 y C-05b corren en paralelo con C-03 y son prerequisitos de C-06; se elige C-03 (prestaciones) como rama representativa del catálogo. `C-05b` (alta mínima de pacientes) es un prerequisito **paralelo** de C-06: depende sólo de C-02 y corre junto a C-03/C-04/C-05, por lo que su duración se solapa con la del catálogo y **no alarga el camino crítico**. Es la secuencia mínima para tener el flujo de reserva funcionando con recurso doble y anti-solapamiento.

### Plan óptimo con 3 agentes

> El sistema es backend puro (sin UI); los 3 agentes se reparten por dominio del backend.

```
Paso │ Agente A (Núcleo de agenda)      │ Agente B (Agenda auxiliar)          │ Agente C (Seguridad / catálogo)
─────┼──────────────────────────────────┼─────────────────────────────────────┼────────────────────────────────
  1  │ C-01 foundation-setup            │ —                                   │ —
  2  │ C-02 dominio-core-models         │ —                                   │ —
  3  │ C-03 gestionar-prestaciones      │ C-04 gestionar-profesionales        │ C-05 gestionar-sillones + C-14 auth-jwt
  4  │ C-05b gestionar-pacientes-basico │ —                                   │ C-15 rbac-por-rol
  5  │ C-06 crear-turno-anti-solapamiento ★ (solo) │ —                          │ —
  6  │ C-07 programar-recordatorio      │ C-08 consultar-disponibilidad       │ C-09 estados-y-transiciones-turno
  7  │ C-10 cancelar-turno              │ C-12 agenda-por-profesional         │ C-16 gestionar-pacientes (RBAC)
  8  │ C-11 reprogramar-turno           │ C-13 concurrencia-constraint        │ —
  9  │ C-17 whatsapp-adapter (POSTERIOR)│ C-18 mercado-pago-sena (POSTERIOR)  │ C-19 google-calendar (POSTERIOR)
```

---

## FASE 0 — Cimientos

> Prerequisitos obligatorios del núcleo. No contienen reglas de negocio propias (salvo la trazabilidad de datos sintéticos).

### [C-01] `foundation-setup`
- **Estado**: `[ ]` pendiente
- **Scope**: Scaffolding del proyecto + infraestructura base (un solo módulo, paquetes por capa)
  - `pom.xml` (Maven) con Java 21, Spring Boot 3.x (web, validation, data-jpa), Flyway, driver PostgreSQL, H2 (test), JUnit 5 + AssertJ + Mockito
  - Estructura hexagonal: `domain/model`, `domain/rule`, `domain/exception`, `domain/port`, `application/service`, `application/dto`, `infrastructure/persistence`, `infrastructure/scheduler`, `api/controller`, `api/dto`, `api/security`
  - Perfiles: `application.yml`, `application-test.yml` (H2 en memoria), `application-prod.yml` (PostgreSQL); Flyway inicializado en `db/migration`
  - `docker-compose.yml` (PostgreSQL 15+ con extensión `btree_gist` + app) y `.env.example` con las variables de `08` — sin secretos versionados
  - Endpoint `GET /api/health`; CI (GitHub Actions) con `mvn test` + check de datos sintéticos en seeds/fixtures (RN-06)
  - Tests: smoke de contexto Spring + health
- **Dependencias**: ninguna
- **Governance**: BAJO
- **RN-XX**: RN-06 (CI guardrail de datos sintéticos)
- **Leer antes**:
  - `knowledge-base/02_descripcion_general.md` §Stack
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios
  - `knowledge-base/08_arquitectura_propuesta.md` §Variables de entorno
  - `knowledge-base/08_arquitectura_propuesta.md` §Despliegue

---

### [C-02] `dominio-core-models`
- **Estado**: `[ ]` pendiente
- **Scope**: Modelos de dominio, puertos, migración inicial y seed sintético
  - Modelos: `Turno`, `Paciente`, `Profesional`, `Sillon`, `Prestacion`, `Usuario`, `Recordatorio`
  - Value object `FranjaHoraria` (intervalo semiabierto `[inicio, fin)`) con validación `inicio < fin`
  - Enums: `EstadoTurno` (PENDIENTE/CONFIRMADO/CANCELADO/REALIZADO/AUSENTE), `CanalTurno` (ONLINE/MOSTRADOR), `Rol`, `EstadoRecordatorio`
  - Puertos de repositorio (`domain/port`): `TurnoRepository`, `ProfesionalRepository`, `SillonRepository`, `PrestacionRepository`, `PacienteRepository`, `UsuarioRepository`, `RecordatorioRepository`
  - Adaptadores JPA + mappers (dominio ↔ entidad) en `infrastructure/persistence`; `@Version` en `Turno` (locking optimista)
  - Migración 001: tablas `usuario, paciente, profesional, sillon, prestacion, turno, recordatorio`; índices `(profesional_id, inicio, fin)`, `(sillon_id, inicio, fin)`
  - Seed sintético (RN-06): sillones BOX-1/BOX-2, prestaciones LIMPIEZA(30)/CONSULTA(20)/ENDO(60)/EXTRACCION(40), profesionales y pacientes ficticios (`@example.test`, documentos `0000000X`)
  - Tests: `@DataJpaTest` con H2 (repositorios + mappers), test de convenciones de seed (dominio `.test`), cálculo derivado de `fin`
- **Dependencias**: C-01
- **Governance**: CRITICO
- **RN-XX**: RN-13, RN-09 (criterio de turno activo modelado), RN-06
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Entidades + §ERD + §Invariantes
  - `knowledge-base/04_modelo_de_datos.md` §Seed data inicial
  - `knowledge-base/05_reglas_de_negocio.md` §RN-13 §RN-09 §RN-06
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-07

---

## FASE 1 — Núcleo de agenda (CAMINO CRÍTICO / MVP)

> Estas changes de catálogo y alta mínima de pacientes (`C-03`, `C-04`, `C-05`, `C-05b`) se proponen en paralelo. `C-06` es el **change prioritario** y no puede proponerse hasta que las cuatro estén archivadas.

### [C-03] `gestionar-prestaciones`
- **Estado**: `[ ]` pendiente
- **Scope**: Catálogo de prestaciones con duración (la duración es el eje del cálculo del turno)
  - Modelo `Prestacion` + endpoints `GET/POST/PUT /api/prestaciones` y desactivación (escritura: Administrador; RBAC se cablea en C-15)
  - Validación `duracionMinutos > 0` y `codigo` único
  - Desactivar una prestación (`activa=false`) sin borrar turnos históricos
  - Tests: alta con duración inválida (rechazo), `codigo` duplicado (rechazo), desactivación (RN-10), duración derivada usada por el cálculo de `fin` (RN-02)
- **Dependencias**: C-02
- **Governance**: BAJO
- **RN-XX**: RN-02, RN-10
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Prestacion
  - `knowledge-base/06_funcionalidades.md` §US-003
  - `knowledge-base/05_reglas_de_negocio.md` §RN-02 §RN-10
  - `knowledge-base/03_actores_y_roles.md` §RBAC

---

### [C-04] `gestionar-profesionales`
- **Estado**: `[ ]` pendiente
- **Scope**: Catálogo de profesionales (recurso 1 del turno)
  - Modelo `Profesional` + endpoints `GET/POST/PUT /api/profesionales` y `GET /api/profesionales/{id}/agenda` (lectura)
  - Validación `matricula` única; `activo` filtra disponibilidad
  - Tests: `matricula` duplicada (rechazo), profesional inactivo no agendable (RN-11), listado y agenda
- **Dependencias**: C-02
- **Governance**: BAJO
- **RN-XX**: RN-01, RN-11
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Profesional (Odontólogo)
  - `knowledge-base/06_funcionalidades.md` §US-005
  - `knowledge-base/05_reglas_de_negocio.md` §RN-11
  - `knowledge-base/03_actores_y_roles.md` §RBAC

---

### [C-05] `gestionar-sillones`
- **Estado**: `[ ]` pendiente
- **Scope**: Catálogo de sillones/boxes (recurso 2 del turno)
  - Modelo `Sillon` + endpoints `GET/POST/PUT /api/sillones` y `GET /api/sillones/{id}/agenda` (lectura)
  - Validación `codigo` único; `activo` filtra disponibilidad
  - Tests: `codigo` duplicado (rechazo), sillón inactivo no agendable (RN-11)
- **Dependencias**: C-02
- **Governance**: BAJO
- **RN-XX**: RN-01, RN-11
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Sillon (box)
  - `knowledge-base/06_funcionalidades.md` §US-004
  - `knowledge-base/05_reglas_de_negocio.md` §RN-11
  - `knowledge-base/03_actores_y_roles.md` §RBAC

---

### [C-05b] `gestionar-pacientes-basico`
- **Estado**: `[ ]` pendiente
- **Scope**: Alta y búsqueda MÍNIMA de pacientes (prerequisito paralelo del núcleo; sin RBAC complejo)
  - Modelo `Paciente` ya declarado en `C-02` (NO se redeclara; se usa)
  - `POST /api/pacientes` — alta mínima (`nombre`, `apellido`, `documento`, `telefono`, `email` opcional)
  - `GET /api/pacientes?q=` — búsqueda mínima por `documento` / `apellido` / `telefono`, para que el mostrador encuentre al paciente al agendar
  - `GET /api/pacientes/{id}` — lectura puntual
  - Validaciones: `documento` único por consultorio; formato de `telefono`/`email`; campos obligatorios
  - **Sin** datos clínicos sensibles (Ley 25.326 / RN-06): datos personales mínimos; seed/fixtures sintéticos (`@example.test`, documentos `0000000X`)
  - **Sin RBAC complejo**: igual que `C-03`/`C-04`/`C-05`, los endpoints se montan **sin autorización por rol** y el **RBAC / verificación de propiedad se cablea en `C-15`** (mismo precedente que el catálogo)
  - Tests: alta válida; `documento` duplicado ⇒ rechazo; formato inválido ⇒ rechazo; búsqueda encuentra por `documento` y por `apellido`; el paciente creado puede referenciarse al crear un turno (costura con `C-06`)
- **Dependencias**: C-02
- **Governance**: MEDIO
- **RN-XX**: RN-06 (RN-LG — datos sintéticos / datos personales mínimos)
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Paciente
  - `knowledge-base/03_actores_y_roles.md` §RBAC
  - `knowledge-base/05_reglas_de_negocio.md` §RN-06
  - `knowledge-base/07_flujos_principales.md` §Flujo 3 (paso 1)

---

### [C-06] ⭐ `crear-turno-anti-solapamiento` — CHANGE PRIORITARIO
- **Estado**: `[ ]` pendiente
- **Scope**: Núcleo del dominio — creación transaccional de turno con recurso doble y anti-solapamiento estricto
  - Regla de dominio `RecursoDoble`: un turno requiere `Profesional` libre **Y** `Sillon` libre en `[inicio, fin)` (RN-01)
  - Regla de dominio `AntiSolapamiento`: solapamiento estricto prohibido; `fin == inicio` **permitido** (encadenado exacto) (RN-03)
  - Cálculo `fin = inicio + prestacion.duracionMinutos`; rechazo de duración manual (RN-02)
  - Validación `inicio < fin` con intervalo semiabierto `[inicio, fin)` (RN-13)
  - Caso de uso `CrearTurnoService` **transaccional**: revalida disponibilidad al confirmar, considera sólo turnos activos (RN-09), persiste `Turno` (estado PENDIENTE/CONFIRMADO, canal ONLINE/MOSTRADOR)
  - Endpoints `POST /api/public/turnos` (invitado, canal ONLINE) y `POST /api/turnos` (mostrador, canal MOSTRADOR); `409 Conflict` si un recurso está ocupado, `422` si intervalo/prestación inválidos
  - Validación de existencia del paciente referenciado (`pacienteId` debe existir; `422` si no) — costura con la alta mínima de `C-05b`
  - Tests unitarios de dominio (JUnit 5 + AssertJ, sin Spring): profesional ocupado + sillón libre ⇒ rechazo; profesional libre + sillón ocupado ⇒ rechazo; ambos libres ⇒ éxito; límite `fin(A) == inicio(B)` ⇒ éxito; `inicio(B) = fin(A) − 1 min` ⇒ rechazo (sobre profesional y sobre sillón por separado); test parametrizado de duración por prestación (RN-02); `inicio >= fin` ⇒ rechazo (RN-13)
- **Dependencias**: C-03, C-04, C-05, C-05b
- **Governance**: CRITICO
- **RN-XX**: RN-01, RN-02, RN-03, RN-13 (+ RN-09)
- **Leer antes**:
  - `knowledge-base/05_reglas_de_negocio.md` §RN-01 §RN-02 §RN-03 §RN-13
  - `knowledge-base/07_flujos_principales.md` §Flujo 2 (Reserva online)
  - `knowledge-base/04_modelo_de_datos.md` §Turno (constraints e índices)
  - `knowledge-base/08_arquitectura_propuesta.md` §Manejo de concurrencia
  - `knowledge-base/06_funcionalidades.md` §US-006 §US-007

---

### [C-07] `programar-recordatorio`
- **Estado**: `[ ]` pendiente
- **Scope**: Programación del recordatorio en el dominio (sin envío externo — el adaptador WhatsApp es POSTERIOR: C-17)
  - Al crear un turno activo se programa **un** `Recordatorio` con `programadoPara = inicio − anticipacion` (config por `APP_RECORDATORIO_ANTICIPACION_MIN`)
  - `NotificadorPort` (interfaz) con implementación no-op/log en el MVP
  - Scheduler (`@Scheduled`) que consulta `estado = PROGRAMADO` y `programadoPara <= now`, marcando `ENVIADO`/`FALLIDO` (sin envío real)
  - Endpoint `GET /api/turnos/{id}/recordatorio`
  - Tests: creación de turno ⇒ exactamente un recordatorio en `programadoPara` esperado; `programadoPara < inicio` (RN-05)
- **Dependencias**: C-06
- **Governance**: MEDIO
- **RN-XX**: RN-05
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Recordatorio
  - `knowledge-base/05_reglas_de_negocio.md` §RN-05
  - `knowledge-base/07_flujos_principales.md` §Flujo 5
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones (Scheduler)
  - `knowledge-base/06_funcionalidades.md` §US-011

---

### [C-08] `consultar-disponibilidad`
- **Estado**: `[ ]` pendiente
- **Scope**: Consulta de franjas con recurso doble libre (misma fuente para online y mostrador)
  - `GET /api/public/disponibilidad?prestacionId=&fecha=` (público) y `GET /api/disponibilidad` (autenticado)
  - Calcula la duración desde la prestación (RN-02) y devuelve franjas con Profesional **Y** Sillón libres (RN-01)
  - Sólo considera turnos activos (RN-09); el cancelado no ocupa recursos
  - Tests: franja ofrecida sólo si ambos recursos libres; franja no ofrecida si uno está ocupado; respeta la duración de la prestación elegida
- **Dependencias**: C-06
- **Governance**: MEDIO
- **RN-XX**: RN-01, RN-02, RN-09
- **Leer antes**:
  - `knowledge-base/07_flujos_principales.md` §Flujo 2 (pasos 1-3)
  - `knowledge-base/05_reglas_de_negocio.md` §RN-01 §RN-09
  - `knowledge-base/04_modelo_de_datos.md` §Turno (índices)
  - `knowledge-base/06_funcionalidades.md` §US-006

---

### [C-09] `estados-y-transiciones-turno`
- **Estado**: `[ ]` pendiente
- **Scope**: Ciclo de vida y transiciones válidas del turno
  - `EstadoTurno` + máquina de transiciones validada en el dominio: `PENDIENTE→CONFIRMADO`, `PENDIENTE→CANCELADO`, `CONFIRMADO→CANCELADO`, `CONFIRMADO→REALIZADO`, `CONFIRMADO→AUSENTE` (RN-07, RN-08)
  - Criterio de "turno activo" (`PENDIENTE`/`CONFIRMADO`) que ocupa recursos; estados finales no ocupan (RN-09)
  - Endpoint `POST /api/turnos/{id}/confirmar`; transición inválida ⇒ `409`
  - Tests de tabla (origen × destino) de aceptación/rechazo; `CANCELADO → CONFIRMADO` falla; un `REALIZADO` no ocupa recursos (RN-09)
- **Dependencias**: C-06
- **Governance**: MEDIO
- **RN-XX**: RN-07, RN-08, RN-09
- **Leer antes**:
  - `knowledge-base/05_reglas_de_negocio.md` §RN-07 §RN-08 §RN-09
  - `knowledge-base/04_modelo_de_datos.md` §Turno (estado)
  - `knowledge-base/06_funcionalidades.md` §US-012
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-04

---

### [C-10] `cancelar-turno`
- **Estado**: `[ ]` pendiente
- **Scope**: Cancelación con liberación inmediata de ambos recursos
  - `POST /api/turnos/{id}/cancelar` (paciente propio / recepcionista / administrador)
  - Valida transición permitida (RN-08) y pasa a `CANCELADO` (RN-07); como el cancelado no ocupa recursos, la franja se libera de inmediato (RN-04, RN-09)
  - Cancela el `Recordatorio` asociado (RN-05)
  - Tests: crear → cancelar → crear otro en la misma franja y recursos (éxito) (RN-04); cancelar un turno final ⇒ `409` (RN-08); recordatorio queda `CANCELADO` (RN-05)
- **Dependencias**: C-09, C-07
- **Governance**: MEDIO
- **RN-XX**: RN-04, RN-08, RN-09, RN-05
- **Leer antes**:
  - `knowledge-base/07_flujos_principales.md` §Flujo 4
  - `knowledge-base/05_reglas_de_negocio.md` §RN-04 §RN-08 §RN-09
  - `knowledge-base/06_funcionalidades.md` §US-009
  - `knowledge-base/03_actores_y_roles.md` §RBAC

---

### [C-11] `reprogramar-turno`
- **Estado**: `[ ]` pendiente
- **Scope**: Reprogramación atómica (libera la franja vieja y reserva la nueva)
  - `POST /api/turnos/{id}/reprogramar` en una transacción: si la nueva franja no tiene ambos recursos, la operación falla y el turno original queda intacto (RN-15)
  - Aplica RN-01/RN-03/RN-04/RN-13 sobre la franja nueva
  - Reprograma el `Recordatorio` a la nueva fecha (uno vigente, RN-12)
  - Tests: reprogramar a franja ocupada ⇒ rechazo + turno original sin cambios (RN-15); a franja libre ⇒ éxito + franja vieja liberada; exactamente un recordatorio `PROGRAMADO` apuntando a la nueva fecha (RN-12)
- **Dependencias**: C-09, C-10, C-07
- **Governance**: ALTO
- **RN-XX**: RN-15, RN-04, RN-12, RN-01, RN-03
- **Leer antes**:
  - `knowledge-base/05_reglas_de_negocio.md` §RN-15 §RN-12
  - `knowledge-base/07_flujos_principales.md` §Flujo 4
  - `knowledge-base/06_funcionalidades.md` §US-010
  - `knowledge-base/04_modelo_de_datos.md` §Turno

---

### [C-12] `agenda-por-profesional`
- **Estado**: `[ ]` pendiente
- **Scope**: Consulta de la agenda del profesional y del sillón
  - `GET /api/profesionales/{id}/agenda` — turnos activos ordenados por `inicio`, con paciente, prestación, sillón y franja (RN-09)
  - `GET /api/sillones/{id}/agenda` (analógico)
  - Tests: listado ordenado por `inicio`, sólo turnos activos, campos completos
- **Dependencias**: C-06, C-09
- **Governance**: BAJO
- **RN-XX**: RN-09
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-008
  - `knowledge-base/04_modelo_de_datos.md` §Turno
  - `knowledge-base/03_actores_y_roles.md` §RBAC
  - `knowledge-base/05_reglas_de_negocio.md` §RN-09

---

## FASE 2 — Concurrencia y consistencia (endurecimiento del núcleo)

### [C-13] `concurrencia-y-constraint-exclusion`
- **Estado**: `[ ]` pendiente
- **Scope**: Garantía dura contra la doble reserva concurrente (online vs. mostrador)
  - Locking pesimista por recurso+franja dentro de la transacción de creación (lock adoptivo sobre `(recursoId, fecha)` / `SELECT ... FOR UPDATE`)
  - Locking optimista con `@Version` en `Turno`; traducción de `OptimisticLockException` a error de dominio controlado
  - Migración: constraint de exclusión PostgreSQL `EXCLUDE USING gist (profesional_id WITH =, tsrange(inicio, fin, '[)') WITH &&) WHERE (estado IN ('PENDIENTE','CONFIRMADO'))` y análogo para `sillon_id`; extensión `btree_gist`
  - Traducción de `23P01 exclusion_violation` a `409 Conflict` (no excepción cruda de base)
  - Tests de concurrencia (dos hilos/transacciones sobre la misma franja ⇒ una gana, otra rechazo controlado, RN-16) con H2 + locking; tests del constraint con Testcontainers PostgreSQL
- **Dependencias**: C-06, C-08, C-09
- **Governance**: CRITICO
- **RN-XX**: RN-16, RN-01, RN-03
- **Leer antes**:
  - `knowledge-base/08_arquitectura_propuesta.md` §Manejo de concurrencia
  - `knowledge-base/05_reglas_de_negocio.md` §RN-16 §RN-03
  - `knowledge-base/06_funcionalidades.md` §US-013
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-06 §DD-08

---

## FASE 3 — Acceso y personas

> Rama de seguridad. Sólo necesita `C-02` para arrancar, por lo que puede desarrollarse en paralelo al núcleo de agenda. Los endpoints de catálogo y turnos se cablean con RBAC una vez que `C-15` está archivado.

### [C-14] `auth-jwt`
- **Estado**: `[ ]` pendiente
- **Scope**: Autenticación JWT stateless con roles embebidos
  - `POST /api/auth/login` (JWT access), `POST /api/auth/refresh`, `GET /api/auth/me`
  - Hash de contraseña (bcrypt/argon2); verifica `Usuario.activo`; claims `sub` + `rol`
  - Filtro de seguridad stateless; rutas públicas declaradas en `03`
  - Tests: login válido ⇒ token con rol; credenciales inválidas ⇒ `401` sin filtrar el campo; cuenta inactiva ⇒ `403`; refresh de token
- **Dependencias**: C-02
- **Governance**: CRITICO
- **RN-XX**: RN-LG (RN-06)
- **Leer antes**:
  - `knowledge-base/07_flujos_principales.md` §Flujo 1
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas §Modelo de autenticación
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad
  - `knowledge-base/06_funcionalidades.md` §US-001
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-10

---

### [C-15] `rbac-por-rol`
- **Estado**: `[ ]` pendiente
- **Scope**: Autorización por rol a nivel de endpoint + verificación de propiedad en el dominio
  - Implementa la matriz RBAC de `03` en todos los endpoints de catálogo y turnos
  - Paciente sólo opera sobre lo propio; `403` en accesos indebidos
  - Tests: paciente recibe `403` al modificar el catálogo o turnos ajenos; verificación de cada fila de la matriz
- **Dependencias**: C-14
- **Governance**: ALTO
- **RN-XX**: — (permisos transversales)
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC (matriz) §Rutas autenticadas
  - `knowledge-base/06_funcionalidades.md` §US-002
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad
  - `knowledge-base/07_flujos_principales.md` §Flujo 1 (paso 7)

---

### [C-16] `gestionar-pacientes` — capa de autorización y gestión extendida
- **Estado**: `[ ]` pendiente
- **Scope**: Autorización RBAC y gestión extendida de pacientes, **construida SOBRE `C-05b`** (que ya aporta el alta y la búsqueda básica). `C-16` NO repite el CRUD básico.
  - Aplica la matriz RBAC de `03` a los endpoints de pacientes de `C-05b`: recepcionista/administrador escriben; paciente propio sólo lectura sobre lo suyo
  - Verificación de propiedad + **aislamiento por propiedad** (`403` en accesos indebidos)
  - Edición y desactivación de pacientes (`PUT /api/pacientes/{id}`, borrado lógico — sin borrado físico si está referenciado por turnos)
  - Sin datos clínicos sensibles (RN-LG / Ley 25.326)
  - Tests: recepcionista/administrador escriben y paciente propio sólo lee lo suyo; `403` de paciente al modificar datos de pacientes; `403` en accesos indebidos (aislamiento por propiedad); edición/desactivación respetan `documento` único y formato de campos
- **Dependencias**: C-05b, C-14, C-15
- **Governance**: MEDIO
- **RN-XX**: RN-06 (RN-LG)
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Paciente
  - `knowledge-base/03_actores_y_roles.md` §RBAC
  - `knowledge-base/05_reglas_de_negocio.md` §RN-06 (RN-LG)
  - `knowledge-base/07_flujos_principales.md` §Flujo 3 (paso 1)

---

## FASE 4 — ETAPA POSTERIOR: Integraciones externas y funcionalidades fuera del core

> ⚠️ **Estos changes NO forman parte del MVP del camino crítico.** Son integraciones con terceros y funcionalidades fuera del núcleo de turnos. Dependen de que el flujo de turnos (FASE 1) y la seguridad (FASE 3) estén estables. No deben proponerse antes de archivar el camino crítico.

### [C-17] `whatsapp-adapter-y-webhook` — POSTERIOR (integración)
- **Estado**: `[ ]` pendiente
- **Scope**: Adaptador real de WhatsApp Business API + webhook de confirmación
  - `infrastructure/whatsapp` que implementa `NotificadorPort` (reemplaza el no-op de C-07); config `WHATSAPP_API_TOKEN`, `WHATSAPP_PHONE_ID`
  - Envío real por el scheduler; recordatorio `ENVIADO`/`FALLIDO`
  - `POST /api/webhooks/whatsapp` con validación por firma/secret; confirmación ⇒ turno `CONFIRMADO` (una confirmación sobre cancelado no reactiva, RN-08)
  - Tests con proveedor mockeado; firma inválida ⇒ rechazo; confirmación sobre cancelado ⇒ sin cambio
  - Sujeto a pregunta abierta P-01 (API oficial vs. no oficial)
- **Dependencias**: C-07, C-16
- **Governance**: ALTO
- **RN-XX**: RN-05, RN-08
- **Leer antes**:
  - `knowledge-base/07_flujos_principales.md` §Flujo 5
  - `knowledge-base/02_descripcion_general.md` §Integraciones externas
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas
  - `knowledge-base/10_preguntas_abiertas.md` §P-01
  - `knowledge-base/06_funcionalidades.md` §US-011 §US-012

---

### [C-18] `mercado-pago-sena` — POSTERIOR (integración)
- **Estado**: `[ ]` pendiente
- **Scope**: Cobro de seña vía Mercado Pago (fuera del camino crítico, SU-08)
  - `infrastructure/mercadopago`; config `MERCADOPAGO_ACCESS_TOKEN`
  - `POST /api/webhooks/mercadopago` con validación por firma; política de seña según P-02
  - No bloquea la confirmación del turno salvo que la cátedra/PO defina lo contrario
- **Dependencias**: C-14, C-16
- **Governance**: ALTO
- **RN-XX**: RN-06 (RN-LG — datos de pago)
- **Leer antes**:
  - `knowledge-base/02_descripcion_general.md` §Integraciones externas
  - `knowledge-base/10_preguntas_abiertas.md` §P-02
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-08
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas

---

### [C-19] `google-calendar-sync` — POSTERIOR (integración, opcional)
- **Estado**: `[ ]` pendiente
- **Scope**: Sincronización de la agenda del profesional con Google Calendar
  - `infrastructure/calendar` (OAuth 2.0, `GOOGLE_CALENDAR_CREDENTIALS`)
  - Post-estabilización del flujo de turnos
- **Dependencias**: C-06
- **Governance**: MEDIO
- **RN-XX**: —
- **Leer antes**:
  - `knowledge-base/02_descripcion_general.md` §Integraciones externas
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones (puertos y adaptadores)
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-01

---

## Backlog OUT del MVP (no son changes)

Funcionalidades explícitamente fuera del alcance de la v1 ([`01_vision_y_objetivos.md`](knowledge-base/01_vision_y_objetivos.md) §OUT): odontograma interactivo 3D, periodontograma avanzado, integración de radiología digital, IA de diagnóstico. No se planifican como changes hasta que la cátedra las incorpore.

---

## Resumen de changes

| ID | Change | Fase | Dependencias | Governance | RN-XX |
|---|---|---|---|---|---|
| C-01 | `foundation-setup` | 0 — Cimientos | — | BAJO | RN-06 |
| C-02 | `dominio-core-models` | 0 — Cimientos | C-01 | CRITICO | RN-13, RN-09, RN-06 |
| C-03 | `gestionar-prestaciones` | 1 — Núcleo de agenda | C-02 | BAJO | RN-02, RN-10 |
| C-04 | `gestionar-profesionales` | 1 — Núcleo de agenda | C-02 | BAJO | RN-01, RN-11 |
| C-05 | `gestionar-sillones` | 1 — Núcleo de agenda | C-02 | BAJO | RN-01, RN-11 |
| C-05b | `gestionar-pacientes-basico` | 1 — Núcleo de agenda | C-02 | MEDIO | RN-06 (RN-LG) |
| **C-06** | **`crear-turno-anti-solapamiento` ★** | **1 — Núcleo de agenda** | **C-03, C-04, C-05, C-05b** | **CRITICO** | **RN-01, RN-02, RN-03, RN-13** |
| C-07 | `programar-recordatorio` | 1 — Núcleo de agenda | C-06 | MEDIO | RN-05 |
| C-08 | `consultar-disponibilidad` | 1 — Núcleo de agenda | C-06 | MEDIO | RN-01, RN-02, RN-09 |
| C-09 | `estados-y-transiciones-turno` | 1 — Núcleo de agenda | C-06 | MEDIO | RN-07, RN-08, RN-09 |
| C-10 | `cancelar-turno` | 1 — Núcleo de agenda | C-09, C-07 | MEDIO | RN-04, RN-08, RN-09, RN-05 |
| C-11 | `reprogramar-turno` | 1 — Núcleo de agenda | C-09, C-10, C-07 | ALTO | RN-15, RN-04, RN-12, RN-01, RN-03 |
| C-12 | `agenda-por-profesional` | 1 — Núcleo de agenda | C-06, C-09 | BAJO | RN-09 |
| C-13 | `concurrencia-y-constraint-exclusion` | 2 — Concurrencia | C-06, C-08, C-09 | CRITICO | RN-16, RN-01, RN-03 |
| C-14 | `auth-jwt` | 3 — Acceso y personas | C-02 | CRITICO | RN-06 (RN-LG) |
| C-15 | `rbac-por-rol` | 3 — Acceso y personas | C-14 | ALTO | — |
| C-16 | `gestionar-pacientes` (RBAC + gestión extendida) | 3 — Acceso y personas | C-05b, C-14, C-15 | MEDIO | RN-06 (RN-LG) |
| C-17 | `whatsapp-adapter-y-webhook` | 4 — POSTERIOR | C-07, C-16 | ALTO | RN-05, RN-08 |
| C-18 | `mercado-pago-sena` | 4 — POSTERIOR | C-14, C-16 | ALTO | RN-06 (RN-LG) |
| C-19 | `google-calendar-sync` | 4 — POSTERIOR | C-06 | MEDIO | — |

### Primer change recomendado

`C-01 foundation-setup`. Para arrancar: `/opsx:propose C-01-foundation-setup`.

> El **change prioritario/ancla** del MVP es `C-06 crear-turno-anti-solapamiento`; es el primer change funcional del núcleo de agenda una vez cubiertos los cimientos (`C-01`, `C-02`) y el catálogo/alta mínima de pacientes (`C-03`, `C-04`, `C-05`, `C-05b`).





