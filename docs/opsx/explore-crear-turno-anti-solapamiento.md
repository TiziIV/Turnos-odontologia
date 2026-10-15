# Explore — crear-turno-anti-solapamiento

Fecha: 2026-10-15. Resumen de exploración del repositorio antes de implementar. Este documento registra hallazgos y decisiones propuestas; no acredita Apply, tests aprobados, Ajustar humano, Archive ni capturas.

## Problema y alcance

El turno ocupa dos recursos simultáneos: profesional y sillón. La duración depende de la prestación; el encadenado exacto está permitido. Juan confirmó Python/FastAPI y aprobó que C-06 sea la primera entrega ejecutable, con base mínima incluida. Se conserva su ID histórico; el resto del roadmap no se da por terminado.

## Observaciones verificadas

- La raíz OpenSpec fue resuelta por `openspec context --json` y `openspec list --json`; no había changes activos ni specs. `openspec/config.yaml` define schema spec-driven, textos en español y encabezados estructurales en inglés.
- La fundación incluye `knowledge-base/`, `CHANGES.md`, `AGENTS.md`, skills OPSX y evidencias previas. Antes de este change no hay código Python ni pyproject en el proyecto.
- KB03 distingue `/api/public/turnos` (invitado) de `/api/turnos` (personal autenticado). La demo usará sólo la primera; mostrador y auth quedan pendientes.
- KB04 define prestaciones 20/30/40/60 minutos. KB05 fija RN-01/02/03, estados ocupantes RN-09 y actividad RN-10/11. Los ejemplos de borde deben compartir recurso; cambiar ambos recursos no demuestra el límite de RN-03.
- KB08 exige dominio sin framework y advierte que fakes no prueban PostgreSQL ni RN-16. Python 3.13 está disponible, pero Docker no tiene daemon accesible y psql no está en PATH. No se ejecutaron tests de integración.
- Se consultó la versión anterior del usuario `https://github.com/juanmagarciat/turnos-odontologia`, clon hermano `referencia-juan`, commit `f1ced04`. Usa TypeScript/Node y contiene cuatro tests. Sirve como referencia conceptual del predicado estricto y de conflictos por profesional/sillón; no se copiaron evidencias ni se presentan sus tests como ejecutados aquí.

## Regla a demostrar

Existe conflicto cuando se comparte profesional O sillón y `inicio(A) < fin(B)` Y `inicio(B) < fin(A)`, considerando sólo PENDIENTE/CONFIRMADO. La desigualdad estricta permite `fin(A) == inicio(B)`. Un rechazo no agrega ni altera reservas.

## Opciones y decisión propuesta

Se propone dominio puro + FastAPI/Pydantic en frontera + repositorio en memoria aislado por instancia. Permite verificar el comportamiento secuencial sin asumir una base instalada. PostgreSQL/SQLAlchemy/Alembic, constraints y pruebas simultáneas siguen en roadmap; SQLite tampoco demostraría las garantías PostgreSQL.

La demo tendrá sólo reservas públicas sobre catálogos sintéticos, estado inicial PENDIENTE, canal ONLINE y fin calculado. Política temporal confirmada en Ajustar 2026-10-15: ISO 8601 con zona obligatoria y UTC interno; tipos SQL siguen pendientes porque no hay PostgreSQL en este change. No se implementan login, PostgreSQL, cancelación, RN-14, recordatorios, pagos, reprogramación, CRUDs ni seguridad completa.

## Riesgos y pendientes de revisión

- Memoria se pierde al reiniciar y no garantiza concurrencia multiproceso: ejecución local, un proceso, datos ficticios y pruebas secuenciales.
- El ID público de paciente no verifica identidad: se trata de demo sintética, no despliegue real.
- Preguntas sobre WhatsApp/seña siguen abiertas para flujos posteriores; PENDIENTE no equivale a confirmación de pago.
- Ajustar de Propose registrado el 2026-10-15 (pedido de Juan: tres escenarios, UTC, sin login/PostgreSQL/cancelación). Captura en `docs/evidencias/etapa-6-propose-ajustar.png`. Sigue Apply.

## Salida

Se eligió `crear-turno-anti-solapamiento` por cubrir el núcleo de valor y permitir evidencia trazable en un único change. La planificación se encuentra en `openspec/changes/crear-turno-anti-solapamiento/`: proposal, design, spec de reserva-turnos y tasks. Su presencia no implica código implementado ni entrega terminada.
