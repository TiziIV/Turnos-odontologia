# Ajustar — crear-turno-anti-solapamiento

Fecha: 2026-10-15. Pedido humano de Juan Martín García sobre el Propose ya escrito. No acredita Apply, tests, Archive ni la captura en `docs/evidencias/`.

## Pedido

> Ajustar: dejen en la spec los tres escenarios DADO/CUANDO/ENTONCES (reserva válida, rechazo por solapamiento de profesional o sillón, y borde inicio igual al fin anterior). Confirmo inicio con zona ISO 8601 y comparación en UTC. No agregar login, PostgreSQL ni cancelación.

## Respuesta

Se acepta el pedido. El change permanece `crear-turno-anti-solapamiento`. No se abre un change nuevo: el alcance no cambia de intención, se cierra el contrato para Apply.

| Punto | Decisión |
|---|---|
| Reserva válida | Conservada: escenario `Camino feliz` |
| Rechazo por profesional o sillón | Conservado: escenario `Error por solapamiento de profesional o sillón` |
| Borde inicio = fin anterior | Conservado: escenario `Borde inicio igual al fin anterior` |
| Tiempo | ISO 8601 con offset o Z; comparación y salida en UTC |
| Login | Fuera de Apply |
| PostgreSQL | Fuera de Apply; demo en memoria |
| Cancelación | Fuera de Apply; `CANCELADO` en fixtures solo para RN-09 |

Los escenarios extra de la spec (un minuto de intersección, recursos distintos, duración de catálogo, offsets equivalentes) siguen como apoyo de las mismas reglas. No amplían el producto ni agregan endpoints.

## Archivos tocados

- `openspec/changes/crear-turno-anti-solapamiento/proposal.md`
- `openspec/changes/crear-turno-anti-solapamiento/design.md`
- `openspec/changes/crear-turno-anti-solapamiento/specs/reserva-turnos/spec.md`
- `openspec/changes/crear-turno-anti-solapamiento/tasks.md` (tarea 1.1 de Ajustar textual)
- `docs/opsx/explore-crear-turno-anti-solapamiento.md`

## Captura

Archivo: `docs/evidencias/etapa-6-propose-ajustar.png` (captura real del pedido y de la respuesta, copiada el 2026-10-15).
