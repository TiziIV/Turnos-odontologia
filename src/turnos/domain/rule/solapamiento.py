from datetime import datetime

from turnos.domain.model.entidades import Turno
from turnos.domain.model.enums import ESTADOS_ACTIVOS
from turnos.domain.rule.tiempo import a_utc


def intervalos_intersectan(
    inicio_a: datetime,
    fin_a: datetime,
    inicio_b: datetime,
    fin_b: datetime,
) -> bool:
    a_ini = a_utc(inicio_a)
    a_fin = a_utc(fin_a)
    b_ini = a_utc(inicio_b)
    b_fin = a_utc(fin_b)
    return a_ini < b_fin and b_ini < a_fin


def comparte_recurso(existente: Turno, profesional_id: int, sillon_id: int) -> bool:
    return existente.profesional_id == profesional_id or existente.sillon_id == sillon_id


def hay_conflicto(
    existentes: list[Turno],
    profesional_id: int,
    sillon_id: int,
    inicio: datetime,
    fin: datetime,
) -> bool:
    for turno in existentes:
        if turno.estado not in ESTADOS_ACTIVOS:
            continue
        if not comparte_recurso(turno, profesional_id, sillon_id):
            continue
        if intervalos_intersectan(turno.inicio, turno.fin, inicio, fin):
            return True
    return False
