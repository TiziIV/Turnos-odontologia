# Design

## Context

Ver motivación en proposal.md. La raíz OpenSpec fue confirmada por CLI y no tenía changes ni specs. La fundación contiene KB, roadmap e instrucciones, pero no código Python ni pyproject. CHANGES.md autoriza la excepción académica para C-06 sin completar previamente todos sus prerrequisitos. Python 3.13 está disponible; no se pudo acceder al daemon Docker y psql no está en PATH. Esos hechos no constituyen instalación ni prueba de PostgreSQL.

## Goals / Non-Goals

**Goals:** separar reglas puras, caso de uso, almacenamiento y frontera HTTP; cubrir el contrato de `specs/reserva-turnos/spec.md` mediante tests de dominio, aplicación y API, reproducibles sin base de datos.

**Non-Goals:** login o autenticación; persistencia PostgreSQL (ni SQLAlchemy/Alembic); endpoints o transiciones de cancelación; demostrar RN-16; imponer horarios RN-14; construir todos los modelos y puertos futuros. El Ajustar del 2026-10-15 cierra estas exclusiones para Apply. El alcance exacto se fija en proposal.md.

## Decisions

1. **Capas mínimas.** `src/turnos/domain/{model,rule,exception,port}`, `application/{service,dto}`, `infrastructure/` y `api/{controller,dto}` según KB08. Dataclasses/enums y puertos con tipos estándar en dominio; Pydantic sólo en API. Alternativa descartada: modelos Pydantic usados directamente como entidades, que acoplarían los tests puros al framework.
2. **Repositorio en memoria por instancia.** Una factoría de aplicación compone catálogos sintéticos y repositorio vacío de turnos; cada test obtiene una instancia aislada. El caso de uso resuelve referencias, calcula fin, valida ocupación y sólo entonces guarda. IDs enteros positivos generados por repositorio. No se agrega unidad de trabajo ficticia ni se promete atomicidad concurrente. PostgreSQL permanece como adaptador futuro: SQLite no demostraría su constraint.
3. **Intersección estricta.** Para un turno activo A y candidato B: `(A.profesionalId == B.profesionalId OR A.sillonId == B.sillonId) AND A.inicio < B.fin AND B.inicio < A.fin`. Comparar contra todos los activos; excluir CANCELADO/REALIZADO/AUSENTE. Capturar ambos bordes, contención y recursos independientes en tests. No basta verificar si el inicio cae dentro del otro turno.
4. **Contrato HTTP.** Sólo `POST /api/public/turnos`, ya público en KB03. DTO de entrada camelCase con los cinco campos de la spec, IDs estrictamente enteros positivos y campos adicionales prohibidos. Respuesta 201 con `id`, referencias, `inicio`, `fin`, `estado` y `canal`. Error de conflicto: `{"detail":{"codigo":"TURNO_SOLAPADO","mensaje":"El profesional o el sillón no está disponible en esa franja."}}`. Referencias inexistentes o inactivas se traducen a 422 con error controlado; validación de DTO usa 422 de FastAPI. No devolver datos del otro paciente. Alternativa descartada: habilitar `/api/turnos` sin autenticación, porque KB03 reserva esa ruta al personal. El flujo de mostrador del scope completo C-06 queda aplazado por la excepción académica.
5. **Tiempo explícito (confirmado en Ajustar 2026-10-15).** Exigir ISO 8601 con offset/Z y normalizar a UTC; rechazar datetimes naive en frontera y dominio. Evita depender de la zona del equipo al comparar. No se elige todavía `tsrange`/`tstzrange`: IN-08 sigue abierto para persistencia futura, que este change no implementa. No imponer fecha futura ni horario de atención, porque no están definidos en este change.
6. **Duración y estado.** Prestaciones sintéticas de KB04: CONSULTA 20, LIMPIEZA 30, EXTRACCION 40, ENDO 60 minutos. Mantener enum de cinco estados por RN-07; creación siempre PENDIENTE/ONLINE. Rechazar fin, duración, estado o canal proporcionados por cliente. Fixtures pueden contener estados finales únicamente para probar RN-09.
7. **Verificación.** TDD por bloques: escribir tests que fallen por comportamiento ausente, registrar esa ejecución real, implementar lo mínimo, ejecutar tests y refactorizar. Tests puros en `tests/domain`, aplicación con fakes en `tests/application`, cliente HTTP en `tests/api`. Guardar matriz escenario → test; nombres citan RN correspondientes. Verificar convenciones sintéticas mediante tests y revisión, sin afirmar que un patrón de email garantiza por sí solo procedencia ficticia.

## Risks / Trade-offs

- Memoria pierde datos y no coordina procesos → README y ejecución limitada a `127.0.0.1`, un proceso, demostración secuencial; RN-16 requiere C-13 y PostgreSQL real.
- Reserva pública por ID no verifica identidad → sólo datos ficticios locales; autenticación/identidad quedan pendientes antes de uso real.
- El roadmap del producto es más amplio → conservar C-06 y explicitar su entrega parcial respecto del producto, sin marcar CRUDs ni auth completados.
- Ejemplos temporales naive de KB04 → usar offset explícito en ejemplos nuevos según la política UTC confirmada; no reinterpretar automáticamente datos históricos ni migraciones inexistentes.
- Preguntas altas sobre seña/WhatsApp → no bloquean este alcance: turno PENDIENTE sin confirmación, pagos ni recordatorios. Siguen abiertas para esos flujos.

## Migration Plan

No hay datos ni esquema que migrar. El Ajustar de Propose quedó registrado el 2026-10-15; Apply puede crear venv, fijar dependencias compatibles en pyproject y archivo reproducible, instalar y ejecutar `python -m pytest`. Arrancar Uvicorn en `127.0.0.1` con un worker y documentar ejemplos PowerShell. El README debe indicar que reiniciar elimina reservas; revertir esta implementación no requiere migración de datos. El CI ejecutará tests con una versión Python soportada, sin servicios externos. Versiones concretas se fijarán durante Apply según instalación comprobada.
