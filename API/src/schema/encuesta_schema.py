from pydantic import BaseModel
from datetime import date,time

class encuesta_asoc(BaseModel):
    id_encuesta:int
    titulo:str
    opc_win:str | None = None
    vot_total:int
    fecha_inicio:date
    fecha_fin:date 
    hora_encuesta:time
    id_asociacion:str


class updt_encuesta(BaseModel):
    titulo:str
    opc_win:str
    vot_total:int
    fecha_fin:date 