from typing import List
from src.schema.pago_schema import pago_update,pago_vecino
from fastapi import APIRouter,HTTPException,Response
from src.config.db import engine
from src.models.BarrioSeguro_model import pagos,vecinos
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from sqlalchemy.sql import select

pago1_router = APIRouter()

#Crear un pago
@pago1_router.post('/pago',status_code=HTTP_201_CREATED,tags=['Pago_Vecino'])
def create_pago(pago:pago_vecino):
    with engine.connect() as conn:
        query = select(pagos).where(pagos.c.id_pago == pago.id_pago)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Ya existe un pago con ese ID")

        result_dni = conn.execute(vecinos.select().where(vecinos.c.dni == pago.vecino_dni)).fetchone()
        if  not result_dni:
            raise HTTPException(status_code=400, detail="No existe un vecino con ese DNI")

        new_pago = pago.model_dump()
        conn.execute(pagos.insert().values(new_pago))
        conn.commit()
        return "Pago correctamente añadido"
    

#Mostrar lista de pagos
@pago1_router.get('/pago',tags=['Pago_Vecino'],response_model=List[pago_vecino])
def mostrar_pagos():
    with engine.connect() as conn:
        result=conn.execute(pagos.select()).fetchall()
        return result
    
    
#Mostrar lista de pagos de un vecino
@pago1_router.get('/pago/{vecino_dni}',response_model=List[pago_vecino],tags=['Pago_Vecino'])
def mostrar_pagos_vecino_dni(vecino_dni:int):
    with engine.connect() as conn:
        result = conn.execute(pagos.select().where(pagos.c.vecino_dni == vecino_dni)).fetchall()
        query=conn.execute(pagos.select().where(pagos.c.vecino_dni == vecino_dni)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Lista de pagos no encontrada con ese DNI")
        else:
            return result
        
#Actualizar los datos de un agente de seguridad
@pago1_router.put('/pago/{id_pago}', tags=['Pago_Vecino'],response_model=pago_update)
def actualizar_pag(id_pago:int, actpag:pago_update):
    with engine.connect() as conn:
        conn.execute(pagos.update().values(fecha_pago=actpag.fecha_pago, hora_pago=actpag.hora_pago, monto_pago=actpag.monto_pago, metodo_pago=actpag.metodo_pago, cancel_pago=actpag.cancel_pago).where(pagos.c.id_pago == id_pago))
        conn.commit()
        result = conn.execute(pagos.select().where(pagos.c.id_pago == id_pago)).first()
        query=conn.execute(pagos.select().where(pagos.c.id_pago == id_pago)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Pago no encontrado con ID")
        else:
            return result

#Eliminar un pago
@pago1_router.delete('/pago/{id_pago}',tags=['Pago_Vecino'],status_code=HTTP_204_NO_CONTENT)
def delete_pag(id_pago:int):
    with engine.connect() as conn:
        conn.execute(pagos.delete().where(pagos.c.id_pago == id_pago))
        conn.commit()
        query=conn.execute(pagos.select().where(pagos.c.id_pago == id_pago)).fetchone()
        if query:
            raise HTTPException(status_code=404, detail="Pago no encontrado con ese ID")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)







