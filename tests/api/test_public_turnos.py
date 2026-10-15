import pytest
from fastapi.testclient import TestClient

from turnos.api.app import create_app
from turnos.application.service.crear_turno import CrearTurnoService
from turnos.domain.model.enums import EstadoTurno
from turnos.infrastructure.memoria import repositorios_demo
from tests.conftest import turno_activo


def cliente() -> TestClient:
    return TestClient(create_app())


def cuerpo(**kwargs) -> dict:
    base = {
        "pacienteId": 1,
        "profesionalId": 1,
        "sillonId": 1,
        "prestacionId": 1,
        "inicio": "2026-11-02T09:00:00-03:00",
    }
    base.update(kwargs)
    return base


def test_camino_feliz_201_utc():
    respuesta = cliente().post("/api/public/turnos", json=cuerpo())
    assert respuesta.status_code == 201
    data = respuesta.json()
    assert data["estado"] == "PENDIENTE"
    assert data["canal"] == "ONLINE"
    assert data["inicio"] == "2026-11-02T12:00:00Z"
    assert data["fin"] == "2026-11-02T12:30:00Z"
    assert data["id"] == 1


@pytest.mark.parametrize(
    "parche",
    [
        {"pacienteId": 99},
        {"profesionalId": 99},
        {"sillonId": 99},
        {"prestacionId": 99},
        {"profesionalId": 3},
        {"sillonId": 3},
        {"prestacionId": 5},
    ],
)
def test_referencias_o_inactivos_422(parche):
    http = cliente()
    respuesta = http.post("/api/public/turnos", json=cuerpo(**parche))
    assert respuesta.status_code == 422
    assert http.post("/api/public/turnos", json=cuerpo()).status_code == 201


@pytest.mark.parametrize(
    "profesional_id, sillon_id",
    [(1, 2), (2, 1)],
)
def test_solapamiento_profesional_o_sillon_409(profesional_id, sillon_id):
    http = cliente()
    assert http.post("/api/public/turnos", json=cuerpo()).status_code == 201
    respuesta = http.post(
        "/api/public/turnos",
        json=cuerpo(
            profesionalId=profesional_id,
            sillonId=sillon_id,
            inicio="2026-11-02T09:15:00-03:00",
        ),
    )
    assert respuesta.status_code == 409
    assert respuesta.json()["detail"]["codigo"] == "TURNO_SOLAPADO"
    assert "paciente" not in respuesta.json()["detail"]["mensaje"].lower()


@pytest.mark.parametrize(
    "profesional_id, sillon_id",
    [(1, 2), (2, 1), (1, 1)],
)
def test_borde_inicio_igual_al_fin_anterior_201(profesional_id, sillon_id):
    http = cliente()
    primera = http.post("/api/public/turnos", json=cuerpo())
    assert primera.status_code == 201
    respuesta = http.post(
        "/api/public/turnos",
        json=cuerpo(
            profesionalId=profesional_id,
            sillonId=sillon_id,
            inicio="2026-11-02T09:30:00-03:00",
        ),
    )
    assert respuesta.status_code == 201
    assert primera.json()["fin"] == "2026-11-02T12:30:00Z"


def test_offsets_equivalentes_409():
    http = cliente()
    assert http.post("/api/public/turnos", json=cuerpo()).status_code == 201
    respuesta = http.post(
        "/api/public/turnos",
        json=cuerpo(inicio="2026-11-02T12:00:00Z"),
    )
    assert respuesta.status_code == 409


@pytest.mark.parametrize(
    "payload",
    [
        cuerpo(inicio="2026-11-02T09:00:00"),
        cuerpo(inicio="no-es-fecha"),
        cuerpo(pacienteId=0),
        cuerpo(pacienteId=-1),
        {k: v for k, v in cuerpo().items() if k != "inicio"},
        {**cuerpo(), "fin": "2026-11-02T12:30:00Z"},
        {**cuerpo(), "duracion": 30},
        {**cuerpo(), "estado": "CONFIRMADO"},
        {**cuerpo(), "canal": "MOSTRADOR"},
    ],
)
def test_entrada_invalida_422(payload):
    http = cliente()
    respuesta = http.post("/api/public/turnos", json=payload)
    assert respuesta.status_code == 422


def test_no_expone_ruta_privada_de_mostrador():
    respuesta = cliente().post("/api/turnos", json=cuerpo())
    assert respuesta.status_code == 404


def test_instancias_aisladas_no_comparten_agenda():
    a = cliente()
    b = cliente()
    assert a.post("/api/public/turnos", json=cuerpo()).status_code == 201
    assert b.post("/api/public/turnos", json=cuerpo()).status_code == 201


def test_estados_finales_en_fixture_permiten_alta():
    repos = repositorios_demo()
    repos[4].cargar(turno_activo(estado=EstadoTurno.REALIZADO))
    servicio = CrearTurnoService(*repos)
    http = TestClient(create_app(servicio))
    respuesta = http.post("/api/public/turnos", json=cuerpo())
    assert respuesta.status_code == 201


def test_reinicio_de_app_pierde_reservas():
    http = cliente()
    assert http.post("/api/public/turnos", json=cuerpo()).status_code == 201
    otra = cliente()
    assert otra.post("/api/public/turnos", json=cuerpo()).status_code == 201
