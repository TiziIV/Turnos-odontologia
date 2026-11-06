# Tasks

## 1. Pantalla

- [x] 1.1 Dejar en `/panel/` la tabla del catálogo, los campos de día y hora, y la agenda en hora Argentina. Verificar que `GET /panel/` incluye esos textos.

## 2. Prueba y documentación

- [x] 2.1 Cubrir con pytest el alta válida, el rechazo por solapamiento de profesional, de sillón y de los dos, el borde de las 09:30 y el recurso inactivo. Verificar que `python -m pytest tests/api/test_tpi.py` pasa.
- [x] 2.2 Documentar en `README.md` y en `CHANGES.md` como C-25 cómo se elige la hora en el panel. Verificar que ambos archivos nombran el día, la hora y la hora Argentina.

## Workflow follow-up

- Archivar `panel-legible` y sincronizar `openspec/specs/panel/spec.md`.
