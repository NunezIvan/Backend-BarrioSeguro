from src.schema.vecinos_schema import VecinoDB,VecinoUpdate,loginVecino
from fastapi import APIRouter, HTTPException, Response
from src.config.db import engine
from src.models.BarrioSeguro_model import vecinos 
from sqlalchemy.sql import select
from werkzeug.security import generate_password_hash,check_password_hash
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List

vecinos1_router=APIRouter()

#Crear un vecino
@vecinos1_router.post('/vecinos',status_code=HTTP_201_CREATED,tags=['Vecinos'])
def create_vecino(vecino:VecinoDB):
    with engine.connect() as conn:
        query = select(vecinos).where(vecinos.c.dni == vecino.dni)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Vecino ya existe con ese DNI")

        new_vecino = vecino.model_dump()
        new_vecino["contraseña"]=generate_password_hash(vecino.contraseña,"pbkdf2:sha256:30",30)
        conn.execute(vecinos.insert().values(new_vecino))
        conn.commit()
        return "Vecino correctamente añadido"


#Mostar la lista de vecinos
@vecinos1_router.get('/vecinos',tags=['Vecinos'],response_model=List[VecinoDB])
def mostrar_vecino():
    with engine.connect() as conn:
        result=conn.execute(vecinos.select()).fetchall()
        return result
    
#Buscar un vecino mediante el ingreso del dni
@vecinos1_router.get('/vecinos/{vecino_id}',response_model=VecinoDB,tags=['Vecinos'])
def mostrar_vecino_id(vecino_id:int):
    with engine.connect() as conn:
        result = conn.execute(vecinos.select().where(vecinos.c.dni==vecino_id)).first()
        query=conn.execute(vecinos.select().where(vecinos.c.dni == vecino_id)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Vecino no encontrado con ese DNI")
        else:
            return result
    
#Actualizar datos del vecino:
@vecinos1_router.put('/vecinos/{vecino_dni}',tags=['Vecinos'],response_model=VecinoUpdate)
def actualizar_vecino(vecino_dni:int, act:VecinoUpdate):
    with engine.connect() as conn:
        encryp_pass=generate_password_hash(act.contraseña,"pbkdf2:sha256:30",30)
        conn.execute(vecinos.update().values(correo=act.correo, num_celular=act.num_celular, direccion=act.direccion, id_asociacion=act.id_asociacion, contraseña=encryp_pass).where(vecinos.c.dni == vecino_dni))
        conn.commit()
        result = conn.execute(vecinos.select().where(vecinos.c.dni == vecino_dni)).first()
        query=conn.execute(vecinos.select().where(vecinos.c.dni == vecino_dni)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Vecino no encontrado con ese DNI")
        else:
            return result
        
#Eliminar a un vecino:
@vecinos1_router.delete('/vecinos/{vecino_dni}',tags=['Vecinos'],status_code=HTTP_204_NO_CONTENT)
def delete_vecino(vecino_dni:int):
    with engine.connect() as conn:
        conn.execute(vecinos.delete().where(vecinos.c.dni==vecino_dni))
        conn.commit()
        query=conn.execute(vecinos.select().where(vecinos.c.dni == vecino_dni)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Vecino no encontrado con ese DNI")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
        
#Login de vecinos:
@vecinos1_router.post('/vecinos/login',tags=['Vecinos'],status_code=200)
def login_vecino(vecino_login:loginVecino):
    with engine.connect() as conn:
        resultado = conn.execute(vecinos.select().where(vecinos.c.dni == vecino_login.dni)).first()
        conn.commit()
        if resultado !=None:
            check_pass=check_password_hash(resultado[9],vecino_login.contraseña)
            if check_pass:
                return {
                    "status": 200,
                    "Message": "Access succces"
                }
        return {
                    "status": HTTP_401_UNAUTHORIZED,
                    "Message": "Access denied"
                }
