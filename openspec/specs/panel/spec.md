# panel Specification

## Purpose

Mostrar en una pantalla solo lo que el backend ya hace: agenda, reserva y espera.

## Requirements

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

### Requirement: Catálogo visible en la pantalla

`GET /panel/` SHALL mostrar el catálogo sintético con el número, el nombre y si se puede usar. SHALL decir que un número ausente, como el paciente 5, no existe.

#### Scenario: La tabla nombra lo que se puede usar
- **GIVEN** la API de demostración en marcha
- **WHEN** se abre `/panel/`
- **THEN** el HTML nombra a Carla Pérez como usable y a Eva Sosa como inactiva

### Requirement: Día y hora de Argentina

Los formularios de Reserva y Espera SHALL pedir el día y la hora por separado. SHALL armar el `inicio` con zona `-03:00`. SHALL NOT pedir el fin: la duración sigue saliendo de la prestación (RN-02).

#### Scenario: Se elige el día y la hora
- **GIVEN** la página Reserva
- **WHEN** se mira el formulario
- **THEN** hay un campo de fecha y un campo de hora, y el HTML explica que 09:00 de una limpieza termina a las 09:30

### Requirement: Agenda en hora Argentina

La agenda SHALL mostrar paciente, profesional, sillón, prestación y estado con sus nombres. SHALL mostrar el intervalo en hora de Argentina, no en UTC crudo.

#### Scenario: El turno se lee sin identificadores sueltos
- **GIVEN** la página Agenda
- **WHEN** se carga el HTML
- **THEN** el HTML convierte la hora con `America/Argentina/Buenos_Aires` y nombra el estado Pendiente

### Requirement: Rechazo y borde explicados

La pantalla SHALL explicar el rechazo de un recurso inactivo y el borde en que el turno siguiente empieza cuando termina el anterior (RN-03). Un choque de profesional, de sillón o de los dos SHALL seguir siendo un rechazo del alta ya existente (RN-01). La pantalla SHALL NOT crear una regla nueva.

#### Scenario: Reserva válida
- **GIVEN** un profesional y un sillón libres
- **WHEN** se crea una limpieza a las 09:00
- **THEN** el alta responde 201 y el fin es 09:30 en hora Argentina

#### Scenario: Rechazo por solapamiento
- **GIVEN** una limpieza de 09:00 a 09:30
- **WHEN** otro turno usa el mismo profesional, el mismo sillón o los dos, y empieza a las 09:15
- **THEN** el alta responde 409

#### Scenario: Borde de encadenado
- **GIVEN** una limpieza que termina a las 09:30
- **WHEN** otro turno con los mismos recursos empieza a las 09:30
- **THEN** el alta responde 201 y el HTML del panel dice que ese encadenado se puede

#### Scenario: Recurso inactivo
- **GIVEN** la profesional 3, Eva Sosa
- **WHEN** se intenta reservar con ella
- **THEN** el alta responde 422 con el mensaje `El profesional no está activo.` y ese mismo mensaje está en el HTML del panel
