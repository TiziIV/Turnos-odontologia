# ficha-minima Specification

## Purpose

La ficha mínima es el paciente sintético que ya existe. No se crea otro identificador de persona.

## Requirements

### Requirement: Leer la ficha del paciente existente

El sistema SHALL devolver `GET /api/pacientes/{id}` con los datos sintéticos ya cargados y MUST NOT incluir datos clínicos.

#### Scenario: Paciente del catálogo
- **GIVEN** el paciente 1 del README, documento `00000001` y correo `@example.test`
- **WHEN** se pide `GET /api/pacientes/1`
- **THEN** se devuelve 200 con ese documento y ese correo, sin campo de diagnóstico

#### Scenario: Paciente inexistente
- **GIVEN** no existe el paciente 99
- **WHEN** se pide `GET /api/pacientes/99`
- **THEN** se devuelve 404 y no se crea un paciente

#### Scenario: El turno sigue usando ese mismo id
- **GIVEN** la ficha del paciente 1
- **WHEN** se crea un turno público con `pacienteId` 1
- **THEN** el turno referencia ese paciente y no aparece un segundo modelo de ficha
