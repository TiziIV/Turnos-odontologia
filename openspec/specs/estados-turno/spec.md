# estados-turno Specification

## Purpose

Confirmar deja el horario ocupado. Cancelar lo libera. Reprogramar vuelve a validar profesional y sillón sin contar el turno que se mueve. Si el destino se rechaza, el original no cambia.

## Requirements

### Requirement: Confirmar, cancelar y reprogramar

El sistema SHALL aceptar confirmar un pendiente y cancelar un pendiente o confirmado, y MUST conservar el turno original si la reprogramación choca.

#### Scenario: Confirmar sigue ocupando
- **GIVEN** un turno pendiente de 9:00 a 9:30 con profesional 1
- **WHEN** se confirma y otro turno pide las 9:10 con ese profesional
- **THEN** el primero queda CONFIRMADO y el segundo recibe 409

#### Scenario: Cancelar libera
- **GIVEN** ese turno confirmado
- **WHEN** se cancela
- **THEN** queda CANCELADO y otra reserva en la misma franja y recursos recibe 201

#### Scenario: Destino ocupado
- **GIVEN** el turno original a las 9:00 y otro turno de profesional 2 y sillón 2 a las 11:00
- **WHEN** se reprograma el original a las 11:00 con profesional 2 y sillón 2
- **THEN** se devuelve 409 y el inicio del original sigue siendo las 12:00 UTC
