# Proposal

## Why

La fundación describe el problema de reservar simultáneamente profesional y sillón, pero todavía no tiene código ejecutable. Elegimos este change porque prueba el núcleo de valor con tres resultados observables (reserva válida, rechazo de solapamiento y encadenado exacto) y permite defender la trazabilidad entre reglas, especificación y tests en una única entrega.

## What Changes

- Implementar la primera entrega académica de `C-06 crear-turno-anti-solapamiento`, conservando su ID histórico. Incorporar la base mínima autorizada en CHANGES.md, sin declarar terminados los changes previos.
- Crear una API Python 3.12+/FastAPI con `POST /api/public/turnos`: referencias a paciente, profesional, sillón y prestación, más inicio con zona horaria; fin calculado por prestación; estado inicial PENDIENTE y canal ONLINE.
- Validar ambos recursos y prestaciones activos, referencias existentes, duración positiva e intervalos semiabiertos. Rechazar conflicto por cualquiera de los dos recursos con HTTP 409; crear con 201; validar entradas con 422.
- **Ajustar 2026-10-15 (Juan Martín García):** contrato cerrado. Los tres escenarios DADO/CUANDO/ENTONCES de demostración quedan fijos: reserva válida; rechazo por solapamiento de profesional o sillón; borde inicio igual al fin anterior. `inicio` MUST ser ISO 8601 con zona (offset o Z) y las comparaciones MUST hacerse en UTC. No se agrega login, PostgreSQL ni cancelación. La captura del pedido y de esta respuesta sigue a cargo de Juan en `docs/evidencias/`.
- Incorporar dominio puro, puertos y adaptador en memoria, catálogos sintéticos, pytest, CI básico y README reproducible para demo local secuencial.
- Fuera de alcance (reafirmado en el Ajustar): login/auth/RBAC, PostgreSQL/SQLAlchemy/Alembic, endpoints de cancelación, CRUDs, ruta privada de mostrador, disponibilidad, reprogramar, recordatorios, pagos e integraciones, RN-14, persistencia durable y garantía concurrente RN-16.

## Capabilities

### New Capabilities

- `reserva-turnos`: creación de una reserva de invitado con duración derivada y disponibilidad conjunta de profesional y sillón.

### Modified Capabilities

Ninguna: `openspec list --specs` no devuelve capacidades existentes.

## Impact

Se crearán `src/turnos/`, `tests/`, `pyproject.toml`, configuración CI y comandos de instalación/ejecución en README. Se fijarán dependencias compatibles de FastAPI, Pydantic, Uvicorn, pytest y cliente HTTP de tests al implementar. La demo escuchará en `127.0.0.1`, con un proceso y datos que se pierden al reiniciar; no se presenta como servicio de producción. Reglas cubiertas: RN-01/02/03/06/09/10/11/13; RN-07 sólo enum e inicialización, sin transiciones. La exclusión de estados finales verifica RN-09, no completa el flujo de cancelación RN-04. Explore se conserva en `docs/opsx/explore-crear-turno-anti-solapamiento.md`.
