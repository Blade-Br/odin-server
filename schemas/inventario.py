from uuid import UUID

from pydantic import Field, model_validator

from schemas.base import SchemaBase

class IdentificacaoSchema(SchemaBase):
    hostname: str = Field(min_length=1)
    sistema_operacional: str = Field(min_length=1)
    versao: str = Field(min_length=1)


class CpuEstaticaSchema(SchemaBase):
    nucleos_fisicos: int | None = Field(default=None, gt=0)
    nucleos_logicos: int = Field(gt=0)

    @model_validator(mode="after")
    def validar_quantidade_de_nucleos(self):
        if (
            self.nucleos_fisicos is not None
            and self.nucleos_logicos < self.nucleos_fisicos
        ):
            raise ValueError(
                "nucleos_logicos não pode ser menor "
                "que nucleos_fisicos."
            )

        return self


class MemoriaEstaticaSchema(SchemaBase):
    capacidade_total_gb: float = Field(ge=0)


class MemoriaSchema(SchemaBase):
    memoria_fisica: MemoriaEstaticaSchema
    memoria_virtual: MemoriaEstaticaSchema


class DiscoEstaticoSchema(SchemaBase):
    nome: str = Field(min_length=1)
    capacidade_total_gb: float = Field(gt=0)


class InventarioSchema(SchemaBase):
    maquina_id: UUID
    identificacao: IdentificacaoSchema
    cpu: CpuEstaticaSchema
    memoria: MemoriaSchema
    discos: list[DiscoEstaticoSchema]
