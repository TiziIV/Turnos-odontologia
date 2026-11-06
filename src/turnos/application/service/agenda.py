import secrets
from datetime import datetime

from turnos.application.dto import CrearTurnoComando
from turnos.application.service.crear_turno import CrearTurnoService
from turnos.domain.exception.errores import (
    EnlaceNoDisponible,
    EsperaSinCupo,
    ReferenciaInexistente,
    TransicionInvalida,
    TurnoSolapado,
)
from turnos.domain.model.entidades import EnlaceReserva, Espera, Turno
from turnos.domain.model.enums import EstadoTurno
from turnos.domain.rule.duracion import calcular_fin
from turnos.domain.rule.solapamiento import hay_conflicto
from turnos.domain.rule.tiempo import a_utc
from turnos.infrastructure.persistence.memoria import EnlaceRepoMem, EsperaRepoMem, TurnoRepoMem


class AgendaService:
    """Operaciones posteriores al alta: ficha, enlace, estados y espera."""

    def __init__(self, crear: CrearTurnoService, enlaces: EnlaceRepoMem, esperas: EsperaRepoMem) -> None:
        self._crear = crear
        self._enlaces = enlaces
        self._esperas = esperas

    @property
    def turnos(self) -> TurnoRepoMem:
        return self._crear._turnos

    def ficha(self, paciente_id: int):
        paciente = self._crear._pacientes.get(paciente_id)
        if paciente is None:
            raise ReferenciaInexistente("El paciente indicado no existe.")
        return paciente

    def crear_enlace(
        self,
        paciente_id: int,
        profesional_id: int,
        sillon_id: int,
        prestacion_id: int,
        inicio: datetime,
    ) -> EnlaceReserva:
        self.ficha(paciente_id)
        enlace = EnlaceReserva(
            token=secrets.token_hex(8),
            paciente_id=paciente_id,
            profesional_id=profesional_id,
            sillon_id=sillon_id,
            prestacion_id=prestacion_id,
            inicio=a_utc(inicio),
            usado=False,
        )
        return self._enlaces.guardar(enlace)

    def usar_enlace(self, token: str) -> Turno:
        enlace = self._enlaces.obtener(token)
        if enlace is None or enlace.usado:
            raise EnlaceNoDisponible("El enlace no existe o ya fue usado.")
        try:
            turno = self._crear.ejecutar(
                CrearTurnoComando(
                    paciente_id=enlace.paciente_id,
                    profesional_id=enlace.profesional_id,
                    sillon_id=enlace.sillon_id,
                    prestacion_id=enlace.prestacion_id,
                    inicio=enlace.inicio,
                )
            )
        except TurnoSolapado:
            raise
        self._enlaces.guardar(
            EnlaceReserva(
                token=enlace.token,
                paciente_id=enlace.paciente_id,
                profesional_id=enlace.profesional_id,
                sillon_id=enlace.sillon_id,
                prestacion_id=enlace.prestacion_id,
                inicio=enlace.inicio,
                usado=True,
            )
        )
        return turno

    def confirmar(self, turno_id: int) -> Turno:
        turno = self._exigir(turno_id)
        if turno.estado is not EstadoTurno.PENDIENTE:
            raise TransicionInvalida("Solo un turno pendiente puede confirmarse.")
        return self.turnos.reemplazar(_con_estado(turno, EstadoTurno.CONFIRMADO))

    def cancelar(self, turno_id: int) -> Turno:
        turno = self._exigir(turno_id)
        if turno.estado not in (EstadoTurno.PENDIENTE, EstadoTurno.CONFIRMADO):
            raise TransicionInvalida("Ese turno ya no se puede cancelar.")
        return self.turnos.reemplazar(_con_estado(turno, EstadoTurno.CANCELADO))

    def reprogramar(
        self,
        turno_id: int,
        inicio: datetime,
        profesional_id: int | None = None,
        sillon_id: int | None = None,
        prestacion_id: int | None = None,
    ) -> Turno:
        turno = self._exigir(turno_id)
        if turno.estado not in (EstadoTurno.PENDIENTE, EstadoTurno.CONFIRMADO):
            raise TransicionInvalida("Ese turno ya no se puede reprogramar.")
        profesional = profesional_id if profesional_id is not None else turno.profesional_id
        sillon = sillon_id if sillon_id is not None else turno.sillon_id
        prestacion_id = prestacion_id if prestacion_id is not None else turno.prestacion_id
        prestacion = self._crear._prestaciones.get(prestacion_id)
        if prestacion is None or not prestacion.activa:
            raise ReferenciaInexistente("La prestación indicada no existe.")
        inicio_utc = a_utc(inicio)
        fin = calcular_fin(inicio_utc, prestacion.duracion_minutos)
        if hay_conflicto(
            self.turnos.listar(),
            profesional,
            sillon,
            inicio_utc,
            fin,
            excluir_id=turno.id,
        ):
            raise TurnoSolapado(
                "El profesional o el sillón no está disponible en esa franja."
            )
        movido = Turno(
            id=turno.id,
            paciente_id=turno.paciente_id,
            profesional_id=profesional,
            sillon_id=sillon,
            prestacion_id=prestacion.id,
            inicio=inicio_utc,
            fin=fin,
            estado=turno.estado,
            canal=turno.canal,
        )
        return self.turnos.reemplazar(movido)

    def anotar_espera(
        self,
        paciente_id: int,
        profesional_id: int,
        sillon_id: int,
        prestacion_id: int,
        inicio: datetime,
    ) -> Espera:
        self.ficha(paciente_id)
        antes = len(self.turnos.listar())
        espera = self._esperas.guardar(
            Espera(0, paciente_id, profesional_id, sillon_id, prestacion_id, a_utc(inicio))
        )
        if len(self.turnos.listar()) != antes:
            raise RuntimeError("Anotar una espera no debe crear un turno.")
        return espera

    def asignar_espera(self) -> Turno:
        for espera in self._esperas.listar():
            try:
                turno = self._crear.ejecutar(
                    CrearTurnoComando(
                        paciente_id=espera.paciente_id,
                        profesional_id=espera.profesional_id,
                        sillon_id=espera.sillon_id,
                        prestacion_id=espera.prestacion_id,
                        inicio=espera.inicio,
                    )
                )
            except TurnoSolapado:
                continue
            self._esperas.quitar(espera.id)
            return turno
        raise EsperaSinCupo("Ninguna espera tiene profesional y sillón libres.")

    def _exigir(self, turno_id: int) -> Turno:
        turno = self.turnos.obtener(turno_id)
        if turno is None:
            raise ReferenciaInexistente("El turno indicado no existe.")
        return turno


def _con_estado(turno: Turno, estado: EstadoTurno) -> Turno:
    return Turno(
        id=turno.id,
        paciente_id=turno.paciente_id,
        profesional_id=turno.profesional_id,
        sillon_id=turno.sillon_id,
        prestacion_id=turno.prestacion_id,
        inicio=turno.inicio,
        fin=turno.fin,
        estado=estado,
        canal=turno.canal,
    )
