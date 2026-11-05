# Spec Delta

## Purpose

Confirmar sigue ocupando. Cancelar libera. Reprogramar valida de nuevo y, si falla, deja el original.

## ADDED Requirements

### Requirement: estados-turno

El sistema SHALL confirmar, cancelar o reprogramar segun la transicion, y MUST conservar el turno si el destino se rechaza.

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
