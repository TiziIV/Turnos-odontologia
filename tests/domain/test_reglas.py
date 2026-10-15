from datetime import datetime, timedelta, timezone

import pytest

from turnos.domain.exception.errores import (
    DatetimeSinZona,
    DuracionInvalida,
    EstadoInvalido,
    IntervaloInvalido,
)
from turnos.domain.model.enums import CanalTurno, EstadoTurno
from turnos.domain.rule.duracion import calcular_fin, exigir_intervalo
from turnos.domain.rule.estados import exigir_estado_valido
from turnos.domain.rule.solapamiento import hay_conflicto
from turnos.domain.rule.tiempo import a_utc
from tests.conftest import instante_local, turno_activo


@pytest.mark.parametrize(
    "duracion",
    [20, 30, 40, 60],
)
def test_rn02_fin_deriva_de_duracion_de_prestacion(duracion):
    inicio = instante_local(9)
    fin = calcular_fin(inicio, duracion)
    assert fin - a_utc(inicio) == timedelta(minutes=duracion)


@pytest.mark.parametrize("duracion", [0, -1])
def test_rn02_duracion_no_positiva_se_rechaza(duracion):
    with pytest.raises(DuracionInvalida):
        calcular_fin(instante_local(9), duracion)


def test_rn13_inicio_igual_al_fin_se_rechaza():
    inicio = a_utc(instante_local(9))
    with pytest.raises(IntervaloInvalido):
        exigir_intervalo(inicio, inicio)


def test_rn07_enum_acepta_cinco_estados():
    for estado in EstadoTurno:
        assert exigir_estado_valido(estado) is estado


def test_rn07_estado_invalido_se_rechaza():
    with pytest.raises(EstadoInvalido):
        exigir_estado_valido("RESERVADO")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("profesional_id", "sillon_id"),
    [(1, 2), (2, 1)],
)
def test_rn01_rn03_rechaza_interseccion_por_profesional_o_sillon(profesional_id, sillon_id):
    a = turno_activo()
    b_inicio = instante_local(9, 15)
    b_fin = calcular_fin(b_inicio, 30)
    assert hay_conflicto([a], profesional_id, sillon_id, b_inicio, b_fin) is True


@pytest.mark.parametrize(
    ("profesional_id", "sillon_id"),
    [(1, 2), (2, 1), (1, 1)],
)
def test_rn03_borde_inicio_igual_al_fin_anterior_es_valido(profesional_id, sillon_id):
    a = turno_activo()
    b_inicio = instante_local(9, 30)
    b_fin = calcular_fin(b_inicio, 30)
    assert hay_conflicto([a], profesional_id, sillon_id, b_inicio, b_fin) is False


@pytest.mark.parametrize(
    ("hora", "minuto", "duracion"),
    [(9, 29, 30), (8, 50, 60), (9, 0, 20)],
)
@pytest.mark.parametrize(
    ("profesional_id", "sillon_id"),
    [(1, 2), (2, 1)],
)
def test_rn03_un_minuto_y_contencion_se_rechazan(hora, minuto, duracion, profesional_id, sillon_id):
    a = turno_activo()
    b_inicio = instante_local(hora, minuto)
    b_fin = calcular_fin(b_inicio, duracion)
    assert hay_conflicto([a], profesional_id, sillon_id, b_inicio, b_fin) is True


def test_rn01_recursos_distintos_no_conflictuan():
    a = turno_activo()
    b_inicio = instante_local(9)
    b_fin = calcular_fin(b_inicio, 30)
    assert hay_conflicto([a], 2, 2, b_inicio, b_fin) is False


@pytest.mark.parametrize(
    "estado",
    [EstadoTurno.CANCELADO, EstadoTurno.REALIZADO, EstadoTurno.AUSENTE],
)
def test_rn09_estados_finales_no_ocupan_recursos(estado):
    a = turno_activo(estado=estado)
    b_inicio = instante_local(9)
    b_fin = calcular_fin(b_inicio, 30)
    assert hay_conflicto([a], 1, 1, b_inicio, b_fin) is False


def test_rn09_confirmado_si_ocupa():
    a = turno_activo(estado=EstadoTurno.CONFIRMADO)
    b_inicio = instante_local(9, 15)
    b_fin = calcular_fin(b_inicio, 30)
    assert hay_conflicto([a], 1, 2, b_inicio, b_fin) is True


def test_tiempo_offsets_equivalentes_son_el_mismo_instante():
    local = instante_local(9)
    utc = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)
    assert a_utc(local) == a_utc(utc)


def test_tiempo_naive_se_rechaza():
    with pytest.raises(DatetimeSinZona):
        a_utc(datetime(2026, 11, 2, 9, 0))


def test_canal_online_existe_para_alta():
    assert CanalTurno.ONLINE.value == "ONLINE"
