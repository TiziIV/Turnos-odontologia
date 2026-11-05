# lista-de-espera Specification

## Purpose

Anotar una espera no crea un turno. Asignar toma la primera que pasa la regla de solapamiento.

## Requirements

### Requirement: lista-de-espera

El sistema SHALL anotar esperas sin crear turnos y MUST asignar solo la primera espera compatible.

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
