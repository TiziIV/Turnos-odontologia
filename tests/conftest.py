from datetime import datetime, timedelta, timezone

import pytest

from turnos.application.service.crear_turno import CrearTurnoService
from turnos.domain.model.entidades import Prestacion, Turno
from turnos.domain.model.enums import CanalTurno, EstadoTurno
from turnos.infrastructure.memoria import repositorios_demo

OFFSET_AR = timezone(timedelta(hours=-3))


def instante_local(hora: int, minuto: int = 0) -> datetime:
    return datetime(2026, 11, 2, hora, minuto, tzinfo=OFFSET_AR)


@pytest.fixture
def repos():
    return repositorios_demo()


@pytest.fixture
def servicio(repos):
    return CrearTurnoService(*repos)


def turno_activo(
    *,
    turno_id: int = 10,
    profesional_id: int = 1,
    sillon_id: int = 1,
    inicio: datetime | None = None,
    duracion: int = 30,
    estado: EstadoTurno = EstadoTurno.PENDIENTE,
) -> Turno:
    inicio = inicio or instante_local(9)
    fin = inicio.astimezone(timezone.utc) + timedelta(minutes=duracion)
    return Turno(
        id=turno_id,
        paciente_id=1,
        profesional_id=profesional_id,
        sillon_id=sillon_id,
        prestacion_id=1,
        inicio=inicio.astimezone(timezone.utc),
        fin=fin,
        estado=estado,
        canal=CanalTurno.ONLINE,
    )


def prestacion_invalida(duracion: int) -> Prestacion:
    return Prestacion(99, "CERO", "Inválida", duracion, True)
