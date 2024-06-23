from typing import List
from src.schema.seguridad_schema import seguridad, update_sec
from fastapi import APIRouter, HTTPException, Response, Depends
from src.config.db import engine
from src.models.BarrioSeguro_model import security
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from sqlalchemy.sql import select
from src.config.utils import get_api_key 

seguridad1_router = APIRouter()

# Crear un agente de seguridad
@seguridad1_router.post('/seguridad', status_code=HTTP_201_CREATED, tags=['Seguridad'], dependencies=[Depends(get_api_key)])
def create_seguridad(seguridad1: seguridad):
    with engine.connect() as conn:
        query = select(security).where(security.c.dni == seguridad1.dni)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Ya existe un agente de seguridad con ese DNI")

        new_security = seguridad1.model_dump()
        conn.execute(security.insert().values(new_security))
        conn.commit()
        return "Agente de seguridad correctamente añadido"

# Mostrar lista de agentes de seguridad
@seguridad1_router.get('/seguridad', tags=['Seguridad'], response_model=List[seguridad], dependencies=[Depends(get_api_key)])
def mostrar_ag_seguridad():
    with engine.connect() as conn:
        result = conn.execute(security.select()).fetchall()
        return result

# Mostrar lista de agentes de seguridad de una asociacion
@seguridad1_router.get('/seguridad/{id_asociacion}', response_model=List[seguridad], tags=['Seguridad'], dependencies=[Depends(get_api_key)])
def mostrar_seguridad_id_asoc(id_asoc: str):
    with engine.connect() as conn:
        result = conn.execute(security.select().where(security.c.id_asociacion == id_asoc)).fetchall()
        query = conn.execute(security.select().where(security.c.id_asociacion == id_asoc)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Lista de agentes de seguridad no encontrada con ese ID de la Asociacion")
        else:
            return result

# Actualizar los datos de un agente de seguridad
@seguridad1_router.put('/seguridad/{vecino_dni}', tags=['Seguridad'], response_model=update_sec, dependencies=[Depends(get_api_key)])
def actualizar_ag_seguridad(vecino_dni: int, actseg: update_sec):
    with engine.connect() as conn:
        conn.execute(security.update().values(num_celular=actseg.num_celular, salario=actseg.salario, fecha_fin=actseg.fecha_fin).where(security.c.dni == vecino_dni))
        conn.commit()
        result = conn.execute(security.select().where(security.c.dni == vecino_dni)).first()
        query = conn.execute(security.select().where(security.c.dni == vecino_dni)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Agente de Seguridad no encontrado con ese DNI")
        else:
            return result

# Eliminar un agente de seguridad
@seguridad1_router.delete('/seguridad/{vecino_dni}', tags=['Seguridad'], status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
def delete_ag_seguridad(vecino_dni: int):
    with engine.connect() as conn:
        conn.execute(security.delete().where(security.c.dni == vecino_dni))
        conn.commit()
        query = conn.execute(security.select().where(security.c.dni == vecino_dni)).fetchone()
        if query:
            raise HTTPException(status_code=404, detail="Agente de Seguridad no encontrado con ese DNI")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
