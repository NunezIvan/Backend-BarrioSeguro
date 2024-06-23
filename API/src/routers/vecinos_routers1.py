from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.sql import select
from werkzeug.security import generate_password_hash, check_password_hash
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List, Optional
from src.schema.vecinos_schema import VecinoDB, VecinoUpdate, loginVecino
from src.config.db import engine
from src.models.BarrioSeguro_model import vecinos
from src.config.utils import get_api_key  

vecinos1_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="vecinos/login")

# Configuración de JWT
SECRET_KEY = "TuClaveSecretaSuperSecreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password):
    return generate_password_hash(password, "pbkdf2:sha256:30", 30)

def verify_password(plain_password, hashed_password):
    return check_password_hash(hashed_password, plain_password)

def authenticate_user(dni: int, password: str):
    with engine.connect() as conn:
        user = conn.execute(select(vecinos).where(vecinos.c.dni == dni)).first()
        if not user:
            return False
        if not verify_password(password, user.contraseña):
            return False
        return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Crear un vecino
@vecinos1_router.post('/vecinos', status_code=HTTP_201_CREATED, tags=['Vecinos'], dependencies=[Depends(get_api_key)])
def create_vecino(vecino: VecinoDB):
    with engine.connect() as conn:
        query = select(vecinos).where(vecinos.c.dni == vecino.dni)
        result = conn.execute(query).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="Vecino ya existe con ese DNI")

        new_vecino = vecino.model_dump()
        new_vecino["contraseña"] = get_password_hash(vecino.contraseña)
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
@vecinos1_router.post("/vecinos/login", tags=['Vecinos'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="DNI o Contraseña Incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str('user.dni')}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}