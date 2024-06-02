from typing import List
from src.models.asociacion_vecinal_models import asociacion_vecinal
from fastapi import APIRouter

asociacion_router=APIRouter()

asociacion=[]

@asociacion_router.post('/asociacion',tags=['Asociacion Vecinal'])
def crear_asociacion(asoc:asociacion_vecinal):
    asociacion.append(asoc.model_dump())
    return asociacion

@asociacion_router.get('/asociacion',tags=['Asociacion Vecinal'])
def mostrar_asociacion() -> List[asociacion_vecinal]:
    return asociacion