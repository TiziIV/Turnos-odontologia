# Ajuste del stack a Python/FastAPI

Fecha: 2026-10-15. Estado: corrección documental autorizada; no es un change OPSX implementado.

## Origen y autorización

La indicación docente del **2026-10-01** en el chat de metodología aportado por Juan requiere Python/FastAPI. El **2026-10-15**, ante la discrepancia con el repositorio, Juan confirmó: «Debemos usar Python/FastAPI» y autorizó ajustar la fundación: «Si ajustemos eso, cumplamos con todo lo q pida».

El chat original es fuente externa de la entrega; no se copia íntegro al repositorio porque contiene conversaciones de terceros. Esta nota registra la corrección confirmada por el usuario, sin atribuir una nueva autorización al docente.

## Antes y después

| Aspecto | Fundación anterior | Decisión vigente |
|---|---|---|
| Lenguaje/API | Java 21 / Spring Boot 3 | Python 3.12+ / FastAPI |
| DTOs | Bean Validation | Pydantic en API |
| Persistencia | JPA | SQLAlchemy en infraestructura |
| Migraciones | Flyway | Alembic |
| Tests | JUnit / AssertJ / Mockito; H2 | pytest con fakes unitarios; PostgreSQL real para integración/concurrencia |
| Proyecto/comando | Maven, `mvn test` | `pyproject.toml`, entorno virtual, `python -m pytest` |
| Base | PostgreSQL | PostgreSQL, sin cambio de garantía prevista |

JWT, Redis cuando corresponda y Docker/Compose forman parte del contexto objetivo. React/TypeScript/Vite corresponde a un posible cliente futuro, fuera del change backend. Las versiones finales de dependencias se fijarán al implementar: esta nota no afirma instalaciones ni código ejecutable existente.

## Alcance de la corrección

Se actualizan las secciones técnicas de KB, CHANGES.md, AGENTS.md/CLAUDE.md, registro de skills y estado de la fundación. Permanecen las reglas de recurso doble, duración por prestación, intervalo semiabierto y arquitectura hexagonal pura. Los nombres del contrato de dominio/API no se migran por sustitución de lenguaje.

Se conserva el informe de Discovery y sus evidencias originales. La elección e instalación de skills Java queda como historial, marcada obsoleta; no se inventa la instalación de skills Python. Este ajuste no implementa código, no crea ni archiva changes y no acredita el uso de Ajustar en Propose. Esas evidencias deben capturarse durante su ejecución real.

## Entrega única y excepción de dependencias aprobada

El 2026-10-15, tras aclarar la diferencia entre comenzar por C-01 y entregar un solo change, Juan respondió «Dale», «Implementenmos esto» y «perfecto sigamos». Se registra así la aprobación de **C-06 crear-turno-anti-solapamiento como primer change entregado**, conservando su ID histórico. Esta aprobación autoriza el alcance; no certifica implementación, pruebas ni capturas realizadas.

La entrega incluye base mínima de API FastAPI, dominio/modelos/puertos, datos ficticios y pytest. La demo local emplea repositorios en memoria, con pérdida de datos al reiniciar y sin garantía de concurrencia PostgreSQL. SQLAlchemy/PostgreSQL/Alembic permanecen como diseño futuro cuando no estén implementados. CRUDs completos, login/RBAC e integraciones quedan para después.

Para esta entrega no se exige archivar previamente C-01/C-02 ni C-03/C-04/C-05/C-05b: sólo su base imprescindible se incorpora al alcance de C-06. Esos IDs continúan pendientes como capacidades completas; no se marcan completados ni se crean archives ficticios. El árbol y camino crítico de CHANGES.md describen el producto completo, mientras la excepción permite el único change académico. Explore/Propose debe reflejar los límites antes de Apply.

Las preguntas de dominio siguen abiertas en KB 10. También debe acordarse la política temporal antes de fijar tipos SQL y rangos (`tsrange` o `tstzrange`).

## Límite de las pruebas

Los tests de pytest con fakes verifican la lógica secuencial (camino feliz, solapamiento, inicio igual al fin anterior). No demuestran transacciones, bloqueo, constraint de exclusión ni RN-16. Esa garantía necesita PostgreSQL real y pruebas de concurrencia/integración, previstas en C-13. Ninguna prueba se ejecuta ni se declara aprobada por esta corrección documental.
