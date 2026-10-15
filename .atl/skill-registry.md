# Skill Registry — turnos-odontologia

**Delegator use only.** Índice de resolución para la fase `apply`: dado un change, resolver qué skill(s) aplican y qué reglas compactas inyectar en el prompt del sub-agente. Los sub-agentes NO leen este archivo ni los `SKILL.md` — reciben las reglas ya resueltas en su launch prompt.

- **Proyecto:** turnos-odontologia (backend puro Java 21 + Spring Boot 3 + PostgreSQL)
- **Fecha:** 2026-10-15
- **Generado por:** skill-registry
- **Change ancla:** C-06 (`crear-turno-anti-solapamiento`)

---

## ⚠️ Nota operativa — gotcha de skills externas

Las 3 skills de dominio (`java-springboot`, `java-junit`, `postgresql-table-design`) **NO** están en `~/.config/opencode/skills/` sino en `~/.agents/skills/` (store canónico cross-agent del instalador). OpenCode las levanta igual porque escanea `~/.agents/skills/**/SKILL.md` como *external skills*.

**CRÍTICO:** OpenCode carga config/skills una sola vez al arrancar y **NO hace hot-reload**. Hasta que el usuario **reinicie OpenCode**, esas 3 skills **no existen** para los agentes. Si un sub-agente de `apply` intenta invocar `java-junit` (etc.) sin haber reiniciado, la invocación **falla**.

- **Escape hatch:** `OPENCODE_DISABLE_EXTERNAL_SKILLS=1` desactiva por completo las external skills.
- **Mitigación:** las reglas compactas de §Skills de dominio están auto-contenidas abajo, así que un sub-agente puede aplicar la convención aunque la skill no esté cargada todavía.

---

## Tabla de skills disponibles

| # | Skill | Tipo | Fuente | Ruta | Para qué changes |
|---|-------|------|--------|------|------------------|
| 1 | `active-orchestrator` | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/active-orchestrator/SKILL.md` | flujo de fundación (orquesta fases) |
| 2 | `agents-md-generator` *(dir: `agent-instruction`)* | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/agent-instruction/SKILL.md` | genera AGENTS.md/CLAUDE.md |
| 3 | `discovery-research` | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/discovery-research/SKILL.md` | fase discovery |
| 4 | `find-skills` *(dir: `find-skill`)* | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/find-skill/SKILL.md` | descubrir/instalar skills |
| 5 | `kb-creator` | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/kb-creator/SKILL.md` | armar knowledge-base/ |
| 6 | `roadmap-generator` | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/roadmap-generator/SKILL.md` | generar CHANGES.md |
| 7 | `skill-creator` | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/skill-creator/SKILL.md` | crear skills nuevas (gaps repetibles) |
| 8 | `skill-registry` | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/skill-registry/SKILL.md` | este registro |
| 9 | `web-scraper` | flujo | local `~/.config/opencode/skills` | `~/.config/opencode/skills/web-scraper/SKILL.md` | investigar competidores por URL |
| 10 | `java-springboot` | **dominio** | external `github/awesome-copilot` | `~/.agents/skills/java-springboot/SKILL.md` | C-01, C-02, C-03, C-04, C-05, C-05b, C-06, C-08 |
| 11 | `java-junit` | **dominio** | external `github/awesome-copilot` | `~/.agents/skills/java-junit/SKILL.md` | **C-06 ★**, C-02 |
| 12 | `postgresql-table-design` | **dominio** | external `wshobson/agents` | `~/.agents/skills/postgresql-table-design/SKILL.md` | C-02, **C-13** |
| 13 | `openspec-propose` | infra (OPSX) | proyecto `.opencode/skills` | `.opencode/skills/openspec-propose/SKILL.md` | `/opsx:propose` de todo change |
| 14 | `openspec-apply-change` | infra (OPSX) | proyecto `.opencode/skills` | `.opencode/skills/openspec-apply-change/SKILL.md` | fase apply de todo change |
| 15 | `openspec-archive-change` | infra (OPSX) | proyecto `.opencode/skills` | `.opencode/skills/openspec-archive-change/SKILL.md` | archivar change |
| 16 | `openspec-explore` | infra (OPSX) | proyecto `.opencode/skills` | `.opencode/skills/openspec-explore/SKILL.md` | explorar antes de proponer |
| 17 | `openspec-sync-specs` | infra (OPSX) | proyecto `.opencode/skills` | `.opencode/skills/openspec-sync-specs/SKILL.md` | sincronizar specs |
| 18 | `openspec-update-change` | infra (OPSX) | proyecto `.opencode/skills` | `.opencode/skills/openspec-update-change/SKILL.md` | actualizar un change en curso |
| — | comandos OPSX | infra (OPSX) | proyecto `.opencode/commands` | `.opencode/commands/opsx-{apply,archive,explore,propose,sync,update}.md` | slash commands (no son skills) |

> Las 6 skills `openspec-*` son **infraestructura del flujo OPSX**, NO skills de dominio. No modificarlas ni reemplazarlas.

---

## Reglas compactas — skills de dominio

Copiar el bloque que corresponda al change en el prompt del sub-agente como `## Project Standards (auto-resolved)`.

### java-springboot  → C-01, C-02, C-03, C-04, C-05, C-05b, C-06, C-08
- Inyección **por constructor**; campos de dependencia `private final`.
- Estereotipos correctos: `@RestController` (web), `@Service` (lógica), `@Repository` (persistencia).
- **DTOs** en `api/dto`; NUNCA exponer entidades JPA al cliente.
- Validación con Bean Validation (`@Valid`, `@NotNull`, `@Size`) sobre DTOs.
- Manejo de errores global con `@ControllerAdvice` + `@ExceptionHandler` (respuestas consistentes).
- `@Transactional` en métodos de servicio, al nivel más granular posible; servicios **stateless**.
- Spring Data JPA: extender `JpaRepository`; proyecciones DTO para lecturas parciales.
- Config en `application.yml` + perfiles (`test`/`prod`); `@ConfigurationProperties` para type-safe; **sin secretos hardcodeados** (env vars).
- Logging SLF4J con mensajes parametrizados.
- Tests: `@SpringBootTest` (integración), `@WebMvcTest` (controllers), `@DataJpaTest` (repos).
- **Nota de conflicto:** la skill sugiere organizar por **feature/dominio**, pero el proyecto exige **hexagonal por capa** (`domain/application/infrastructure`). Prevalecen las convenciones del proyecto (§Convenciones 4).

### java-junit  → C-06 ★, C-02
- JUnit 5 puro; tests en `src/test/java`; `mvn test`.
- Clases de test con sufijo `Test`; patrón Arrange-Act-Assert (AAA).
- Naming: `methodName_should_expectedBehavior_when_scenario`.
- Un comportamiento por test; tests independientes e idempotentes (sin interdependencias).
- Parametrizados: `@ParameterizedTest` + `@ValueSource`/`@MethodSource`/`@CsvSource`/`@EnumSource`.
- Assertions con AssertJ (`assertThat(...).is...`) o `Assertions`; `assertThrows` para excepciones; `assertAll` para agrupar.
- Mockito con `@Mock`/`@InjectMocks` sobre interfaces.
- **Para C-06**: los tests de dominio de la regla `RecursoDoble`/`AntiSolapamiento` son **sin contexto Spring** (JUnit + AssertJ puro). Test parametrizado obligatorio de duración por prestación (RN-02) y límite `fin(A)==inicio(B)` permitido vs `-1min` rechazado (RN-03/RN-13).

### postgresql-table-design  → C-02, C-13
- PK en tablas de referencia: `BIGINT GENERATED ALWAYS AS IDENTITY` (UUID sólo si se necesita opacidad).
- Normalizar a 3NF primero; desnormalizar sólo por performance medida.
- `NOT NULL` donde corresponda + `DEFAULT` para valores comunes.
- **Indexar FKs manualmente** (PostgreSQL NO las indexa solo).
- Tipos: `TIMESTAMPTZ` (eventos), `NUMERIC` (dinero), `TEXT` (strings), `BIGINT` (enteros); evitar `timestamp`, `varchar(n)`, `money`, `serial`.
- **EXCLUDE**: previene solapamientos con operadores — `EXCLUDE USING gist (recurso_id WITH =, franja WITH &&)` exige un tipo GiST-capable (`tsrange`). Base directa del constraint de C-13.
- `GiST` para rangos / constraints de exclusión; `GIN` para JSONB/arrays; B-tree para igualdad/rango.
- UNIQUE permite múltiples NULL; usar `UNIQUE NULLS NOT DISTINCT` (PG15+) si se quiere uno solo.
- Overflows de longitud/precisión **erroran** (no truncan).

---

## Convenciones del proyecto (reemplazan a las skills inexistentes)

Los 6 gaps de `find_skill.gaps_sin_candidata` no tienen skill candidata; se cubren con convención + puntero a la KB. Un agente DEBE respetarlas sin ayuda de ninguna skill.

| # | Change(s) | Convención | Dónde vive |
|---|-----------|-----------|------------|
| 1 | C-13 | Constraint `EXCLUDE USING gist (profesional_id WITH =, tsrange(inicio,fin,'[)') WITH &&) WHERE (estado IN ('PENDIENTE','CONFIRMADO'))` + análogo para `sillon_id`; extensión `btree_gist`; traducir SQLSTATE `23P01` a **`409 Conflict`** | `knowledge-base/08_arquitectura_propuesta.md` §Manejo de concurrencia · `knowledge-base/09_decisiones_y_supuestos.md` DD-06, DD-08 |
| 2 | C-13 | Tests del constraint con **Testcontainers PostgreSQL** — H2 **no** soporta `EXCLUDE USING gist`; los tests de doble reserva exigen un PostgreSQL real | `knowledge-base/08_arquitectura_propuesta.md` §Manejo de concurrencia · CHANGES.md C-13 |
| 3 | C-13 | Locking pesimista (adoptivo `SELECT ... FOR UPDATE` por `(recursoId, fecha)`) + optimista (`@Version` en `Turno`); traducir `OptimisticLockException` a error de dominio controlado (**no** excepción cruda de base) | `knowledge-base/08_arquitectura_propuesta.md` §Manejo de concurrencia |
| 4 | C-01, C-02 | Arquitectura **hexagonal limpia** por capa: `domain/model`, `domain/rule`, `domain/exception`, `domain/port`, `application/service`, `application/dto`, `infrastructure/{persistence,scheduler}`, `api/{controller,dto,security}`; **el dominio no depende de frameworks** | `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios / §Patrones |
| 5 | C-01 | Guardrail de CI para datos sintéticos (**RN-06**): check en GitHub Actions sobre seeds/fixtures — dominios `@example.test`, documentos `0000000X`; prohibido versionar datos sensibles reales | `knowledge-base/05_reglas_de_negocio.md` §RN-06 · CHANGES.md C-01 |
| 6 | C-17, C-18, C-19 | Integraciones externas (WhatsApp Business API, Mercado Pago, Google Calendar) **fuera del MVP**; reevaluar en Fase 4 | `knowledge-base/02_descripcion_general.md` §Integraciones externas · `knowledge-base/10_preguntas_abiertas.md` |

---

## Cómo usarlo — dado el change X, cargar estas reglas

| Change | Skills a inyectar | Convenciones a inyectar |
|--------|-------------------|-------------------------|
| C-01 | `java-springboot` | 4 (hexagonal), 5 (guardrail CI / RN-06) |
| C-02 | `java-springboot`, `java-junit`, `postgresql-table-design` | 4 (hexagonal) |
| C-03 | `java-springboot` | — |
| C-04 | `java-springboot` | — |
| C-05 | `java-springboot` | — |
| C-05b | `java-springboot` | 5 (RN-06, datos sintéticos) |
| **C-06 ★** | `java-springboot`, **`java-junit`** | — |
| C-07 | `java-springboot` | — |
| C-08 | `java-springboot` | — |
| C-09 | `java-springboot` | — |
| C-10 | `java-springboot` | — |
| C-11 | `java-springboot` | — |
| C-12 | `java-springboot` | — |
| C-13 | `java-springboot`, `postgresql-table-design` | **1, 2, 3** (constraint GiST + Testcontainers + locking) |
| C-14 | `java-springboot` | — |
| C-15 | `java-springboot` | — |
| C-16 | `java-springboot` | 5 (RN-06 / RN-LG) |
| C-17 | `java-springboot` | 6 (fuera del MVP) |
| C-18 | `java-springboot` | 6 (fuera del MVP) |
| C-19 | `java-springboot` | 6 (fuera del MVP) |
| Todos | `openspec-propose` / `openspec-apply-change` / `openspec-archive-change` (infra) | — |

> Recordar el gotcha: si las skills de dominio no están cargadas (sin reinicio), usar las reglas compactas de §Skills de dominio directamente en el prompt.
