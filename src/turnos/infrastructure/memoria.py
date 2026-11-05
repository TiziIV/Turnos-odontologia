from typing import Optional

from turnos.domain.model.entidades import (
    EnlaceReserva,
    Espera,
    Paciente,
    Prestacion,
    Profesional,
    Sillon,
    Turno,
)
from turnos.infrastructure.catalogos import catalogos_sinteticos


class CatalogoEnMemoria:
    def __init__(self, items: dict[int, object]) -> None:
        self._items = dict(items)

    def get(self, item_id: int):
        return self._items.get(item_id)


class PacienteRepoMem(CatalogoEnMemoria):
    def get(self, paciente_id: int) -> Optional[Paciente]:
        item = self._items.get(paciente_id)
        return item if isinstance(item, Paciente) else None


class ProfesionalRepoMem(CatalogoEnMemoria):
    def get(self, profesional_id: int) -> Optional[Profesional]:
        item = self._items.get(profesional_id)
        return item if isinstance(item, Profesional) else None


class SillonRepoMem(CatalogoEnMemoria):
    def get(self, sillon_id: int) -> Optional[Sillon]:
        item = self._items.get(sillon_id)
        return item if isinstance(item, Sillon) else None


class PrestacionRepoMem(CatalogoEnMemoria):
    def get(self, prestacion_id: int) -> Optional[Prestacion]:
        item = self._items.get(prestacion_id)
        return item if isinstance(item, Prestacion) else None


class TurnoRepoMem:
    def __init__(self) -> None:
        self._turnos: list[Turno] = []
        self._siguiente = 1

    def listar(self) -> list[Turno]:
        return list(self._turnos)

    def cargar(self, turno: Turno) -> None:
        self._turnos.append(turno)
        self._siguiente = max(self._siguiente, turno.id + 1)

    def guardar(self, turno: Turno) -> Turno:
        asignado = Turno(
            id=self._siguiente,
            paciente_id=turno.paciente_id,
            profesional_id=turno.profesional_id,
            sillon_id=turno.sillon_id,
            prestacion_id=turno.prestacion_id,
            inicio=turno.inicio,
            fin=turno.fin,
            estado=turno.estado,
            canal=turno.canal,
        )
        self._siguiente += 1
        self._turnos.append(asignado)
        return asignado

    def obtener(self, turno_id: int) -> Optional[Turno]:
        for turno in self._turnos:
            if turno.id == turno_id:
                return turno
        return None

    def reemplazar(self, turno: Turno) -> Turno:
        for indice, actual in enumerate(self._turnos):
            if actual.id == turno.id:
                self._turnos[indice] = turno
                return turno
        raise KeyError(turno.id)


class EnlaceRepoMem:
    def __init__(self) -> None:
        self._items: dict[str, EnlaceReserva] = {}

    def guardar(self, enlace: EnlaceReserva) -> EnlaceReserva:
        self._items[enlace.token] = enlace
        return enlace

    def obtener(self, token: str) -> Optional[EnlaceReserva]:
        return self._items.get(token)


class EsperaRepoMem:
    def __init__(self) -> None:
        self._items: list[Espera] = []
        self._siguiente = 1

    def listar(self) -> list[Espera]:
        return list(self._items)

    def guardar(self, espera: Espera) -> Espera:
        asignada = Espera(
            id=self._siguiente,
            paciente_id=espera.paciente_id,
            profesional_id=espera.profesional_id,
            sillon_id=espera.sillon_id,
            prestacion_id=espera.prestacion_id,
            inicio=espera.inicio,
        )
        self._siguiente += 1
        self._items.append(asignada)
        return asignada

    def quitar(self, espera_id: int) -> None:
        self._items = [item for item in self._items if item.id != espera_id]


def repositorios_demo() -> tuple[
    PacienteRepoMem,
    ProfesionalRepoMem,
    SillonRepoMem,
    PrestacionRepoMem,
    TurnoRepoMem,
]:
    pacientes, profesionales, sillones, prestaciones = catalogos_sinteticos()
    return (
        PacienteRepoMem(pacientes),
        ProfesionalRepoMem(profesionales),
        SillonRepoMem(sillones),
        PrestacionRepoMem(prestaciones),
        TurnoRepoMem(),
    )
