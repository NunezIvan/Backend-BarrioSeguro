from typing import List
from src.models.vecinos_models import VecinoDB,VecinoUpdate
from fastapi import APIRouter, Depends, HTTPException,Body
from fastapi.security import OAuth2PasswordRequestForm

vecino_router=APIRouter()

vecinos: List[VecinoDB] = [
  {
    "dni": "72196732",
    "nombre": "Ivan Joaquin",
    "apellido": "Nuñez Cardenas",
    "num_celular": "stringstr",
    "direccion": "string",
    "genero": "Masculino",
    "clas_vecino": "Excelente",
    "id_asociacion": "A001",
    "id_cargo": "Vecino",
    "correo": "nunezivan2@gmail.com",
    "password": "12345"
  },
  {
    "dni": "72196738",
    "nombre": "Kevin Rodrigo",
    "apellido": "Nuñez Cardenas",
    "num_celular": "982974756",
    "direccion": "Paraiso Florido",
    "genero": "Masculino",
    "clas_vecino": "Excelente",
    "id_asociacion": "A001",
    "id_cargo": "Vecino",
    "correo": "nunezivan124@gmail.com",
    "password": "12345"
  },
  {
    "dni": "72196731",
    "nombre": "Luis David",
    "apellido": "Nuñez Cardenas",
    "num_celular": "982974756",
    "direccion": "Paraiso Florido",
    "genero": "Masculino",
    "clas_vecino": "Excelente",
    "id_asociacion": "A001",
    "id_cargo": "Vecino",
    "correo": "nunezivan124@gmail.com",
    "password": "12345"
  }
]

#Crear un vecino
@vecino_router.post('/vecino', tags=['Vecino'])
def crear_vecino(vecino: VecinoDB):
    # Verificación de DNI duplicado
    for vecino_existente in vecinos:
        if vecino_existente['dni'] == vecino.model_dump()['dni']:
            raise HTTPException(status_code=400, detail="Ya existe un vecino con este DNI")
    # Verificación de nombres duplicados
        if vecino_existente['nombre'] == vecino.model_dump()['nombre'] and vecino_existente['apellido'] == vecino.model_dump()['apellido']:
            raise HTTPException(status_code=400, detail="Ya existe un vecino con el mismo nombre completo")
    
    vecinos.append(vecino.model_dump())
    return vecinos


#Mostrar la lista de vecinos
@vecino_router.get('/vecino',tags=['Vecino'])
def mostrar_vecino() -> List[VecinoDB]:
    return vecinos

#Buscar un vecino mediante el ingreso del dni
@vecino_router.get('/vecino/{dni}',tags=['Vecino'])
def mostrar_vecino_dni(dni:str):
    for vecino in vecinos:
        if vecino['dni']==dni:
            return vecino

        
#Actualizar datos del vecino:
@vecino_router.put('/vecino/{dni}', tags=['Vecino'])
def actualizar_vecino(dni: str, actualizacion: VecinoUpdate = Body(...)):
    for vecino in vecinos:
        if vecino['dni'] == dni:
            vecino['direccion'] = actualizacion.direccion
            vecino['num_celular']= actualizacion.num_celular
            vecino['correo'] = actualizacion.correo
            return vecino
    raise HTTPException(status_code=404, detail="Vecino no encontrado")

#Eliminar a un vecino:
@vecino_router.delete('/vecino/{dni}', tags=['Vecino'])
def eliminar_vecino(dni: str): 
    for i, vecino in enumerate(vecinos):
        if vecino['dni'] == dni:
            del vecinos[i] 
            return vecinos
    raise HTTPException(status_code=404, detail="Vecino no encontrado")


#Autentificacion de vecinos
def autentificar_vecino(dni:str, password:str):
    for vecino in vecinos:
        if vecino['dni'] == dni and vecino['password']==password:
            return vecino

@vecino_router.post('/login',tags=['Login'])
async def login(form: OAuth2PasswordRequestForm = Depends()):
    vecino = autentificar_vecino(form.username, form.password)
    if not vecino:
         raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    return {"access_token": vecino['dni'], "token_type": "bearer"}
