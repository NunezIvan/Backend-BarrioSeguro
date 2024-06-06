from pydantic import BaseModel
from typing import Optional

class Vecino(BaseModel):
    dni:int 
    nombre:str
    apellido:str
    direccion:str
    genero:str
    clas_vecino:str
    id_asociacion:str | None = None
    num_celular:str 
    correo:str

class VecinoDB(Vecino):
    contraseña:str

class VecinoUpdate(BaseModel):
    correo:str
    num_celular:str 
    direccion:str
    id_asociacion:str | None = None
    contraseña:str

class loginVecino(BaseModel):
    dni:int
    contraseña:str