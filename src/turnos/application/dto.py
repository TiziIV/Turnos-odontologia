from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrearTurnoComando:
    paciente_id: int
    profesional_id: int
    sillon_id: int
    prestacion_id: int
    inicio: datetime
