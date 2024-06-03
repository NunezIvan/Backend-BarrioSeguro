from fastapi import FastAPI
from src.routers.vecinos_routers import vecino_router
from src.routers.asociacion_vecinal_routers import asociacion_router
app = FastAPI()
app.include_router(router= vecino_router)
app.include_router(router= asociacion_router)
app.title = "API de BarrioSeguro"
app.version = "1.0.0"



