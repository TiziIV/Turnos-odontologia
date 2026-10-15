# turnos-odontologia — Instrucciones para Agentes

> Este archivo (y su copia idéntica `CLAUDE.md`) es lo PRIMERO que todo agente lee al entrar al repo.
> Generado a partir de `knowledge-base/`, `CHANGES.md` y `.atl/skill-registry.md`. No editar a mano sin re-sincronizar `AGENTS.md` y `CLAUDE.md`.

---

## Propósito del Proyecto

`turnos-odontologia` es una **API/backend puro** (sin UI) para la gestión de turnos de **un único consultorio odontológico** (mono-tenant, equipo chico <50 personas). Su núcleo es el **turno como recurso doble**: cada turno exige **simultáneamente** un `Profesional` libre **y** un `Sillon/box` libre en su franja, con **duración derivada de la prestación** y **anti-solapamiento estricto** (se admite encadenado exacto). El principal riesgo —agendamiento concurrente online vs. mostrador— se resuelve con transacciones, locking y un **constraint de exclusión PostgreSQL**.

> Prioridad declarada: **mantenibilidad y verificabilidad** (tests unitarios estrictos + trazabilidad de reglas `RN-XX`).

---

## Stack Tecnológico

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

**Comando de test objetivo:** `python -m pytest` (cuando esté implementado).

Detalle completo: [knowledge-base/02_descripcion_general.md](knowledge-base/02_descripcion_general.md)

---

## Base de Conocimiento

La fuente de verdad del dominio vive en `knowledge-base/`. **Leé el archivo relevante ANTES de implementar.**

| Archivo | Cuándo leerlo |
|---------|---------------|
| [01_vision_y_objetivos.md](knowledge-base/01_vision_y_objetivos.md) | Propósito, alcance IN/OUT, métricas de éxito |
| [02_descripcion_general.md](knowledge-base/02_descripcion_general.md) | Stack, arquitectura general, integraciones, mono-tenant |
| [03_actores_y_roles.md](knowledge-base/03_actores_y_roles.md) | Auth, RBAC, rutas públicas vs. autenticadas |
| [04_modelo_de_datos.md](knowledge-base/04_modelo_de_datos.md) | Entidades, ERD, invariantes, seed sintético |
| [05_reglas_de_negocio.md](knowledge-base/05_reglas_de_negocio.md) | Reglas `RN-01`…`RN-16` codificadas |
| [06_funcionalidades.md](knowledge-base/06_funcionalidades.md) | Historias de usuario y criterios de aceptación |
| [07_flujos_principales.md](knowledge-base/07_flujos_principales.md) | Flujos E2E (auth, reserva, mostrador, cancelación, recordatorio) |
| [08_arquitectura_propuesta.md](knowledge-base/08_arquitectura_propuesta.md) | Patrones, directorios, concurrencia, env vars |
| [09_decisiones_y_supuestos.md](knowledge-base/09_decisiones_y_supuestos.md) | Decisiones `DD-XX` y supuestos `SU-XX` |
| [10_preguntas_abiertas.md](knowledge-base/10_preguntas_abiertas.md) | ⚠️ Inconsistencias a resolver ANTES de codear |

> ⚠️ Resolver las preguntas de prioridad **Alta** de `10_preguntas_abiertas.md` antes de arrancar el primer change.

---

## Estructura de Capas (hexagonal)

Estructura canónica (detalle en [08_arquitectura_propuesta.md](knowledge-base/08_arquitectura_propuesta.md) §Estructura de directorios):

```
src/turnos/
├── domain/            # núcleo: SIN framework
│   ├── model/         # Turno, Profesional, Sillon, Prestacion, Paciente, Recordatorio
│   ├── rule/          # reglas RN-NN (duración, solapamiento, transiciones)
│   ├── exception/     # errores de dominio
│   └── port/          # interfaces de repositorio y servicios externos
├── application/       # casos de uso / orquestación transaccional
│   ├── service/       # AgendaService, TurnoService, RecordatorioService
│   └── dto/           # comandos y resultados de aplicación
├── infrastructure/    # adaptadores: persistence, whatsapp, mercadopago, calendar, scheduler
└── api/               # controller, dto, security (JWT/RBAC)
```

**Regla de dependencia (obligatoria):** `domain` **no conoce** FastAPI, Pydantic, SQLAlchemy ni la base de datos — el paquete `domain` no importa framework alguno. Las dependencias apuntan hacia adentro: `api → application → domain` y `infrastructure → domain` (vía puertos). El dominio se testea sin framework.

---

## Skills Disponibles

| Rol | Referencias registradas | Estado |
|---|---|---|
| Orquestación | `active-orchestrator`, `kb-creator`, `roadmap-generator`, `agents-md-generator`, `skill-registry`, `openspec-*` | Referencias de la fundación; verificar disponibilidad en el entorno actual |
| Persistencia | `postgresql-table-design` | Referencia heredada; no se afirma instalación local nueva |
| Backend Python y tests | Convenciones de KB 02/08 y este archivo | No se ha instalado ni verificado una skill Python en este ajuste |

`java-springboot` y `java-junit` fueron registradas en la fundación anterior y quedan **obsoletas para el stack actual**. No cargarlas para implementar Python. El registro conserva su historia sin convertirla en instrucciones activas.

Los compact rules se resuelven desde `.atl/skill-registry.md`. Las rutas heredadas deben comprobarse antes de invocar una skill; este ajuste no modifica instalaciones globales.

---

## Roadmap de Changes

> **Excepción académica aprobada el 2026-10-15:** C-06 es el primer change entregado (conserva su ID). Incluye base mínima FastAPI + dominio/modelos/puertos + fixtures sintéticos + pytest, con repositorios en memoria para demo local. No requiere archivar antes C-01/C-02/C-03/C-04/C-05/C-05b: sus capacidades completas siguen pendientes. CRUDs, login/RBAC e integraciones se difieren; PostgreSQL/SQLAlchemy/Alembic siguen como diseño futuro si no implementados. No afirmar persistencia durable ni concurrencia real. Explore/Propose debe concretar estos límites antes de Apply.


El plan de implementación completo está en [CHANGES.md](CHANGES.md). Resumen:

- **Total:** 20 changes en 5 fases (0 Cimientos → 4 POSTERIOR).
- **Camino crítico del producto completo (5):** `C-01 → C-02 → C-03 → C-06 ★ → C-08`.
- **Change prioritario/ancla:** `C-06 crear-turno-anti-solapamiento ★` — primer change funcional del núcleo (recurso doble + anti-solapamiento).
- **Primer change del producto completo:** `C-01 foundation-setup`.
- **Primer change entregado en el trabajo académico:** `C-06 crear-turno-anti-solapamiento`, con base mínima incluida y alcance acotado aprobado.

**Flujo OPSX:** `/opsx:propose <change>` → implementar las tasks → `/opsx:archive <change>` (+ marcar `[x]` en `CHANGES.md`). Antes de cualquier `propose`, leé `CHANGES.md`, verificá dependencias archivadas o la excepción académica explícita de C-06 y leé los archivos de "Leer antes".

---

## Reglas Duras (específicas del proyecto)

> Reglas **globales** ya definidas en la config del stack (`~/.config/opencode/opencode.json`, agente `sdd-orchestrator`): orquestación/delegación OPSX, protocolo de Engram, TDD estricto, asignación de modelos y gobernanza por dominio. El proyecto las **hereda**; acá viven solo las reglas **específicas de este proyecto**. Si necesitás una global, referenciala con un puntero de una línea — no la copies.

Son contrato: romperlas es un defecto.

### 1. Regla de dominio estricta — Protección de datos (Ley 25.326 / RN-06)

**Prohibido almacenar o incluir datos reales o sensibles de pacientes en el repositorio, fixtures, tests o documentación. Usar exclusivamente datos y nombres sintéticos.**
- **Respaldo KB:** [05_reglas_de_negocio.md §RN-06 (RN-LG)](knowledge-base/05_reglas_de_negocio.md) · [04_modelo_de_datos.md §Seed data inicial](knowledge-base/04_modelo_de_datos.md) · [09_decisiones_y_supuestos.md](knowledge-base/09_decisiones_y_supuestos.md).
- **Cómo se hace cumplir:** secciones **solo con datos ficticios** (dominio `@example.test`, documentos `0000000X`); sin columnas de datos clínicos en el MVP; **guardrail de CI** en GitHub Actions sobre seeds/fixtures (change `C-01`) + revisión del contenido del repo; test/chequeo de convenciones de seed.

### 2. Arquitectura — Hexagonal sobre convenciones por feature

**Prevalencia estricta del diseño hexagonal (`domain` / `application` / `infrastructure`) sobre convenciones por feature. Dominio puro, sin acoplamiento a frameworks.**
- **Respaldo KB:** [08_arquitectura_propuesta.md §Estructura de directorios / §Patrones](knowledge-base/08_arquitectura_propuesta.md).
- **Cómo se hace cumplir:** el paquete `domain` **no importa** FastAPI/Pydantic/SQLAlchemy (verificable por revisión y por los tests de dominio sin framework); si una skill sugiere organizar por feature, **prevalecen las capas del proyecto**.

### 3. Consistencia de anti-solapamiento — RN-01 / RN-02 / RN-03

**Todo turno debe respetar `RN-01`, `RN-02` y `RN-03`. Un turno puede iniciar en el instante exacto en que termina el anterior (caso de borde válido).**
- **Respaldo KB:** [05_reglas_de_negocio.md §RN-01 §RN-02 §RN-03](knowledge-base/05_reglas_de_negocio.md) · [08_arquitectura_propuesta.md §Manejo de concurrencia](knowledge-base/08_arquitectura_propuesta.md).
- **Cómo se hace cumplir:** tests de dominio (recurso doble libre, duración derivada de la prestación, `fin(A) == inicio(B)` ⇒ **éxito**, `inicio(B) = fin(A) − 1 min` ⇒ **rechazo**) + `constraint` de exclusión PostgreSQL (`EXCLUDE USING gist` con `tsrange` semiabierto `[inicio, fin)`), a probar con PostgreSQL real (change `C-13`, pendiente).

### 4. Testing — pytest obligatorio

**Pruebas unitarias obligatorias con pytest para cada escenario de cambio, sin depender de FastAPI ni de SQLAlchemy para la lógica pura de dominio.**
- **Respaldo KB:** [08_arquitectura_propuesta.md §Estrategia de tests](knowledge-base/08_arquitectura_propuesta.md) · [05_reglas_de_negocio.md](knowledge-base/05_reglas_de_negocio.md) (cada regla indica "cómo se testea").
- **Cómo se hace cumplir:** la lógica de dominio se testea con **pytest puro** (sin FastAPI ni ORM); el CI corre `python -m pytest`; test parametrizado obligatorio de duración por prestación (`RN-02`) y de límite de solapamiento (`RN-03`/`RN-13`) en `C-06 ★`.

---

> **Límite:** tests unitarios con fakes no prueban constraints, atomicidad ni concurrencia PostgreSQL (RN-16). Se necesita integración separada sobre PostgreSQL real.

## Convenciones del Proyecto (reemplazan skills inexistentes)

Los 6 gaps sin skill candidata se cubren con convención + puntero a la KB. Un agente **DEBE** respetarlas sin ayuda de ninguna skill.

| # | Change(s) | Convención | Dónde vive |
|---|-----------|-----------|------------|
| 1 | C-13 | Constraint `EXCLUDE USING gist (profesional_id WITH =, tsrange(inicio,fin,'[)') WITH &&) WHERE (estado IN ('PENDIENTE','CONFIRMADO'))` + análogo para `sillon_id`; extensión `btree_gist`; traducir SQLSTATE **`23P01` → `409 Conflict`** | [08 §Manejo de concurrencia](knowledge-base/08_arquitectura_propuesta.md) · [09 DD-06/DD-08](knowledge-base/09_decisiones_y_supuestos.md) |
| 2 | C-13 | Tests del constraint con **PostgreSQL real** (Docker Compose o Testcontainers para Python); los fakes no validan `EXCLUDE USING gist` | [08 §Manejo de concurrencia](knowledge-base/08_arquitectura_propuesta.md) · [CHANGES.md C-13](CHANGES.md) |
| 3 | C-13 | Locking **pesimista** (`SELECT ... FOR UPDATE` por `(recursoId, fecha)`) + **optimista** (columna de versión SQLAlchemy en `Turno`); traducir `StaleDataError` a error de dominio controlado | [08 §Manejo de concurrencia](knowledge-base/08_arquitectura_propuesta.md) |
| 4 | C-01, C-02 | Arquitectura **hexagonal limpia** por capa; el dominio no depende de frameworks | [08 §Estructura de directorios](knowledge-base/08_arquitectura_propuesta.md) |
| 5 | C-01 | Guardrail de CI para datos sintéticos (**RN-06**): dominios `@example.test`, documentos `0000000X` | [05 §RN-06](knowledge-base/05_reglas_de_negocio.md) · [CHANGES.md C-01](CHANGES.md) |
| 6 | C-17, C-18, C-19 | Integraciones externas (WhatsApp Business API, Mercado Pago, Google Calendar) **fuera del MVP**; reevaluar en Fase 4 | [02 §Integraciones externas](knowledge-base/02_descripcion_general.md) · [10](knowledge-base/10_preguntas_abiertas.md) |

---

## Trazabilidad RN-XX

Toda regla de negocio `RN-XX` **debe**: (a) tener al menos un **test automatizado** que la respalde (cita la regla en el nombre del test), y (b) **citarse en los criterios de aceptación** de la historia correspondiente en `06_funcionalidades.md`. Es la métrica de éxito "trazabilidad de reglas" del proyecto.

---

## Flujo de Trabajo

```
1. Leer la KB relevante (knowledge-base/)        → entender el dominio
2. Identificar el change en CHANGES.md           → respetar dependencias
3. /opsx:propose C-NN-nombre                     → proposal + design + specs + tasks
4. Implementar las tasks (cargando skills)       → respetando las reglas duras
5. /opsx:archive C-NN-nombre + marcar [x]        → cerrar el change
```

Aplicar TODAS las reglas duras en cada paso. Ante conflicto entre la KB y este archivo, **las reglas duras prevalecen**.

---

## Punteros

- **KB:** [`knowledge-base/`](knowledge-base/) (índice en [README.md](knowledge-base/README.md))
- **Roadmap:** [`CHANGES.md`](CHANGES.md)
- **Registro de skills + reglas compactas:** [`.atl/skill-registry.md`](.atl/skill-registry.md)
- **OpenSpec:** [`openspec/`](openspec/)
