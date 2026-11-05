from fastapi.testclient import TestClient

from turnos.api.app import create_app


def cliente() -> TestClient:
    return TestClient(create_app())


def reserva(**cambios) -> dict:
    base = {
        "pacienteId": 1,
        "profesionalId": 1,
        "sillonId": 1,
        "prestacionId": 1,
        "inicio": "2026-11-02T09:00:00-03:00",
    }
    base.update(cambios)
    return base


def test_ficha_es_el_paciente_sintetico_y_no_trae_clinica():
    http = cliente()
    respuesta = http.get("/api/pacientes/1")
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["documento"] == "00000001"
    assert cuerpo["email"].endswith("@example.test")
    assert "diagnostico" not in cuerpo
    assert http.get("/api/pacientes/99").status_code == 404


def test_enlace_usado_crea_turno_y_el_rechazo_lo_deja_libre():
    http = cliente()
    assert http.post("/api/public/turnos", json=reserva()).status_code == 201
    enlace = http.post("/api/public/enlaces", json=reserva(pacienteId=2, inicio="2026-11-02T09:15:00-03:00"))
    assert enlace.status_code == 201
    token = enlace.json()["token"]
    choque = http.post(f"/api/public/enlaces/{token}/usar")
    assert choque.status_code == 409
    assert http.post(f"/api/public/enlaces/{token}/usar", json={}).status_code == 409
    libre = http.post("/api/public/enlaces", json=reserva(sillonId=2, profesionalId=2))
    token_libre = libre.json()["token"]
    alta = http.post(f"/api/public/enlaces/{token_libre}/usar")
    assert alta.status_code == 201
    assert http.post(f"/api/public/enlaces/{token_libre}/usar").status_code == 422
    assert http.post("/api/public/enlaces/no-existe/usar").status_code == 422


def test_confirmar_ocupa_cancelar_libera_y_reprogramar_es_atomica():
    http = cliente()
    creado = http.post("/api/public/turnos", json=reserva()).json()
    confirmado = http.post(f"/api/turnos/{creado['id']}/confirmar")
    assert confirmado.status_code == 200
    assert confirmado.json()["estado"] == "CONFIRMADO"
    choque = http.post("/api/public/turnos", json=reserva(pacienteId=2, sillonId=2, inicio="2026-11-02T09:10:00-03:00"))
    assert choque.status_code == 409
    otro = http.post("/api/public/turnos", json=reserva(pacienteId=2, profesionalId=2, sillonId=2, inicio="2026-11-02T11:00:00-03:00"))
    assert otro.status_code == 201
    rechazado = http.post(
        f"/api/turnos/{creado['id']}/reprogramar",
        json=reserva(profesionalId=2, sillonId=2, inicio="2026-11-02T11:00:00-03:00"),
    )
    assert rechazado.status_code == 409
    assert http.get("/api/turnos").json()[0]["inicio"].startswith("2026-11-02T12:00:00")
    cancelado = http.post(f"/api/turnos/{creado['id']}/cancelar")
    assert cancelado.json()["estado"] == "CANCELADO"
    assert http.post("/api/public/turnos", json=reserva(pacienteId=2)).status_code == 201
    assert http.post(f"/api/turnos/{creado['id']}/cancelar").status_code == 409


def test_espera_no_crea_turno_y_asigna_la_primera_que_entra():
    http = cliente()
    assert http.post("/api/public/turnos", json=reserva()).status_code == 201
    primera = http.post("/api/espera", json=reserva(pacienteId=2, inicio="2026-11-02T09:15:00-03:00"))
    assert primera.status_code == 201
    assert primera.json()["turnoCreado"] is False
    assert len(http.get("/api/turnos").json()) == 1
    segunda = http.post("/api/espera", json=reserva(pacienteId=2, profesionalId=2, sillonId=2, inicio="2026-11-02T09:15:00-03:00"))
    assert segunda.status_code == 201
    asignada = http.post("/api/espera/asignar")
    assert asignada.status_code == 200
    assert asignada.json()["profesionalId"] == 2
    restantes = http.get("/api/espera").json()
    assert [item["id"] for item in restantes] == [primera.json()["id"]]
    otra = cliente()
    otra.post("/api/public/turnos", json=reserva())
    otra.post("/api/espera", json=reserva(pacienteId=2, inicio="2026-11-02T09:10:00-03:00"))
    assert otra.post("/api/espera/asignar").status_code == 409
    assert len(otra.get("/api/espera").json()) == 1


def test_panel_muestra_las_tres_paginas():
    respuesta = cliente().get("/panel/")
    assert respuesta.status_code == 200
    texto = respuesta.text
    assert "Agenda" in texto and "Reserva" in texto and "Espera" in texto
