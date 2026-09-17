from typing import Annotated
from ipaddress import IPv4Address
from uuid import UUID

from pydantic import AwareDatetime, Field, model_validator

from schemas.base import SchemaBase


Percentual = Annotated[float, Field(ge=0, le=100)]


class CpuVolatilSchema(SchemaBase):
    uso_percentual: Percentual
    frequencia_ghz: float | None = Field(default=None, ge=0)
    uso_por_nucleo: list[Percentual]


class MemoriaVolatilSchema(SchemaBase):
    memoria_utilizada_gb: float = Field(ge=0)
    memoria_utilizada_percentual: Percentual
    memoria_disponivel_gb: float = Field(ge=0)
    memoria_disponivel_percentual: Percentual


class MemoriaVolatilCompletaSchema(SchemaBase):
    memoria_fisica: MemoriaVolatilSchema
    memoria_virtual: MemoriaVolatilSchema


class DiscoVolatilSchema(SchemaBase):
    nome: str = Field(min_length=1)
    utilizado_gb: float = Field(ge=0)
    disponivel_gb: float = Field(ge=0)


class RedeVolatilSchema(SchemaBase):
    conectado: bool
    nome_rede: str | None = None
    ipv4: IPv4Address | None = None
    download_mb_s: float = Field(ge=0)
    upload_mb_s: float = Field(ge=0)

    @model_validator(mode="after")
    def validar_rede_desconectada(self):
        if not self.conectado:
            if self.nome_rede is not None or self.ipv4 is not None:
                raise ValueError(
                    "Uma rede desconectada não deve possuir "
                    "nome de rede ou IPv4."
                )

        return self


class SistemaVolatilSchema(SchemaBase):
    uptime_segundos: int = Field(ge=0)


class MetricasSchema(SchemaBase):
    maquina_id: UUID
    timestamp: AwareDatetime
    cpu: CpuVolatilSchema
    memoria: MemoriaVolatilCompletaSchema
    discos: list[DiscoVolatilSchema]
    rede: RedeVolatilSchema
    sistema: SistemaVolatilSchema
