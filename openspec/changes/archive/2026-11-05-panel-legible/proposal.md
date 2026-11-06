# Proposal

## Why

En `/panel/` la persona tenía que adivinar los números del catálogo, leer la agenda en UTC y escribir el inicio como `2026-11-02T09:00:00-03:00`. Para la demostración, la pantalla tiene que decir qué número es cada cosa, mostrar el turno en hora Argentina y dejar elegir el día y la hora.

## What Changes

- La pantalla muestra una tabla del catálogo sintético: número, nombre y si se puede usar.
- Reserva y Espera eligen paciente, profesional, sillón y prestación por nombre. Las opciones inactivas dicen que se rechazan.
- El inicio se elige con día y hora de Argentina. El formulario arma `inicio` con zona `-03:00`. El fin sigue saliendo de la prestación.
- La agenda muestra paciente, profesional, sillón, prestación, estado y el intervalo en hora Argentina.
- Si el alta se rechaza, el mensaje nombra qué número usar.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `panel`: la pantalla explica el catálogo, el horario local y el borde de encadenado. No cambia el alta pública ni las reglas RN-01, RN-02 y RN-03.

## Impact

- `src/turnos/api/panel.html`
- `tests/api/test_tpi.py`
- `README.md` y `CHANGES.md`
- La API sigue recibiendo `inicio` en ISO 8601 con zona. Swagger no cambia.
