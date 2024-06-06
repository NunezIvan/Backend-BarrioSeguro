from fastapi import FastAPI
from src.routers.asociacion_vecinal_routers import asociacion_router
from src.routers.vecinos_routers1 import vecinos1_router
from src.routers.asociacion_routers1 import asociacion1_router
app = FastAPI()
app.include_router(router=vecinos1_router)
app.include_router(router= asociacion_router)
app.include_router(router=asociacion1_router)
app.title = "API de BarrioSeguro"
app.version = "1.0.1"



