from pydantic import BaseModel
from datetime import date,time

class reunion(BaseModel):
    id_reunion:str
    hora_reunion:time
    fecha_reunion:date
    asunto_reunion:str
    id_asociacion:str
    reu_realizada:bool
    asist1:str
    asist1_dni:int

class act_reu(BaseModel):
    hora_reunion:time
    fecha_reunion:date
    asunto_reunion:str
    reu_realizada:bool
    asist1:str
    asist1_dni:int
