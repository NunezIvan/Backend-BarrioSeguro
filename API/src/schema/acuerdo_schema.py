from pydantic import BaseModel

class acuerdo_reu(BaseModel):
    id_acuerdo:int
    titulo:str
    descripcion:str
    id_reunion:str

class updt_acuerdo(BaseModel):
    titulo:str
    descripcion:str