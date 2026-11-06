# Design

## Context

`/panel/` ya sirve Agenda, Reserva y Espera. El alta sigue en `POST /api/public/turnos` y serializa `inicio` y `fin` en UTC. Ver `proposal.md`.

## Goals / Non-Goals

**Goals:**

- Que la pantalla se entienda sin abrir el README ni Swagger.
- Conservar el contrato de la API: `inicio` con zona, fin derivado de la prestación.

**Non-Goals:**

- No se cambia el JSON de los endpoints.
- No se agregan login, PostgreSQL ni un selector de huso horario.

## Decisions

- El catálogo visible repite los identificadores sintéticos ya cargados en memoria. No se agrega un endpoint de catálogo: la demostración tiene seis pacientes, profesionales, sillones y prestaciones fijos.
- Día y hora son controles nativos. El navegador arma `YYYY-MM-DDTHH:MM:SS-03:00` antes de llamar al alta. Argentina se fija en `-03:00` porque el consultorio de la demo está en ese huso.
- La agenda formatea en el navegador con `America/Argentina/Buenos_Aires`. El backend sigue respondiendo UTC, así Swagger y los tests HTTP no cambian de formato.
- Los textos de rechazo del panel citan el `mensaje` que ya devuelve el dominio. El test comprueba que la frase del HTML y la de la API son la misma.

## Risks / Trade-offs

- [El catálogo de la pantalla puede desfasarse del seed] → el test exige los nombres Carla Pérez y Eva Sosa, que salen de `catalogos.py`.
- [Un navegador sin calendario muestra igual los campos de fecha y hora] → el valor inicial sigue siendo 2 de noviembre de 2026, 09:00.
