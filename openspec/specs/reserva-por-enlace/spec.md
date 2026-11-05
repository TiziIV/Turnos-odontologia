# reserva-por-enlace Specification

## Purpose

Un enlace nombra un hueco. Si el alta entra, el turno queda y el enlace queda usado. Si el alta se rechaza, el enlace sigue disponible.

## Requirements

### Requirement: Usar un enlace una sola vez

El sistema SHALL crear el turno al usar un enlace libre y MUST rechazar un enlace inexistente o ya usado sin crear otro turno.

#### Scenario: Enlace libre
- **GIVEN** un enlace para profesional 2 y sillón 2, con ambos libres
- **WHEN** se usa ese enlace
- **THEN** se devuelve 201 y un segundo uso del mismo token devuelve 422

#### Scenario: El hueco está ocupado
- **GIVEN** ya hay un turno de limpieza a las 9:00 con profesional 1 y un enlace a las 9:15 con ese mismo profesional
- **WHEN** se usa el enlace
- **THEN** se devuelve 409 y el enlace sigue sin usar

#### Scenario: Token que no existe
- **GIVEN** no hay un enlace `no-existe`
- **WHEN** se intenta usarlo
- **THEN** se devuelve 422 y no se crea un turno
