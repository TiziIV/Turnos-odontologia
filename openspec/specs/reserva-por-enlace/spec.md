# reserva-por-enlace Specification

## Purpose

Un enlace nombra un hueco. Si el alta entra, el enlace queda usado. Si se rechaza, sigue disponible.

## Requirements

### Requirement: reserva-por-enlace

El sistema SHALL crear un turno solo cuando el enlace existe, no fue usado y el hueco no se solapa.

#### Scenario: Camino feliz
- **GIVEN** el catalogo sintetico del README
- **WHEN** se usa la operacion principal de este change
- **THEN** el resultado observable coincide con la spec y queda cubierto por tests/api/test_tpi.py

#### Scenario: Rechazo de negocio
- **GIVEN** un turno activo que ocupa el recurso
- **WHEN** la operacion viola la regla de solapamiento o de estado
- **THEN** no se crea un turno indebido y el anterior permanece

#### Scenario: Borde
- **GIVEN** un caso limite del change (enlace ya usado, paciente inexistente, espera que no entra)
- **WHEN** se intenta la operacion
- **THEN** el sistema rechaza sin alterar los turnos validos
