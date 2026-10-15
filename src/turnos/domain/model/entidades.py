from dataclasses import dataclass
from datetime import datetime

from turnos.domain.model.enums import CanalTurno, EstadoTurno


@dataclass(frozen=True)
class Paciente:
    id: int
    nombre: str
    apellido: str
    documento: str
    telefono: str
    email: str


@dataclass(frozen=True)
class Profesional:
    id: int
    nombre: str
    apellido: str
    matricula: str
    especialidad: str
    activo: bool


@dataclass(frozen=True)
class Sillon:
    id: int
    codigo: str
    descripcion: str
    activo: bool


@dataclass(frozen=True)
class Prestacion:
    id: int
    codigo: str
    nombre: str
    duracion_minutos: int
    activa: bool


@dataclass(frozen=True)
class Turno:
    id: int
    paciente_id: int
    profesional_id: int
    sillon_id: int
    prestacion_id: int
    inicio: datetime
    fin: datetime
    estado: EstadoTurno
    canal: CanalTurno
