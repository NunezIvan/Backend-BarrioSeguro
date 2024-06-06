from typing import List
from src.schema.asociacion_vecinal_schema import asociacion_vecinal,update_asociacion
from fastapi import APIRouter,Body,HTTPException
from src.config.db import engine
from src.models.vecino_model import asociaciones
asociacion1_router=APIRouter()


#Crear una asociacion
@asociacion1_router.post('/asociaciones/')
def create_asociacion(asociacion:asociacion_vecinal):
    with engine.connect() as conn:
        new_asociacion=asociacion.model_dump()
        conn.execute(asociaciones.insert().values(new_asociacion))
        conn.commit()
        return "Success"

