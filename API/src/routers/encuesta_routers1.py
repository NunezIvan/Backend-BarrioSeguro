from typing import List
from src.schema.encuesta_schema import encuesta_asoc,updt_encuesta
from fastapi import APIRouter,HTTPException,Response
from src.config.db import engine
from src.models.BarrioSeguro_model import encuestas,asociaciones
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from sqlalchemy.sql import select

encuesta1_router = APIRouter()

#Crear un encuesta
@encuesta1_router.post('/encuesta',status_code=HTTP_201_CREATED,tags=['Encuesta'])
def create_encuesta(encuesta1:encuesta_asoc):
    with engine.connect() as conn:
        query = select(encuestas).where(encuestas.c.id_encuesta == encuesta1.id_encuesta)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Ya existe una encuesta con ese ID")

        result_asoc = conn.execute(asociaciones.select().where(asociaciones.c.id_asociacion == encuesta1.id_asociacion)).fetchone()
        if  not result_asoc:
            raise HTTPException(status_code=400, detail="No existe una asociacion con ese ID")

        new_encuesta = encuesta1.model_dump()
        conn.execute(encuestas.insert().values(new_encuesta))
        conn.commit()
        return "Encuesta correctamente añadida"
    
#Mostrar lista de encuesta de una asociacion
@encuesta1_router.get('/encuesta/{id_asociacion}',response_model=List[encuesta_asoc],tags=['Encuesta'])
def mostrar_encuesta_id_asociacion(id_asociacion:str):
    with engine.connect() as conn:
        result = conn.execute(encuestas.select().where(encuestas.c.id_asociacion == id_asociacion)).fetchall()
        query=conn.execute(encuestas.select().where(encuestas.c.id_asociacion == id_asociacion)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Lista de encuestas no encontrada en esa asociacion")
        else:
            return result

#Actualizar los datos de una encuesta
@encuesta1_router.put('/encuesta/{id_encuesta}', tags=['Encuesta'],response_model=updt_encuesta)
def actualizar_encuesta(id_encuesta:int, actenc:updt_encuesta):
    with engine.connect() as conn:
        conn.execute(encuestas.update().values(titulo=actenc.titulo, opc_win=actenc.opc_win, vot_total=actenc.vot_total, fecha_fin=actenc.fecha_fin).where(encuestas.c.id_encuesta == id_encuesta))
        conn.commit()
        result = conn.execute(encuestas.select().where(encuestas.c.id_encuesta == id_encuesta)).first()
        query=conn.execute(encuestas.select().where(encuestas.c.id_encuesta == id_encuesta)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Encuesta no encontrada con ID")
        else:
            return result

#Eliminar una encuesta
@encuesta1_router.delete('/encuesta/{id_encuesta}',tags=['Encuesta'],status_code=HTTP_204_NO_CONTENT)
def delete_encuesta(id_encuesta:int):
    with engine.connect() as conn:
        conn.execute(encuestas.delete().where(encuestas.c.id_encuesta == id_encuesta))
        conn.commit()
        query=conn.execute(encuestas.select().where(encuestas.c.id_encuesta == id_encuesta)).fetchone()
        if query:
            raise HTTPException(status_code=404, detail="Reunion no encontrada con ID")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)




