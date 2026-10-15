# Verify — crear-turno-anti-solapamiento

Fecha: 2026-10-15. Entorno: Windows, Python 3.13.7, venv local. No es captura de pantalla ni Archive.

## Comandos

```text
python -m venv .venv
.\.venv\Scripts\pip.exe install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -o addopts=
.\.venv\Scripts\python.exe scripts\check_synthetic.py
```

## Resultado

```text
======================== 74 passed, 1 warning in 0.76s ========================
RN-06: convención @example.test verificada.
```

Advertencia de Starlette sobre TestClient/httpx: deprecación de la librería, no falla de negocio.

El workflow de CI (`.github/workflows/pytest.yml`) ejecuta los mismos dos comandos de test y chequeo sintético. Esa corrida local no acredita una ejecución remota de GitHub Actions.

## Trazabilidad

Los tres escenarios del Ajustar:

- Reserva válida → 201 PENDIENTE/ONLINE, `12:00:00Z`–`12:30:00Z`
- Solapamiento de profesional o sillón → 409 `TURNO_SOLAPADO`
- Borde inicio = fin anterior → 201

Matriz completa: `tests/matriz-escenarios.md`.

## Límites

No se probaron transacciones, locking ni `EXCLUDE USING gist`. RN-16 y PostgreSQL siguen pendientes. La demo es un proceso, memoria, datos ficticios. No hay login ni cancelación.

## Captura

Archivo: `docs/evidencias/etapa-6-tests-verde.png` (comando `python -m pytest` y resumen `74 passed`, 2026-10-15).
