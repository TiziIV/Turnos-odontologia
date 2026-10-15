from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_serializer, field_validator

from turnos.domain.exception.errores import DatetimeSinZona
from turnos.domain.rule.tiempo import exigir_aware


class CrearTurnoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pacienteId: StrictInt = Field(gt=0)
    profesionalId: StrictInt = Field(gt=0)
    sillonId: StrictInt = Field(gt=0)
    prestacionId: StrictInt = Field(gt=0)
    inicio: datetime

    @field_validator("inicio")
    @classmethod
    def inicio_con_zona(cls, valor: datetime) -> datetime:
        try:
            return exigir_aware(valor)
        except DatetimeSinZona as exc:
            raise ValueError(exc.mensaje) from exc


class TurnoResponse(BaseModel):
    id: int
    pacienteId: int
    profesionalId: int
    sillonId: int
    prestacionId: int
    inicio: datetime
    fin: datetime
    estado: str
    canal: str

    @field_serializer("inicio", "fin")
    def serializar_utc(self, valor: datetime) -> str:
        utc = valor.astimezone(timezone.utc)
        return utc.strftime("%Y-%m-%dT%H:%M:%SZ")
