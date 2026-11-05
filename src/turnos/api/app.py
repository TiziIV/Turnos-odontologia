from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from turnos.application.service.agenda import AgendaService
from turnos.application.service.crear_turno import CrearTurnoService
from turnos.domain.exception.errores import ErrorDeDominio, TurnoSolapado
from turnos.infrastructure.memoria import EnlaceRepoMem, EsperaRepoMem, repositorios_demo
from turnos.api.controller import registrar_rutas


def armar_servicio() -> CrearTurnoService:
    return CrearTurnoService(*repositorios_demo())


def armar_agenda(servicio: CrearTurnoService | None = None) -> AgendaService:
    return AgendaService(servicio or armar_servicio(), EnlaceRepoMem(), EsperaRepoMem())


def create_app(servicio: CrearTurnoService | None = None, agenda: AgendaService | None = None) -> FastAPI:
    app = FastAPI(title="turnos-odontologia", version="0.1.0")
    app.state.servicio = servicio or (agenda._crear if agenda else armar_servicio())
    app.state.agenda = agenda or armar_agenda(app.state.servicio)

    @app.exception_handler(TurnoSolapado)
    async def solapado(_request: Request, exc: TurnoSolapado) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": {"codigo": exc.codigo, "mensaje": exc.mensaje}},
        )

    @app.exception_handler(ErrorDeDominio)
    async def dominio(_request: Request, exc: ErrorDeDominio) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": {"codigo": exc.codigo, "mensaje": exc.mensaje}},
        )

    registrar_rutas(app)
    return app


app = create_app()
