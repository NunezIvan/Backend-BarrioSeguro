from pydantic import BaseModel, Field
from typing import Optional

class Vecino(BaseModel):
    dni:str = Field(min_length=8,max_length=8)
    nombre:str
    apellido:str
    num_celular:str = Field(min_length=9,max_length=9)
    direccion:str
    genero:str
    clas_vecino:str
    id_asociacion:Optional[str]=None
    id_cargo:Optional[str]=None
    correo:str

class VecinoDB(Vecino):
    password:str

class VecinoUpdate(BaseModel):
    correo:str
    num_celular:str = Field(min_length=9,max_length=9)
    direccion:str