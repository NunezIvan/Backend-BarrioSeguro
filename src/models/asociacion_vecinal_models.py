from pydantic import BaseModel, Field
class asociacion_vecinal(BaseModel):
    id_asociacion:str
    nombre:str
    distrito:str
    provincia:str
    est_plus:bool
    membresia:int
    