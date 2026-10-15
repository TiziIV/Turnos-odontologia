from pathlib import Path

PROHIBIDOS = ("fastapi", "pydantic", "sqlalchemy", "starlette", "uvicorn")


def test_dominio_no_importa_frameworks():
    raiz = Path(__file__).resolve().parents[2] / "src" / "turnos" / "domain"
    ofensores = []
    for archivo in raiz.rglob("*.py"):
        texto = archivo.read_text(encoding="utf-8").lower()
        for nombre in PROHIBIDOS:
            if nombre in texto:
                ofensores.append(f"{archivo}: {nombre}")
    assert ofensores == []
