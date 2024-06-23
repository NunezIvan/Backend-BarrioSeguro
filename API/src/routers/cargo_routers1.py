from typing import List
from src.schema.cargo_schema import cargo_asoc, cargo_update
from fastapi import APIRouter, HTTPException, Response, Depends
from src.config.db import engine
from src.models.BarrioSeguro_model import cargo, vecinos
from sqlalchemy.sql import select
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from datetime import date
from src.config.utils import get_api_key 

cargo1_router = APIRouter()

# Crear un cargo
@cargo1_router.post('/cargo', status_code=HTTP_201_CREATED, tags=['Cargos'], dependencies=[Depends(get_api_key)])
def create_cargo(cargos: cargo_asoc):
    with engine.connect() as conn:
        result_dni = conn.execute(cargo.select().where(cargo.c.vecino_dni == cargos.vecino_dni)).fetchone()
        if result_dni:
            raise HTTPException(status_code=400, detail=f"El DNI {cargos.vecino_dni} ya tiene cargo")

        result_asoc = conn.execute(vecinos.select().where(vecinos.c.dni == cargos.vecino_dni, vecinos.c.id_asociacion == cargos.id_asociacion)).first()
        if not result_asoc:
            raise HTTPException(status_code=400, detail=f"El DNI {cargos.vecino_dni} no pertenece a la asociación {cargos.id_asociacion}")

        if cargos.nombre_cargo.lower() in ['director', 'secretario', 'tesorero', 'vecino']:
            if cargos.nombre_cargo.lower() in ['director', 'secretario']:
                result_cargo = conn.execute(cargo.select().where(cargo.c.nombre_cargo == cargos.nombre_cargo, cargo.c.fecha_fin >= date.today(), cargo.c.id_asociacion == cargos.id_asociacion)).fetchone()
                if result_cargo:
                    raise HTTPException(status_code=400, detail=f"Ya existe un cargo activo de {cargos.nombre_cargo}")
        else:
            raise HTTPException(status_code=400, detail=f"No existe un cargo llamado {cargos.nombre_cargo}")

        new_cargo = cargos.model_dump()
        conn.execute(cargo.insert().values(new_cargo))
        conn.commit()
        return "Cargo añadido correctamente"

# Mostrar lista de cargos
@cargo1_router.get('/cargo', tags=['Cargos'], response_model=List[cargo_asoc], dependencies=[Depends(get_api_key)])
def mostrar_cargos():
    with engine.connect() as conn:
        result = conn.execute(cargo.select()).fetchall()
        return result

# Mostrar lista de cargos de una asociación
@cargo1_router.get('/cargo/{id_asociacion}', response_model=List[cargo_asoc], tags=['Cargos'], dependencies=[Depends(get_api_key)])
def mostrar_cargos_id_asoc(id_asoc: str):
    with engine.connect() as conn:
        result = conn.execute(cargo.select().where(cargo.c.id_asociacion == id_asoc)).fetchall()
        query = conn.execute(cargo.select().where(cargo.c.id_asociacion == id_asoc)).fetchone()
        if not query:
            raise HTTPException(status_code=404, detail="Lista de cargos no encontrada con ese ID de la Asociación")
        else:
            return result

# Actualizar los datos de un cargo
@cargo1_router.put('/cargo/{id_cargo}', tags=['Cargos'], response_model=cargo_update, dependencies=[Depends(get_api_key)])
def actualizar_cargo(id_cargo: int, actcargo: cargo_update):
    with engine.connect() as conn:
        current_cargo = conn.execute(cargo.select().where(cargo.c.id_cargo == id_cargo)).fetchone()
        if not current_cargo:
            raise HTTPException(status_code=404, detail="Cargo no encontrado con ese ID")

        if actcargo.nombre_cargo.lower() in ['director', 'secretario', 'tesorero', 'vecino']:
            if actcargo.nombre_cargo.lower() in ['director', 'secretario']:
                result_cargo = conn.execute(cargo.select().where(cargo.c.nombre_cargo == actcargo.nombre_cargo, cargo.c.fecha_fin >= date.today(), cargo.c.id_asociacion == current_cargo.id_asociacion)).fetchone()
                if result_cargo:
                    raise HTTPException(status_code=400, detail=f"Ya existe un cargo activo de {actcargo.nombre_cargo} en la asociación {current_cargo.id_asociacion}")

        conn.execute(cargo.update().values(nombre_cargo=actcargo.nombre_cargo, fecha_fin=actcargo.fecha_fin, sueldo=actcargo.sueldo).where(cargo.c.id_cargo == id_cargo))
        conn.commit()

        result = conn.execute(cargo.select().where(cargo.c.id_cargo == id_cargo)).fetchone()
        return result

# Eliminar un cargo
@cargo1_router.delete('/cargo/{id_cargo}', tags=['Cargos'], status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
def delete_cargo(id_cargo: int):
    with engine.connect() as conn:
        conn.execute(cargo.delete().where(cargo.c.id_cargo == id_cargo))
        conn.commit()
        query = conn.execute(cargo.select().where(cargo.c.id_cargo == id_cargo)).fetchone()
        if query:
            raise HTTPException(status_code=404, detail="Cargo no encontrado con ese ID")
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
