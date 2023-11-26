from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import boto3
import time
import datetime

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
logs = boto3.client('logs', region_name='us-east-1')

log_stream_name = 'LogStream'
log_group_name = 'LogGroup'


try:
    logs.create_log_group(logGroupName=log_group_name)
    logs.create_log_stream(logGroupName=log_group_name,logStreamName=log_stream_name)
except:
    pass


def send_log(operation : str):
    logs.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[
            {
               'timestamp': int(time.time()),
               'message': f"A {operation} action"
            },
        ]
    )

def send_metric_plano(name, descricao, preco):
    cloudwatch.put_metric_data(
      Namespace='Metrics',
      MetricData=[
          {
              'MetricName': 'comprimento do nome',
              'Value': len(name),
              'Unit': 'None'
          },
          {
              'MetricName': 'comprimento da descricao',
              'Value': len(descricao),
              'Unit': 'None'
          },
          {
              'MetricName': 'Preco',
              'Value': preco,
              'Unit': 'None'
          },
      ]
  )
    
def send_metric_membro(name, id, data : datetime.date):
    cloudwatch.put_metric_data(
      Namespace='Metrics',
      MetricData=[
          {
              'MetricName': 'ano nascimento',
              'Value': int(data.year),
              'Unit': 'None'
          },
          {
              'MetricName': 'mes do nascimento',
              'Value': int(data.month),
              'Unit': 'None'
          },
          {
              'MetricName': 'dia do nascimento',
              'Value': int(data.day),
              'Unit': 'None'
          },
      ]
  )

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
    send_log("create member")
    send_metric_membro(membro.nome, membro.id_plano, membro.data_nascimento)
    return {"success": "created"}

@app.put("/membro")
def update_member(membro:Membro):
    if membro.id_membro not in Membros:
        return {"error": "not found"}
    if membro.id_plano not in Planos:
        return {"error": "plano not found"}
    Membros[membro.id_membro] = membro
    send_log("update member")
    return {"id": membro.id_membro, "success": "updated"} 

@app.get("/membro")
def read_all_members():
    list_membros = []
    dict_membros = {}
    for membro in Membros.values():
        dict_membros = {"id_membro": membro.id_membro, "nome": membro.nome, "id_plano": membro.id_plano, "data_nascimento": membro.data_nascimento}
        list_membros.append(dict_membros)
    send_log("get member")
    return list_membros

@app.get("/membro/{id_membro}")
def read_member(id_membro:int):
    if id_membro not in Membros:
        return {"error": "not found"}
    send_log("get member")
    return Membros[id_membro]

@app.delete("/membro/{id_membro}")
def delete_member(id_membro:int):
    if id_membro not in Membros:
        return {"error": "not found"}
    del Membros[id_membro]
    send_log("delete member")
    return {"id": id_membro, "success": "deleted"}


# Plano
@app.post("/plano")
def create_plano(plano:Plano):
    if plano.id_plano in Planos:
        return {"error": "already exists"}
    Planos[plano.id_plano] = plano
    send_log("create plano")
    send_metric_plano(plano.nome, plano.descricao, plano.preco)
    return {"success": "created"}

@app.put("/plano")
def update_plano(plano:Plano):
    if plano.id_plano not in Planos:
        return {"error": "not found"}
    Planos[plano.id_plano] = plano
    send_log("update plano")
    return {"id": plano.id_plano, "success": "updated"} 

@app.get("/plano")
def read_all_planos():
    list_planos = []
    dict_planos = {}
    for plano in Planos.values():
        dict_planos = {"id_plano": plano.id_plano, "nome": plano.nome, "descricao": plano.descricao, "preco": plano.preco}
        list_planos.append(dict_planos)
    send_log("get plano")
    return list_planos

@app.get("/plano/{id_plano}")
def read_plano(id_plano:int):
    if id_plano not in Planos:
        return {"error": "not found"}
    send_log("get plano")
    return Planos[id_plano]

@app.delete("/plano/{id_plano}")
def delete_plano(id_plano:int):
    if id_plano not in Planos:
        return {"error": "not found"}
    del Planos[id_plano]
    send_log("delete plano")
    return {"id": id_plano, "success": "deleted"}