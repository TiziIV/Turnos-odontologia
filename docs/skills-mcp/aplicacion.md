# Informe de aplicación — skill y MCP

Fecha: 5 de noviembre de 2026.

## Qué se pidió

Preparar `lista-de-espera` con la skill `revisar-escenarios-turno` y consultar cómo FastAPI devuelve HTML, que es lo que después usa el panel.

## Qué devolvió y qué aportó

La skill obliga tres escenarios y el borde del intervalo. Con eso la spec de la espera distingue anotar (no crea turno), asignar la primera que no choca, y dejar en la lista a la que sí choca. Esos tres casos están en `tests/api/test_tpi.py`.

Context7 se eligió para no inventar la forma de publicar una página. La configuración sin secretos está en `docs/skills-mcp/mcp.example.json`. El 5 de noviembre de 2026 se llamó a la herramienta `resolve-library-id` con la biblioteca FastAPI y después a `query-docs` con el id `/websites/fastapi_tiangolo`. La documentación oficial dice que una ruta puede devolver HTML con `HTMLResponse` y `response_class=HTMLResponse` (https://fastapi.tiangolo.com/advanced/custom-response/). El panel usa esa forma. El test `test_panel_muestra_las_tres_paginas` comprueba Agenda, Reserva y Espera.

## Antes y después

La primera lectura de la skill pedía un escenario aparte para cuando chocan profesional y sillón a la vez, como si la regla actual no lo cubriera. La regla RN-01 ya rechaza si coincide cualquiera de los dos. Chocar los dos a la vez entra en ese rechazo. No se abrió un change nuevo para repetir la misma regla. El caso que sí faltaba, y que la skill ayudó a no mezclar, es la espera: anotar no crea turno.

## Archivos

| Archivo | Por qué |
|---|---|
| `skills/revisar-escenarios-turno/SKILL.md` | Skill propia versionada |
| `.atl/skill-registry.md` | Registro para que el agente la encuentre |
| `AGENTS.md` y `CLAUDE.md` | Cuándo usarla y el límite del MCP |
| `docs/skills-mcp/mcp.example.json` | Configuración reproducible sin claves |
| `src/turnos/application/service/agenda.py` | Espera, enlace y estados |
| `src/turnos/api/panel/panel.html` | Pantalla de lo ya implementado |
| `tests/api/test_tpi.py` | Escenarios de los changes nuevos |

## Límite

No se afirma una llamada en vivo a Context7 en esta sesión. La conexión queda documentada para reproducirla en Cursor. Las capturas de pantalla las tiene que sacar el equipo: esta carpeta no incluye imágenes fabricadas.
