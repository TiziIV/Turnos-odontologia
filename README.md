# Turnos odontológicos

API y pantalla de demostración para un consultorio. Un turno ocupa a la vez un profesional y un sillón. La duración sale de la prestación. El intervalo es semiabierto: un turno puede empezar en el instante exacto en que termina el anterior.

## Qué está completo

- Crear un turno público (`POST /api/public/turnos`), archivado el 2026-10-15.
- Ficha mínima: el paciente sintético que ya existe (`GET /api/pacientes/{id}`).
- Reserva por enlace, confirmar, cancelar, reprogramar y lista de espera.
- Pantalla en `/panel/` (Agenda, Reserva y Espera) y Swagger en `/docs`.

## Qué falta

Login, mostrador autenticado, PostgreSQL, recordatorios, Mercado Pago, WhatsApp y dos reservas simultáneas (RN-16). Los datos viven en memoria y se pierden al detener el servidor.

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

Pantalla: http://127.0.0.1:8000/panel/

En Reserva y en Espera se elige el día y la hora de Argentina. El panel arma el inicio con zona `-03:00`. La agenda muestra el nombre de cada recurso y el intervalo en hora Argentina. La tabla de arriba dice qué número existe y cuál se rechaza. Swagger sigue pidiendo el inicio en ISO 8601.

Swagger: http://127.0.0.1:8000/docs

## Skill propia y MCP

La skill `revisar-escenarios-turno` está en `skills/revisar-escenarios-turno/SKILL.md`. Se usa al escribir una spec de turnos. Pide un caso que entra, uno que se rechaza y el borde en que el siguiente empieza cuando el anterior termina. Está registrada en `.atl/skill-registry.md` y citada en `AGENTS.md`.

El MCP es Context7. No es una skill y no lleva clave. El ejemplo está en `docs/skills-mcp/mcp.example.json`. En Cursor se agrega ese bloque a la configuración de MCP del usuario y se reinicia el agente. La conexión se comprueba si aparecen las herramientas `resolve-library-id` y `query-docs`.

Si Context7 no aparece, el agente no lo tiene cargado en esa sesión. No es un fallo del código de turnos. Hay que habilitar el servidor y abrir una sesión nueva. La ficha y el informe están en `docs/skills-mcp/`.

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
- Sin login y sin alta de mostrador autenticada. Cancelar sí está: `POST /api/turnos/{id}/cancelar`.
- Sin PostgreSQL. La garantía contra dos reservas simultáneas en procesos distintos queda fuera.
