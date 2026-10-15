from turnos.domain.exception.errores import EstadoInvalido
from turnos.domain.model.enums import ESTADOS_VALIDOS, EstadoTurno


def exigir_estado_valido(estado: EstadoTurno) -> EstadoTurno:
    if estado not in ESTADOS_VALIDOS:
        raise EstadoInvalido("El estado del turno no pertenece al conjunto permitido.")
    return estado
