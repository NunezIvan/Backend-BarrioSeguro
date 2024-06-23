from typing import List
from src.schema.acuerdo_schema import acuerdo_reu,updt_acuerdo
from fastapi import APIRouter,HTTPException,Response,Depends
from src.config.db import engine
from src.models.BarrioSeguro_model import acuerdos,reuniones
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from sqlalchemy.sql import select
from src.config.utils import get_api_key 

acuerdo1_router = APIRouter()

#Crear un acuerdo
@acuerdo1_router.post('/acuerdo',status_code=HTTP_201_CREATED,tags=['Acuerdo'], dependencies=[Depends(get_api_key)])
def create_acuerdo(acuerdo1:acuerdo_reu):
    with engine.connect() as conn:
        query = select(acuerdos).where(acuerdos.c.id_acuerdo == acuerdo1.id_acuerdo)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Ya existe un acuerdo con ese ID")

        result_reu = conn.execute(reuniones.select().where(reuniones.c.id_reunion == acuerdo1.id_reunion)).fetchone()
        if  not result_reu:
            raise HTTPException(status_code=400, detail="No existe una reunion con ese ID de reunion")

        new_acuerdo = acuerdo1.model_dump()
        conn.execute(acuerdos.insert().values(new_acuerdo))
        conn.commit()
        return "Acuerdo correctamente añadido"
    
#Mostrar lista de encuesta de una reunion
@acuerdo1_router.get('/acuerdo/{id_reunion}',response_model=List[acuerdo_reu],tags=['Acuerdo'], dependencies=[Depends(get_api_key)])
def mostrar_acuerdo_id_acuerdo(id_reunion:str):
    with engine.connect() as conn:
        result = conn.execute(acuerdos.select().where(acuerdos.c.id_reunion == id_reunion)).fetchall()
        query=conn.execute(acuerdos.select().where(acuerdos.c.id_reunion == id_reunion)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Lista de acuerdos no encontrada en esa reunion")
        else:
            return result
        
#Actualizar los datos de un acuerdo
@acuerdo1_router.put('/acuerdo/{id_acuerdo}', tags=['Acuerdo'],response_model=updt_acuerdo, dependencies=[Depends(get_api_key)])
def actualizar_acuerdo(id_acuerdo:int, actacuerdo:updt_acuerdo):
    with engine.connect() as conn:
        conn.execute(acuerdos.update().values(titulo=actacuerdo.titulo, descripcion=actacuerdo.descripcion).where(acuerdos.c.id_acuerdo == id_acuerdo))
        conn.commit()
        result = conn.execute(acuerdos.select().where(acuerdos.c.id_acuerdo == id_acuerdo)).first()
        query=conn.execute(acuerdos.select().where(acuerdos.c.id_acuerdo == id_acuerdo)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Acuerdo no encontrado con ID")
        else:
            return result
        
#Eliminar un acuerdo
@acuerdo1_router.delete('/acuerdo/{id_acuerdo}',tags=['Acuerdo'],status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
def delete_acuerdo(id_acuerdo:int):
    with engine.connect() as conn:
        conn.execute(acuerdos.delete().where(acuerdos.c.id_acuerdo == id_acuerdo))
        conn.commit()
        query=conn.execute(acuerdos.select().where(acuerdos.c.id_acuerdo == id_acuerdo)).fetchone()
        if query:
            raise HTTPException(status_code=404, detail="Acuerdo no encontrado con ID")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)