from pathlib import Path

from turnos.infrastructure.catalogos import catalogos_sinteticos


def test_rn06_emails_y_documentos_sinteticos():
    pacientes, *_ = catalogos_sinteticos()
    for paciente in pacientes.values():
        assert paciente.email.endswith("@example.test")
        assert paciente.documento.startswith("0000000")
        assert paciente.documento != ""


def test_rn06_sin_datos_clinicos_en_catalogo():
    texto = Path("src/turnos/infrastructure/catalogos.py").read_text(encoding="utf-8").lower()
    for prohibido in ("diagnostico", "radiografia", "historia clinica", "dni real"):
        assert prohibido not in texto
