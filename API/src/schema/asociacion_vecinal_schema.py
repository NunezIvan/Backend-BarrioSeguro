from pydantic import BaseModel
class asociacion_vecinal(BaseModel):
    id_asociacion:str
    nombre:str
    distrito:str
    provincia:str
    est_plus:str
    membresia:int
    nombre_creador:str

class update_asociacion(BaseModel):
    nombre:str
    distrito:str
    provincia:str
    