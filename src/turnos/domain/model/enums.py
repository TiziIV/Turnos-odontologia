from enum import Enum


class EstadoTurno(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"
    REALIZADO = "REALIZADO"
    AUSENTE = "AUSENTE"


class CanalTurno(str, Enum):
    ONLINE = "ONLINE"
    MOSTRADOR = "MOSTRADOR"


ESTADOS_ACTIVOS = frozenset({EstadoTurno.PENDIENTE, EstadoTurno.CONFIRMADO})
ESTADOS_VALIDOS = frozenset(EstadoTurno)
