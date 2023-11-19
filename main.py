from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI()

class Plano(BaseModel):
    id_plano: int
    nome: str
    descricao: str
    preco: float

class Membro(BaseModel):
    id_membro: int
    nome: str
    id_plano: int
    data_nascimento : datetime.date

Planos = {}
Membros = {}

@app.get("/")
def read_root():
    return {"Olá": "Bem vindo à Academia!"}


# Membro
@app.post("/membro")
def create_member(membro:Membro):
    if membro.id_membro in Membros:
        return {"error": "already exists"}
    if membro.id_plano not in Planos:
        return {"error": "plano not found"}
    Membros[membro.id_membro] = membro
    return {"success": "created"}

@app.put("/membro")
def update_member(membro:Membro):
    if membro.id_membro not in Membros:
        return {"error": "not found"}
    if membro.id_plano not in Planos:
        return {"error": "plano not found"}
    Membros[membro.id_membro] = membro
    return {"id": membro.id_membro, "success": "updated"} 

@app.get("/membro")
def read_all_members():
    list_membros = []
    dict_membros = {}
    for membro in Membros.values():
        dict_membros = {"id_membro": membro.id_membro, "nome": membro.nome, "id_plano": membro.id_plano, "data_nascimento": membro.data_nascimento}	
        list_membros.append(dict_membros)
    return list_membros

@app.get("/membro/{id_membro}")
def read_member(id_membro:int):
    if id_membro not in Membros:
        return {"error": "not found"}
    return Membros[id_membro]

@app.delete("/membro/{id_membro}")
def delete_member(id_membro:int):
    if id_membro not in Membros:
        return {"error": "not found"}
    del Membros[id_membro]
    return {"id": id_membro, "success": "deleted"}


# Plano
@app.post("/plano")
def create_plano(plano:Plano):
    if plano.id_plano in Planos:
        return {"error": "already exists"}
    Planos[plano.id_plano] = plano
    return {"success": "created"}

@app.put("/plano")
def update_plano(plano:Plano):
    if plano.id_plano not in Planos:
        return {"error": "not found"}
    Planos[plano.id_plano] = plano
    return {"id": plano.id_plano, "success": "updated"} 

@app.get("/plano")
def read_all_planos():
    list_planos = []
    dict_planos = {}
    for plano in Planos.values():
        dict_planos = {"id_plano": plano.id_plano, "nome": plano.nome, "descricao": plano.descricao, "preco": plano.preco}	
        list_planos.append(dict_planos)
    return list_planos

@app.get("/plano/{id_plano}")
def read_plano(id_plano:int):
    if id_plano not in Planos:
        return {"error": "not found"}
    return Planos[id_plano]

@app.delete("/plano/{id_plano}")
def delete_plano(id_plano:int):
    if id_plano not in Planos:
        return {"error": "not found"}
    del Planos[id_plano]
    return {"id": id_plano, "success": "deleted"}
 