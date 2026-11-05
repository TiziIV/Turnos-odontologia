# Ficha de investigación — skill y MCP

Fecha de consulta: 5 de noviembre de 2026. Integrantes: García Juan Martín y Tiziano Valentini.

## Necesidad y change

El change elegido es `lista-de-espera`. Anotar no crea un turno, y al asignar solo entra la primera espera que pasa la misma regla de solapamiento. Hace falta una skill que revise esos escenarios antes de programar, y un MCP para leer la documentación de FastAPI sin inventar cómo se publica una página.

## Skill creadora

Nombre: `skill-creator`. Fuente: [github.com/anthropics/skills/tree/main/skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator), consultada el 5 de noviembre de 2026. Sirve para redactar un `SKILL.md` con propósito, cuándo se activa y cómo revisar el resultado. Está disponible para el agente del equipo.

La skill propia se llama `revisar-escenarios-turno`. Se activa al escribir una spec de agenda. Pide un caso que entra, uno que se rechaza y el borde en que el siguiente empieza cuando el anterior termina. El resultado se contrasta con RN-01, RN-02 y RN-03. Vive en `skills/revisar-escenarios-turno/SKILL.md`.

## Dos MCP

| MCP | Qué aporta | Costo | Elección |
|---|---|---|---|
| Context7 | Documentación actual de librerías, por ejemplo FastAPI | Sin clave en el ejemplo | Elegido: el change necesita servir HTML desde la API |
| Playwright MCP | Manejar un navegador | Sin clave, más pesado para esta tarea | Descartado para preparar la spec; la pantalla se prueba con el cliente HTTP |

Configuración de ejemplo, sin secretos: `docs/skills-mcp/mcp.example.json`.

## Fundación a actualizar

`.atl/skill-registry.md`, `AGENTS.md`, `CLAUDE.md` y `CHANGES.md`. No se rehace el Discovery.

## Fuentes

- https://github.com/anthropics/skills/tree/main/skills/skill-creator — 5 de noviembre de 2026
- https://github.com/upstash/context7 — 5 de noviembre de 2026
- https://github.com/microsoft/playwright-mcp — 5 de noviembre de 2026
