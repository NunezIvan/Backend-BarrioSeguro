from typing import List
from src.schema.asociacion_vecinal_schema import asociacion_vecinal,update_asociacion
from fastapi import APIRouter,Body,HTTPException

asociacion_router=APIRouter()

asociacion=[]

#Crear Asociacion Vecinal
@asociacion_router.post('/asociacion', tags=['Asociacion Vecinal'])
def crear_asociacion(asoc: asociacion_vecinal):
    for asociacion_existente in asociacion:
        if asociacion_existente['nombre_creador'] == asoc.model_dump()['nombre_creador']:
            raise HTTPException(status_code=400, detail="Esta persona ya creo una asociacion vecinal")
    asociacion.append(asoc.model_dump())
    return asociacion

#Mostrar Asociacion Vecinal
@asociacion_router.get('/asociacion',tags=['Asociacion Vecinal'])
def mostrar_asociacion() -> List[asociacion_vecinal]:
    return asociacion

#Buscar una Asociacion Vecinal mediante el ingreso del id
@asociacion_router.get('/asociacion/{id_asociacion}',tags=['Asociacion Vecinal'])
def mostrar_asociacion_id(id_asociacion:str):
    for asociaciones in asociacion:
        if asociaciones['id_asociacion']==id_asociacion:
            return asociacion
        
#Actualizar datos de la Asociacion Vecinal:
@asociacion_router.put('/asociacion/{id_asociacion}', tags=['Asociacion Vecinal'])
def actualizar_asociacion(id_asociacion:str, actualizacion: update_asociacion = Body(...)):
    for asociaciones in asociacion:
        if asociaciones['id_asociacion'] == id_asociacion:
            asociaciones['distrito'] = actualizacion.distrito
            asociaciones['provincia']= actualizacion.provincia
            return asociaciones
    raise HTTPException(status_code=404, detail="Asociacion Vecinal no encontrada")

#Eliminar a una Asociacion Vecinal:
@asociacion_router.delete('/asociacion/{id_asociacion}', tags=['Asociacion Vecinal'])
def eliminar_vecino(id_asociacion: str): 
    for i, asociaciones in enumerate(asociacion):
        if asociaciones['id_asociacion'] == id_asociacion:
            del asociacion[i] 
            return asociacion
    raise HTTPException(status_code=404, detail="Asociacion Vecinal no encontrada")