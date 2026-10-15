from fastapi import FastAPI, Request

from turnos.api.dto import CrearTurnoRequest, TurnoResponse
from turnos.application.dto import CrearTurnoComando


def registrar_rutas(app: FastAPI) -> None:
    @app.post("/api/public/turnos", status_code=201, response_model=TurnoResponse)
    def crear_turno_publico(cuerpo: CrearTurnoRequest, request: Request) -> TurnoResponse:
        servicio = request.app.state.servicio
        turno = servicio.ejecutar(
            CrearTurnoComando(
                paciente_id=cuerpo.pacienteId,
                profesional_id=cuerpo.profesionalId,
                sillon_id=cuerpo.sillonId,
                prestacion_id=cuerpo.prestacionId,
                inicio=cuerpo.inicio,
            )
        )
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
