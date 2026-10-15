# Turnos odontológicos

API de demostración para crear un turno que ocupa a la vez un profesional y un sillón. La duración sale de la prestación. El intervalo es semiabierto: un turno puede empezar en el instante exacto en que termina el anterior.

No hay pantalla, login ni base de datos. Los datos viven en memoria de un solo proceso y se pierden al reiniciar. No se demuestra concurrencia PostgreSQL (RN-16).

## Identificadores de la demo

| Recurso | ID | Notas |
|---|---|---|
| Paciente Carla Pérez | 1 | `paciente1@example.test`, documento `00000001` |
| Paciente Diego Ruiz | 2 | `paciente2@example.test`, documento `00000002` |
| Profesional Ana Gómez | 1 | activo |
| Profesional Bruno Díaz | 2 | activo |
| Profesional Eva Sosa | 3 | inactivo |
| Sillón BOX-1 | 1 | activo |
| Sillón BOX-2 | 2 | activo |
| Prestación LIMPIEZA | 1 | 30 minutos |
| Prestación CONSULTA | 2 | 20 minutos |
| Prestación EXTRACCION | 3 | 40 minutos |
| Prestación ENDO | 4 | 60 minutos |

Al arrancar no hay reservas. Nombres y documentos son ficticios.

## Instalación

Python 3.12 o superior. Esta máquina usó Python 3.13.7. Dependencias fijadas en `requirements.txt` (FastAPI 0.143.2, Pydantic 2.14.1, pytest 8.4.2, Uvicorn 0.54.0). El CI usa Python 3.12; no se afirma una corrida remota de GitHub Actions.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

En un clon nuevo, si se usa `requirements.txt`:

```powershell
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Tests

```powershell
python -m pytest
```

Chequeo de convención sintética (RN-06):

```powershell
python scripts/check_synthetic.py
```

## Servidor local

Un worker, solo loopback:

```powershell
python -m uvicorn turnos.api.app:app --host 127.0.0.1 --port 8000 --workers 1
```

Reiniciar el proceso borra las reservas y vuelve a cargar el catálogo ficticio.

## Ejemplos PowerShell

Reserva válida (LIMPIEZA 30 minutos, 09:00-03:00 → 12:00Z / 12:30Z):

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/public/turnos -ContentType "application/json" -Body '{"pacienteId":1,"profesionalId":1,"sillonId":1,"prestacionId":1,"inicio":"2026-11-02T09:00:00-03:00"}'
```

Conflicto (mismo profesional, otro sillón, 09:15):

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/public/turnos -ContentType "application/json" -Body '{"pacienteId":2,"profesionalId":1,"sillonId":2,"prestacionId":1,"inicio":"2026-11-02T09:15:00-03:00"}'
```

Borde permitido (empieza a las 09:30, cuando termina el primero):

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/public/turnos -ContentType "application/json" -Body '{"pacienteId":2,"profesionalId":1,"sillonId":1,"prestacionId":1,"inicio":"2026-11-02T09:30:00-03:00"}'
```

Códigos: 201 creado, 409 `TURNO_SOLAPADO`, 422 entrada o referencia inválida.

## Límites

- Un proceso, datos en memoria, ejecución secuencial.
- Sin login, sin `POST /api/turnos` de mostrador, sin cancelar, sin PostgreSQL.
- La garantía contra dos reservas simultáneas en procesos distintos queda fuera de esta entrega.
