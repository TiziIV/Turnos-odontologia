from datetime import datetime, timezone

from turnos.domain.exception.errores import DatetimeSinZona


def exigir_aware(valor: datetime) -> datetime:
    if not isinstance(valor, datetime):
        raise DatetimeSinZona("El inicio debe ser un datetime con zona horaria.")
    if valor.tzinfo is None or valor.tzinfo.utcoffset(valor) is None:
        raise DatetimeSinZona("El inicio debe incluir zona horaria (offset o Z).")
    return valor.astimezone(timezone.utc)


def a_utc(valor: datetime) -> datetime:
    return exigir_aware(valor)
