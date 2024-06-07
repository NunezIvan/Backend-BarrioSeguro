from pydantic import BaseModel
from datetime import date
class cargo_asoc(BaseModel):
    id_cargo:int
    nombre_cargo:str
    fecha_inicio:date
    fecha_fin:date
    sueldo:int
    vecino_dni:int
    id_asociacion:str

class cargo_update(BaseModel):
    nombre_cargo:str
    fecha_fin:date
    sueldo:int