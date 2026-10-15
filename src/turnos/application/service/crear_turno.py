from turnos.application.dto import CrearTurnoComando
from turnos.domain.exception.errores import (
    PrestacionInactiva,
    RecursoInactivo,
    ReferenciaInexistente,
    TurnoSolapado,
)
from turnos.domain.model.entidades import Turno
from turnos.domain.model.enums import CanalTurno, EstadoTurno
from turnos.domain.port.repositorios import (
    PacienteRepository,
    PrestacionRepository,
    ProfesionalRepository,
    SillonRepository,
    TurnoRepository,
)
from turnos.domain.rule.duracion import calcular_fin
from turnos.domain.rule.estados import exigir_estado_valido
from turnos.domain.rule.solapamiento import hay_conflicto
from turnos.domain.rule.tiempo import a_utc


class CrearTurnoService:
    def __init__(
        self,
        pacientes: PacienteRepository,
        profesionales: ProfesionalRepository,
        sillones: SillonRepository,
        prestaciones: PrestacionRepository,
        turnos: TurnoRepository,
    ) -> None:
        self._pacientes = pacientes
        self._profesionales = profesionales
        self._sillones = sillones
        self._prestaciones = prestaciones
        self._turnos = turnos

    def ejecutar(self, comando: CrearTurnoComando) -> Turno:
        paciente = self._pacientes.get(comando.paciente_id)
        profesional = self._profesionales.get(comando.profesional_id)
        sillon = self._sillones.get(comando.sillon_id)
        prestacion = self._prestaciones.get(comando.prestacion_id)

        if paciente is None:
            raise ReferenciaInexistente("El paciente indicado no existe.")
        if profesional is None:
            raise ReferenciaInexistente("El profesional indicado no existe.")
        if sillon is None:
            raise ReferenciaInexistente("El sillón indicado no existe.")
        if prestacion is None:
            raise ReferenciaInexistente("La prestación indicada no existe.")
        if not profesional.activo:
            raise RecursoInactivo("El profesional no está activo.")
        if not sillon.activo:
            raise RecursoInactivo("El sillón no está activo.")
        if not prestacion.activa:
            raise PrestacionInactiva("La prestación no está activa.")

        inicio = a_utc(comando.inicio)
        fin = calcular_fin(inicio, prestacion.duracion_minutos)
        existentes = self._turnos.listar()
        if hay_conflicto(existentes, profesional.id, sillon.id, inicio, fin):
            raise TurnoSolapado(
                "El profesional o el sillón no está disponible en esa franja."
            )

        estado = exigir_estado_valido(EstadoTurno.PENDIENTE)
        turno = Turno(
            id=0,
            paciente_id=paciente.id,
            profesional_id=profesional.id,
            sillon_id=sillon.id,
            prestacion_id=prestacion.id,
            inicio=inicio,
            fin=fin,
            estado=estado,
            canal=CanalTurno.ONLINE,
        )
        return self._turnos.guardar(turno)
