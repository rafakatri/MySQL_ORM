from sqlalchemy.orm import Session
from sqlalchemy import update

from . import models, schemas

# PLANO --------------------------------------------------------

def create_plano(db: Session, plano: schemas.PlanoCreate):
    db_plano = models.Plano(**plano.model_dump())
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano

def get_planos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Plano).offset(skip).limit(limit).all()

def get_plano(db: Session, id_plano: int):
    return db.query(models.Plano).filter(models.Plano.id_plano == id_plano).first()

def update_plano(db: Session, plano: schemas.PlanoCreate, id_plano : int):
    db_plano = models.Plano(id_plano = id_plano, **plano.model_dump())
    stmt = (
        update(models.Plano).where(models.Plano.id_plano == id_plano)
        .values(id_plano = id_plano, **plano.model_dump()) 
    )
    db.execute(stmt)
    db.commit()
    return db_plano


def create_membro(db:Session, membro:schemas.MembroCreate):
    db_membro = models.Membro(**membro.model_dump())
    db.add(db_membro)
    db.commit()
    db.refresh(db_membro)
    return db_membro

def delete_plano(db: Session, id_plano : int):
    plano = db.get(models.Plano, id_plano)
    db.delete(plano)
    db.commit()
    return {'Sucess' : f"ID: {id_plano} deleted"}

# MEMBRO --------------------------------------------------------

def get_membro(db:Session, id_membro:int):
    return db.query(models.Membro).filter(models.Membro.id_membro == id_membro).first()

def get_membros(db : Session, skip : int = 0,limit : int = 100):
    return db.query(models.Membro).offset(skip).limit(limit).all()

def update_membro(db: Session, membro: schemas.MembroCreate, id_membro : int):
    db_membro = models.Membro(id_membro = id_membro, **membro.model_dump())
    stmt = (
        update(models.Membro).where(models.Membro.id_membro == id_membro)
        .values(id_membro = id_membro, **membro.model_dump()) 
    )
    db.execute(stmt)
    db.commit()
    return db_membro

def delete_membro(db: Session, id_membro : int):
    membro = db.get(models.Membro, id_membro)
    db.delete(membro)
    db.commit()
    return {'Sucess' : f"ID: {id_membro} deleted"}

