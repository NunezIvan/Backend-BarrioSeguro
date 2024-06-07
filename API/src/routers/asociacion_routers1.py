from typing import List
from src.schema.asociacion_vecinal_schema import asociacion_vecinal,update_asociacion
from fastapi import APIRouter,HTTPException,Response
from src.config.db import engine
from src.models.BarrioSeguro_model import asociaciones
from sqlalchemy.sql import select
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

asociacion1_router=APIRouter()

#Crear una asociacion
@asociacion1_router.post('/asociaciones', tags=['Asociaciones Vecinales'], status_code=HTTP_201_CREATED)
def create_asociacion(asociacion:asociacion_vecinal):
    with engine.connect() as conn:
        query = select(asociaciones).where(asociaciones.c.id_asociacion == asociacion.id_asociacion)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Una asociacion ya tiene este ID")
        
        new_asociacion=asociacion.model_dump()
        conn.execute(asociaciones.insert().values(new_asociacion))
        conn.commit()
        return "Asociacion creada con exito"
    

#Mostrar la lista de asociaciones
@asociacion1_router.get('/asociaciones', tags=['Asociaciones Vecinales'], response_model=List[asociacion_vecinal])
def mostrar_asociaciones():
    with engine.connect() as conn:
        result=conn.execute(asociaciones.select()).fetchall()
        return result

#Buscar asociacion mediante su ID
@asociacion1_router.get('/asociaciones/{id_asociacion}',response_model=asociacion_vecinal,tags=['Asociaciones Vecinales'])
def mostrar_asociacion_id(id_asoc:str):
    with engine.connect() as conn:
        result = conn.execute(asociaciones.select().where(asociaciones.c.id_asociacion ==id_asoc)).first()
        query=conn.execute(asociaciones.select().where(asociaciones.c.id_asociacion == id_asoc)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Asociacion no encontrada con ese ID")
        else:
            return result
        

#Actualizar los datos de una asociacion vecinal
@asociacion1_router.put('/asociaciones/{id_asociacion}', tags=['Asociaciones Vecinales'],response_model=update_asociacion)
def actualizar_asociacion(id_asoc:str, actasoc:update_asociacion):
    with engine.connect() as conn:
        conn.execute(asociaciones.update().values(nombre=actasoc.nombre, distrito=actasoc.distrito, provincia=actasoc.provincia).where(asociaciones.c.id_asociacion == id_asoc))
        conn.commit()
        result = conn.execute(asociaciones.select().where(asociaciones.c.id_asociacion == id_asoc)).first()
        query=conn.execute(asociaciones.select().where(asociaciones.c.id_asociacion == id_asoc)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Asociacion no encontrada con ese ID")
        else:
            return result
        
#Eliminar una asociacion vecinal
@asociacion1_router.delete('/asociaciones/{id_asociacion}',tags=['Asociaciones Vecinales'],status_code=HTTP_204_NO_CONTENT)
def delete_asociaciones(id_asoc:str):
    with engine.connect() as conn:
        conn.execute(asociaciones.delete().where(asociaciones.c.id_asociacion == id_asoc))
        conn.commit()
        query=conn.execute(asociaciones.select().where(asociaciones.c.id_asociacion == id_asoc)).fetchone()
        if query:
            raise HTTPException(status_code=404, detail="Asociacion no encontrada con ese ID")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)