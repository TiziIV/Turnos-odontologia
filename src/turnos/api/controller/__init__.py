from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from turnos.api.dto import CrearTurnoRequest, TurnoResponse
from turnos.application.dto import CrearTurnoComando
from turnos.domain.exception.errores import ReferenciaInexistente

PANEL = Path(__file__).resolve().parents[1] / "panel" / "panel.html"


def _respuesta(turno) -> TurnoResponse:
    return TurnoResponse(
        id=turno.id,
        pacienteId=turno.paciente_id,
        profesionalId=turno.profesional_id,
        sillonId=turno.sillon_id,
        prestacionId=turno.prestacion_id,
        inicio=turno.inicio,
        fin=turno.fin,
        estado=turno.estado.value,
        canal=turno.canal.value,
    )


def registrar_rutas(app: FastAPI) -> None:
    @app.get("/panel", response_class=HTMLResponse)
    @app.get("/panel/", response_class=HTMLResponse)
    def panel() -> str:
        return PANEL.read_text(encoding="utf-8")

    @app.post("/api/public/turnos", status_code=201, response_model=TurnoResponse)
    def crear_turno_publico(cuerpo: CrearTurnoRequest, request: Request) -> TurnoResponse:
        turno = request.app.state.servicio.ejecutar(
            CrearTurnoComando(
                paciente_id=cuerpo.pacienteId,
                profesional_id=cuerpo.profesionalId,
                sillon_id=cuerpo.sillonId,
                prestacion_id=cuerpo.prestacionId,
                inicio=cuerpo.inicio,
            )
        )
        return _respuesta(turno)

    @app.get("/api/turnos", response_model=list[TurnoResponse])
    def listar_turnos(request: Request) -> list[TurnoResponse]:
        return [_respuesta(turno) for turno in request.app.state.agenda.turnos.listar()]

    @app.get("/api/pacientes/{paciente_id}")
    def ficha(paciente_id: int, request: Request) -> dict:
        try:
            paciente = request.app.state.agenda.ficha(paciente_id)
        except ReferenciaInexistente as exc:
            raise HTTPException(status_code=404, detail={"codigo": exc.codigo, "mensaje": exc.mensaje}) from exc
        return {
            "id": paciente.id,
            "nombre": paciente.nombre,
            "apellido": paciente.apellido,
            "documento": paciente.documento,
            "email": paciente.email,
        }

    @app.post("/api/public/enlaces", status_code=201)
    def crear_enlace(cuerpo: CrearTurnoRequest, request: Request) -> dict:
        enlace = request.app.state.agenda.crear_enlace(
            cuerpo.pacienteId, cuerpo.profesionalId, cuerpo.sillonId, cuerpo.prestacionId, cuerpo.inicio
        )
        return {"token": enlace.token, "usado": enlace.usado}

    @app.post("/api/public/enlaces/{token}/usar", status_code=201, response_model=TurnoResponse)
    def usar_enlace(token: str, request: Request) -> TurnoResponse:
        return _respuesta(request.app.state.agenda.usar_enlace(token))

    @app.post("/api/turnos/{turno_id}/confirmar", response_model=TurnoResponse)
    def confirmar(turno_id: int, request: Request) -> TurnoResponse:
        return _respuesta(request.app.state.agenda.confirmar(turno_id))

    @app.post("/api/turnos/{turno_id}/cancelar", response_model=TurnoResponse)
    def cancelar(turno_id: int, request: Request) -> TurnoResponse:
        return _respuesta(request.app.state.agenda.cancelar(turno_id))

    @app.post("/api/turnos/{turno_id}/reprogramar", response_model=TurnoResponse)
    def reprogramar(turno_id: int, cuerpo: CrearTurnoRequest, request: Request) -> TurnoResponse:
        return _respuesta(
            request.app.state.agenda.reprogramar(
                turno_id,
                cuerpo.inicio,
                cuerpo.profesionalId,
                cuerpo.sillonId,
                cuerpo.prestacionId,
            )
        )

    @app.get("/api/espera")
    def listar_espera(request: Request) -> list[dict]:
        return [
            {
                "id": espera.id,
                "pacienteId": espera.paciente_id,
                "profesionalId": espera.profesional_id,
                "sillonId": espera.sillon_id,
                "prestacionId": espera.prestacion_id,
                "inicio": espera.inicio,
            }
            for espera in request.app.state.agenda._esperas.listar()
        ]

    @app.post("/api/espera", status_code=201)
    def anotar_espera(cuerpo: CrearTurnoRequest, request: Request) -> dict:
        espera = request.app.state.agenda.anotar_espera(
            cuerpo.pacienteId, cuerpo.profesionalId, cuerpo.sillonId, cuerpo.prestacionId, cuerpo.inicio
        )
        return {"id": espera.id, "turnoCreado": False}

    @app.post("/api/espera/asignar", response_model=TurnoResponse)
    def asignar_espera(request: Request) -> TurnoResponse:
        return _respuesta(request.app.state.agenda.asignar_espera())
