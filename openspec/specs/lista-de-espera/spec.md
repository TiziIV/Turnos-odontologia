# lista-de-espera Specification

## Purpose

Anotar una espera no crea un turno. Al asignar, entra solo la primera espera que pasa la regla de solapamiento. Las demás siguen en la lista.

## Requirements

### Requirement: Asignar la primera espera compatible

El sistema SHALL anotar esperas sin crear turnos y MUST crear un turno solo para la primera espera cuyo hueco esté libre.

#### Scenario: Anotar no ocupa la agenda
- **GIVEN** ya hay un turno a las 9:00
- **WHEN** se anota una espera a las 9:15 con el mismo profesional
- **THEN** la respuesta dice que no se creó un turno y la agenda sigue con un solo turno

#### Scenario: La primera que entra
- **GIVEN** esa espera que se pisa y otra espera a la misma hora con profesional 2 y sillón 2 libres
- **WHEN** se asigna
- **THEN** se crea el turno del profesional 2 y la espera que se pisaba sigue en la lista

#### Scenario: Ninguna entra
- **GIVEN** todas las esperas chocan con turnos activos
- **WHEN** se asigna
- **THEN** se devuelve 409 y la lista no pierde esas esperas
