from typing import Optional, Protocol

from turnos.domain.model.entidades import Paciente, Prestacion, Profesional, Sillon, Turno


class PacienteRepository(Protocol):
    def get(self, paciente_id: int) -> Optional[Paciente]: ...


class ProfesionalRepository(Protocol):
    def get(self, profesional_id: int) -> Optional[Profesional]: ...


class SillonRepository(Protocol):
    def get(self, sillon_id: int) -> Optional[Sillon]: ...


class PrestacionRepository(Protocol):
    def get(self, prestacion_id: int) -> Optional[Prestacion]: ...


class TurnoRepository(Protocol):
    def listar(self) -> list[Turno]: ...

    def guardar(self, turno: Turno) -> Turno: ...
