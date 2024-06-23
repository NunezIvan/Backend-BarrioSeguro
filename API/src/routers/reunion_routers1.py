from typing import List
from src.schema.reunion_schema import reunion, act_reu
from fastapi import APIRouter, HTTPException, Response, Depends
from src.config.db import engine
from src.models.BarrioSeguro_model import reuniones, asociaciones, vecinos
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from sqlalchemy.sql import select
from src.config.utils import get_api_key  

reunion1_router = APIRouter()

# Crear una reunion
@reunion1_router.post('/reunion', status_code=HTTP_201_CREATED, tags=['Reunion'], dependencies=[Depends(get_api_key)])
def create_reunion(reu: reunion):
    with engine.connect() as conn:
        query = select(reuniones).where(reuniones.c.id_reunion == reu.id_reunion)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Ya existe una reunion con ese ID")

        result_asoc = conn.execute(asociaciones.select().where(asociaciones.c.id_asociacion == reu.id_asociacion)).fetchone()
        if not result_asoc:
            raise HTTPException(status_code=400, detail="No existe una asociacion con ese ID")

        result_asist = conn.execute(vecinos.select().where(vecinos.c.dni == reu.asist1_dni, vecinos.c.id_asociacion == reu.id_asociacion)).fetchone()
        if not result_asist:
            raise HTTPException(status_code=400, detail=f"El DNI {reu.asist1_dni} no pertenece a la asociación {reu.id_asociacion}")

        new_reunion = reu.model_dump()
        conn.execute(reuniones.insert().values(new_reunion))
        conn.commit()
        return "Reunion correctamente añadida"

# Mostrar la lista de reuniones de una asociacion
@reunion1_router.get('/reunion/{id_asociacion}', response_model=List[reunion], tags=['Reunion'], dependencies=[Depends(get_api_key)])
def mostrar_reunion_id_asociacion(id_asociacion: str):
    with engine.connect() as conn:
        result = conn.execute(reuniones.select().where(reuniones.c.id_asociacion == id_asociacion)).fetchall()
        query = conn.execute(reuniones.select().where(reuniones.c.id_asociacion == id_asociacion)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Lista de reuniones no encontrada en esa asociacion")
        else:
            return result

# Mostrar la lista de reuniones pendientes de una asociacion
@reunion1_router.get('/reunion/pendiente/{id_asociacion}', response_model=List[reunion], tags=['Reunion'], dependencies=[Depends(get_api_key)])
def mostrar_reunion_pendiente_id_asociacion(id_asociacion: str):
    with engine.connect() as conn:
        result = conn.execute(reuniones.select().where(reuniones.c.id_asociacion == id_asociacion, reuniones.c.reu_realizada == False)).fetchall()
        query = conn.execute(reuniones.select().where(reuniones.c.id_asociacion == id_asociacion, reuniones.c.reu_realizada == False)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="No hay reuniones pendientes en la asociacion")
        else:
            return result

# Mostrar la lista de reuniones realizadas de una asociacion
@reunion1_router.get('/reunion/realizada/{id_asociacion}', response_model=List[reunion], tags=['Reunion'], dependencies=[Depends(get_api_key)])
def mostrar_reunion_realizada_id_asociacion(id_asociacion: str):
    with engine.connect() as conn:
        result = conn.execute(reuniones.select().where(reuniones.c.id_asociacion == id_asociacion, reuniones.c.reu_realizada == True)).fetchall()
        query = conn.execute(reuniones.select().where(reuniones.c.id_asociacion == id_asociacion, reuniones.c.reu_realizada == True)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="No hay reuniones realizadas en la asociacion")
        else:
            return result

# Actualizar los datos de una reunion
@reunion1_router.put('/reunion/{id_reunion}', tags=['Reunion'], response_model=act_reu, dependencies=[Depends(get_api_key)])
def actualizar_pag(id_reunion: int, actreu: act_reu):
    with engine.connect() as conn:
        conn.execute(reuniones.update().values(hora_reunion=actreu.hora_reunion, fecha_reunion=actreu.fecha_reunion, asunto_reunion=actreu.asunto_reunion, reu_realizada=actreu.reu_realizada, asist1=actreu.asist1, asist1_dni=actreu.asist1_dni).where(reuniones.c.id_reunion == id_reunion))
        conn.commit()
        result = conn.execute(reuniones.select().where(reuniones.c.id_reunion == id_reunion)).first()
        query = conn.execute(reuniones.select().where(reuniones.c.id_reunion == id_reunion)).fetchone()

        result_asist = conn.execute(vecinos.select().where(vecinos.c.dni == actreu.asist1_dni, vecinos.c.id_asociacion == actreu.id_asociacion)).fetchone()
        if not result_asist:
            raise HTTPException(status_code=400, detail=f"El DNI {actreu.asist1_dni} no pertenece a la asociación {actreu.id_asociacion}")

        if not query:
            raise HTTPException(status_code=404, detail="Reunion no encontrada con ID")
        else:
            return result

# Eliminar una reunion
@reunion1_router.delete('/reunion/{id_reunion}', tags=['Reunion'], status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
def delete_pag(id_reunion: int):
    with engine.connect() as conn:
        conn.execute(reuniones.delete().where(reuniones.c.id_reunion == id_reunion))
        conn.commit()
        query = conn.execute(reuniones.select().where(reuniones.c.id_reunion == id_reunion)).fetchone()
        if query:
            raise HTTPException(status_code=404, detail="Reunion no encontrada con ID")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
