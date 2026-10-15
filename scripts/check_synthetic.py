"""Chequeo RN-06: convenciones sintéticas en catálogos y tests."""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
OBJETIVOS = [
    RAIZ / "src" / "turnos" / "infrastructure" / "catalogos.py",
    RAIZ / "tests",
]

EMAIL = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I)


def main() -> int:
    ofensores: list[str] = []
    for objetivo in OBJETIVOS:
        archivos = [objetivo] if objetivo.is_file() else list(objetivo.rglob("*.py"))
        for archivo in archivos:
            texto = archivo.read_text(encoding="utf-8")
            for match in EMAIL.finditer(texto):
                correo = match.group(0)
                if not correo.endswith("@example.test"):
                    ofensores.append(f"{archivo}: {correo}")
    if ofensores:
        print("RN-06: correos no sintéticos:")
        print("\n".join(ofensores))
        return 1
    print("RN-06: convención @example.test verificada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
