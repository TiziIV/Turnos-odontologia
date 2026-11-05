# Spec Delta

## Purpose

Mostrar en una pantalla solo lo que el backend ya hace: agenda, reserva y espera.

## ADDED Requirements

### Requirement: Tres páginas en la misma API

El sistema SHALL servir `GET /panel/` con las secciones Agenda, Reserva y Espera, usando los endpoints ya implementados.

#### Scenario: La pantalla carga
- **GIVEN** la API de demostración en marcha
- **WHEN** se abre `/panel/`
- **THEN** se devuelve 200 y el HTML nombra Agenda, Reserva y Espera

#### Scenario: La reserva usa el alta pública
- **GIVEN** la página Reserva
- **WHEN** se envía el formulario
- **THEN** el navegador llama a `POST /api/public/turnos` y muestra el resultado

#### Scenario: No muestra lo que no existe
- **GIVEN** la pantalla
- **WHEN** se recorren las tres secciones
- **THEN** no hay login, precios ni teléfonos nuevos

