# src/routers/vecinos_routers1.py

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.sql import select
from werkzeug.security import generate_password_hash, check_password_hash
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
from src.schema.vecinos_schema import VecinoDB, VecinoUpdate, loginVecino
from src.config.db import engine
from src.models.BarrioSeguro_model import vecinos
from src.config.utils import get_api_key  

vecinos1_router = APIRouter()

# Crear un vecino
@vecinos1_router.post('/vecinos', status_code=HTTP_201_CREATED, tags=['Vecinos'], dependencies=[Depends(get_api_key)])
def create_vecino(vecino: VecinoDB):
    with engine.connect() as conn:
        query = select(vecinos).where(vecinos.c.dni == vecino.dni)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Vecino ya existe con ese DNI")

        new_vecino = vecino.model_dump()
        new_vecino["contraseña"] = generate_password_hash(vecino.contraseña, "pbkdf2:sha256:30", 30)
        conn.execute(vecinos.insert().values(new_vecino))
        conn.commit()
        return "Vecino correctamente añadido"

# Mostrar la lista de vecinos
@vecinos1_router.get('/vecinos', tags=['Vecinos'], response_model=List[VecinoDB], dependencies=[Depends(get_api_key)])
def mostrar_vecino():
    with engine.connect() as conn:
        result = conn.execute(vecinos.select()).fetchall()
        return result

# Buscar un vecino mediante el ingreso del dni
@vecinos1_router.get('/vecinos/{vecino_id}', response_model=VecinoDB, tags=['Vecinos'], dependencies=[Depends(get_api_key)])
def mostrar_vecino_id(vecino_id: int):
    with engine.connect() as conn:
        result = conn.execute(vecinos.select().where(vecinos.c.dni == vecino_id)).first()
        query = conn.execute(vecinos.select().where(vecinos.c.dni == vecino_id)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Vecino no encontrado con ese DNI")
        else:
            return result

# Actualizar datos del vecino
@vecinos1_router.put('/vecinos/{vecino_dni}', tags=['Vecinos'], response_model=VecinoUpdate, dependencies=[Depends(get_api_key)])
def actualizar_vecino(vecino_dni: int, act: VecinoUpdate):
    with engine.connect() as conn:
        encryp_pass = generate_password_hash(act.contraseña, "pbkdf2:sha256:30", 30)
        conn.execute(vecinos.update().values(correo=act.correo, num_celular=act.num_celular, direccion=act.direccion, id_asociacion=act.id_asociacion, contraseña=encryp_pass).where(vecinos.c.dni == vecino_dni))
        conn.commit()
        result = conn.execute(vecinos.select().where(vecinos.c.dni == vecino_dni)).first()
        query = conn.execute(vecinos.select().where(vecinos.c.dni == vecino_dni)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Vecino no encontrado con ese DNI")
        else:
            return result

# Eliminar a un vecino
@vecinos1_router.delete('/vecinos/{vecino_dni}', tags=['Vecinos'], status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
def delete_vecino(vecino_dni: int):
    with engine.connect() as conn:
        conn.execute(vecinos.delete().where(vecinos.c.dni == vecino_dni))
        conn.commit()
        query = conn.execute(vecinos.select().where(vecinos.c.dni == vecino_dni)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Vecino no encontrado con ese DNI")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)

# Login de vecinos (con protección de API Key)
@vecinos1_router.post('/vecinos/login', tags=['Vecinos'], status_code=200, dependencies=[Depends(get_api_key)])
def login_vecino(vecino_login: loginVecino):
    with engine.connect() as conn:
        resultado = conn.execute(vecinos.select().where(vecinos.c.dni == vecino_login.dni)).first()
        conn.commit()
        if resultado:
            check_pass = check_password_hash(resultado[9], vecino_login.contraseña)
            if check_pass:
                return {
                    "status": 200,
                    "Message": "Access successful"
                }
        return {
            "status": HTTP_401_UNAUTHORIZED,
            "Message": "Access denied"
        }
