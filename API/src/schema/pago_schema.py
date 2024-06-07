from pydantic import BaseModel
from datetime import date,time

class pago_vecino(BaseModel):
    id_pago:int
    vecino_dni:int
    fecha_pago:date
    hora_pago:time
    monto_pago:float
    metodo_pago:str
    cancel_pago:bool

class pago_update(BaseModel):
    fecha_pago:date
    hora_pago:time
    monto_pago:float
    metodo_pago:str
    cancel_pago:bool

