from datetime import datetime, timedelta, timezone

import pytest

from turnos.application.dto import CrearTurnoComando
from turnos.application.service.crear_turno import CrearTurnoService
from turnos.domain.exception.errores import (
    DuracionInvalida,
    PrestacionInactiva,
    RecursoInactivo,
    ReferenciaInexistente,
    TurnoSolapado,
)
from turnos.domain.model.enums import CanalTurno, EstadoTurno
from turnos.infrastructure.memoria import PrestacionRepoMem
from tests.conftest import instante_local, prestacion_invalida, turno_activo


def comando(**kwargs) -> CrearTurnoComando:
    base = dict(
        paciente_id=1,
        profesional_id=1,
        sillon_id=1,
        prestacion_id=1,
        inicio=instante_local(9),
    )
    base.update(kwargs)
    return CrearTurnoComando(**base)


def test_alta_valida_pendiente_online_y_fin_calculado(servicio):
    creado = servicio.ejecutar(comando())
    assert creado.id == 1
    assert creado.estado is EstadoTurno.PENDIENTE
    assert creado.canal is CanalTurno.ONLINE
    assert creado.inicio == datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)
    assert creado.fin == datetime(2026, 11, 2, 12, 30, tzinfo=timezone.utc)


def test_alta_valida_guarda_una_sola_vez(servicio, repos):
    servicio.ejecutar(comando())
    assert len(repos[4].listar()) == 1


@pytest.mark.parametrize(
    "campo",
    ["paciente_id", "profesional_id", "sillon_id", "prestacion_id"],
)
def test_referencia_inexistente_no_guarda(servicio, repos, campo):
    with pytest.raises(ReferenciaInexistente):
        servicio.ejecutar(comando(**{campo: 99}))
    assert repos[4].listar() == []


@pytest.mark.parametrize(
    "kwargs",
    [{"profesional_id": 3}, {"sillon_id": 3}],
)
def test_rn11_recurso_inactivo_no_guarda(servicio, repos, kwargs):
    with pytest.raises(RecursoInactivo):
        servicio.ejecutar(comando(**kwargs))
    assert repos[4].listar() == []


def test_rn10_prestacion_inactiva_no_guarda(servicio, repos):
    with pytest.raises(PrestacionInactiva):
        servicio.ejecutar(comando(prestacion_id=5))
    assert repos[4].listar() == []


def test_rechazo_por_solapamiento_deja_agenda_intacta(servicio, repos):
    primero = servicio.ejecutar(comando())
    with pytest.raises(TurnoSolapado):
        servicio.ejecutar(comando(sillon_id=2, inicio=instante_local(9, 15)))
    agenda = repos[4].listar()
    assert agenda == [primero]


def test_duracion_invalida_en_catalogo_inyectado(repos):
    _, profesionales, sillones, _, turnos = repos
    prestaciones = PrestacionRepoMem({99: prestacion_invalida(0)})
    servicio = CrearTurnoService(repos[0], profesionales, sillones, prestaciones, turnos)
    with pytest.raises(DuracionInvalida):
        servicio.ejecutar(comando(prestacion_id=99))
    assert turnos.listar() == []


@pytest.mark.parametrize("codigo, minutos", [(2, 20), (1, 30), (3, 40), (4, 60)])
def test_rn02_duraciones_de_catalogo(servicio, codigo, minutos):
    creado = servicio.ejecutar(
        comando(prestacion_id=codigo, profesional_id=2, sillon_id=2)
    )
    assert creado.fin - creado.inicio == timedelta(minutes=minutos)


def test_rn09_fixture_cancelado_no_bloquea(servicio, repos):
    repos[4].cargar(turno_activo(estado=EstadoTurno.CANCELADO))
    creado = servicio.ejecutar(comando())
    assert creado.id >= 1
    assert len(repos[4].listar()) == 2
