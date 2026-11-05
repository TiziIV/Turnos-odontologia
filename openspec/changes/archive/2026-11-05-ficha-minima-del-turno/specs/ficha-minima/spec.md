# Spec Delta

## Purpose

El turno ya referencia un paciente sintetico. La ficha minima es ese paciente, no un segundo identificador.

## ADDED Requirements

### Requirement: ficha-minima

El sistema SHALL devolver la ficha del paciente sintetico existente y MUST NOT incluir datos clinicos.

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
