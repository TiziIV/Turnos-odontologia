class ErrorDeDominio(Exception):
    codigo: str = "ERROR_DOMINIO"

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class TurnoSolapado(ErrorDeDominio):
    codigo = "TURNO_SOLAPADO"


class ReferenciaInexistente(ErrorDeDominio):
    codigo = "REFERENCIA_INEXISTENTE"


class RecursoInactivo(ErrorDeDominio):
    codigo = "RECURSO_INACTIVO"


class PrestacionInactiva(ErrorDeDominio):
    codigo = "PRESTACION_INACTIVA"


class DuracionInvalida(ErrorDeDominio):
    codigo = "DURACION_INVALIDA"


class IntervaloInvalido(ErrorDeDominio):
    codigo = "INTERVALO_INVALIDO"


class DatetimeSinZona(ErrorDeDominio):
    codigo = "DATETIME_SIN_ZONA"


class EstadoInvalido(ErrorDeDominio):
    codigo = "ESTADO_INVALIDO"
