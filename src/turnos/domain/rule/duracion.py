from datetime import datetime, timedelta

from turnos.domain.exception.errores import DuracionInvalida, IntervaloInvalido
from turnos.domain.rule.tiempo import a_utc


def calcular_fin(inicio: datetime, duracion_minutos: int) -> datetime:
    if not isinstance(duracion_minutos, int) or isinstance(duracion_minutos, bool):
        raise DuracionInvalida("La duración debe ser un entero positivo de minutos.")
    if duracion_minutos <= 0:
        raise DuracionInvalida("La duración de la prestación debe ser un entero positivo.")
    inicio_utc = a_utc(inicio)
    fin = inicio_utc + timedelta(minutes=duracion_minutos)
    if not inicio_utc < fin:
        raise IntervaloInvalido("El intervalo requiere inicio estrictamente anterior al fin.")
    return fin


def exigir_intervalo(inicio: datetime, fin: datetime) -> None:
    inicio_utc = a_utc(inicio)
    fin_utc = a_utc(fin)
    if not inicio_utc < fin_utc:
        raise IntervaloInvalido("El intervalo requiere inicio estrictamente anterior al fin.")
