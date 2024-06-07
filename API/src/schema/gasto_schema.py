from pydantic import BaseModel
from datetime import date
class gasto_asoc(BaseModel):
    id_gasto:int
    fecha_gasto:date
    tit_gasto:str
    monto_gastado:float
    id_asociacion:str | None = None

class gasto_up(BaseModel):
    tit_gasto:str
    fecha_gasto:date
    