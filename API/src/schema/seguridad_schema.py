from pydantic import BaseModel
from datetime import date

class seguridad(BaseModel):
    dni:int
    nombre:str
    apellido:str
    num_celular:str
    salario:int
    fecha_inicio:date
    fecha_fin:date
    id_asociacion:str

class update_sec(BaseModel):
    num_celular:str
    salario:int
    fecha_fin:date