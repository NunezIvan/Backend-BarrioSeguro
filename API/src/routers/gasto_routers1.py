from typing import List
from src.schema.gasto_schema import gasto_asoc,gasto_up
from fastapi import APIRouter,HTTPException,Response
from src.config.db import engine
from src.models.BarrioSeguro_model import gastos
from sqlalchemy.sql import select
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

gasto1_router=APIRouter()

#Registrar un gasto
@gasto1_router.post('/gasto',status_code=HTTP_201_CREATED,tags=['Gastos'])
def registrar_gastos(gasto:gasto_asoc):
    with engine.connect() as conn:
        query = select(gastos).where(gastos.c.id_gasto == gasto.id_gasto)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Ya existe un gasto con ese ID")

        new_gasto = gasto.model_dump()
        conn.execute(gastos.insert().values(new_gasto))
        conn.commit()
        return "Gasto correctamente añadido"
    
#Mostrar la lista de gastos
@gasto1_router.get('/gasto',tags=['Gastos'],response_model=List[gasto_asoc])
def mostrar_gastos():
    with engine.connect() as conn:
        result=conn.execute(gastos.select()).fetchall()
        return result
    
#Mostrar la lista de gastos de una asociacion
@gasto1_router.get('/gasto/{id_asociacion}',response_model=List[gasto_asoc],tags=['Gastos'])
def mostrar_gastos_id_asoc(id_asoc:str):
    with engine.connect() as conn:
        result = conn.execute(gastos.select().where(gastos.c.id_asociacion == id_asoc)).fetchall()
        query=conn.execute(gastos.select().where(gastos.c.id_asociacion == id_asoc)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Lista de gastos no encontrada con ese ID de la Asociacion")
        else:
            return result
        
#Actualizar los datos de un gasto
@gasto1_router.put('/gasto/{id_gasto}', tags=['Gastos'],response_model=gasto_up)
def actualizar_gasto(id_gasto:int, actgast:gasto_up):
    with engine.connect() as conn:
        conn.execute(gastos.update().values(tit_gasto=actgast.tit_gasto, fecha_gasto=actgast.fecha_gasto).where(gastos.c.id_gasto == id_gasto))
        conn.commit()
        result = conn.execute(gastos.select().where(gastos.c.id_gasto == id_gasto)).first()
        query=conn.execute(gastos.select().where(gastos.c.id_gasto == id_gasto)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Gasto no encontrado con ese ID")
        else:
            return result

#Eliminar un gasto del registro
@gasto1_router.delete('/gasto/{id_gasto}',tags=['Gastos'],status_code=HTTP_204_NO_CONTENT)
def delete_gasto(id_gasto:int):
    with engine.connect() as conn:
        conn.execute(gastos.delete().where(gastos.c.id_gasto == id_gasto))
        conn.commit()
        query=conn.execute(gastos.select().where(gastos.c.id_gasto == id_gasto)).fetchone()
        if query:
            raise HTTPException(status_code=404, detail="Gasto no encontrado con ese ID")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)