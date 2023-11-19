from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PLANO ----------------------------------

@app.post("/plano", response_model=schemas.Plano)
def create_plano(plano: schemas.PlanoCreate, db: Session = Depends(get_db)):
    return crud.create_plano(db=db, plano=plano)


@app.get("/plano", response_model=list[schemas.Plano])
def read_planos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    planos = crud.get_planos(db, skip=skip, limit=limit)
    return planos


@app.get("/plano/{plano_id}", response_model=schemas.Plano)
def read_plano(plano_id: int, db: Session = Depends(get_db)):
    db_plano = crud.get_plano(db, id_plano=plano_id)
    if db_plano is None:
        raise HTTPException(status_code=404, detail="plano not found")
    return db_plano


@app.put('/plano/{plano_id}', response_model=schemas.Plano)
def update_plano(plano_id : int, plano : schemas.PlanoCreate, db : Session = Depends(get_db)):
    db_plano = crud.update_plano(db, plano, plano_id)
    if db_plano is None:
        raise HTTPException(status_code=404, detail="plano not found")
    return db_plano


@app.delete('/plano/{plano_id}')
def delete_plano(plano_id : int, db : Session = Depends(get_db)):
    db_plano = crud.delete_plano(db, plano_id)
    if db_plano is None:
        raise HTTPException(status_code=404, detail="plano not found")
    return db_plano


# MEMBRO ----------------------------------

@app.post("/membro", response_model=schemas.Membro)
def create_membro(membro: schemas.MembroCreate, db: Session = Depends(get_db)):
    db_plano = crud.get_plano(db, id_plano=membro.id_plano)
    if db_plano is None:
        raise HTTPException(status_code=404, detail="plano not found")
    return crud.create_membro(db=db, membro=membro)

@app.get("/membro", response_model=list[schemas.Membro])
def read_membros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    planos = crud.get_membros(db, skip=skip, limit=limit)
    return planos

@app.get("/membro/{membro_id}", response_model=schemas.Membro)
def read_membro(membro_id: int, db: Session = Depends(get_db)):
    db_membro = crud.get_membro(db, id_membro=membro_id)
    if db_membro is None:
        raise HTTPException(status_code=404, detail="membro not found")
    return db_membro

@app.put('/membro/{membro_id}', response_model=schemas.Membro)
def update_membro(membro_id : int, membro : schemas.MembroCreate, db : Session = Depends(get_db)):
    db_membro = crud.get_membro(db, id_membro=membro_id)
    if db_membro is None:
        raise HTTPException(status_code=404, detail="membro not found")
    db_plano = crud.get_plano(db, id_plano=membro.id_plano)
    if db_plano is None:
        raise HTTPException(status_code=404, detail="plano not found")
    db_membro = crud.update_membro(db, membro, membro_id)
    
    
    return db_membro

@app.delete('/membro/{membro_id}')
def delete_membro(membro_id : int, db : Session = Depends(get_db)):
    db_membro = crud.get_membro(db, id_membro=membro_id)
    if db_membro is None:
        raise HTTPException(status_code=404, detail="membro not found")
    db_membro = crud.delete_membro(db, membro_id)
    return db_membro