from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Float,DateTime,VARCHAR
from sqlalchemy.orm import relationship, mapped_column

from .database import Base


class Plano(Base):
    __tablename__ = "plano"

    id_plano = Column(Integer,primary_key=True,index = True, autoincrement=True)
    nome = Column(String(45),index = True)
    descricao =  Column(String(45),index=True)
    preco = Column(Float,index = True)

    membro = relationship("Membro",back_populates="plano")


class Membro(Base):
    __tablename__ = "membro"

    id_membro = Column(Integer, primary_key = True,index = True, autoincrement=True)
    nome =  Column(String(45),index = True)
    data_nascimento = Column(DateTime,index = True)
    id_plano =  mapped_column(ForeignKey("plano.id_plano"))

    plano = relationship("Plano",back_populates="membro")