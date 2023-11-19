from pydantic import BaseModel
import datetime


class PlanoBase(BaseModel):
    nome: str
    descricao: str
    preco: float


class PlanoCreate(PlanoBase):
    pass


class Plano(PlanoBase):
    id_plano: int

    class Config:
        orm_mode = True


class MembroBase(BaseModel):
    nome: str
    id_plano: int
    data_nascimento : datetime.date


class MembroCreate(MembroBase):
    pass


class Membro(MembroBase):
    id_membro: int

    class Config:
        orm_mode = True
