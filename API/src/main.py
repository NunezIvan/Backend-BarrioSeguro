from fastapi import FastAPI
from src.routers.vecinos_routers1 import vecinos1_router
from src.routers.asociacion_routers1 import asociacion1_router
from src.routers.gasto_routers1 import gasto1_router
from src.routers.cargo_routers1 import cargo1_router
from src.routers.seguridad_routers1 import seguridad1_router
from src.routers.pago_routers1 import pago1_router
from src.routers.reunion_routers1 import reunion1_router
from src.routers.encuesta_routers1 import encuesta1_router
from src.routers.acuerdo_routers1 import acuerdo1_router
app = FastAPI()
app.include_router(router=vecinos1_router)
app.include_router(router=asociacion1_router)
app.include_router(router=gasto1_router)
app.include_router(router=cargo1_router)
app.include_router(router=seguridad1_router)
app.include_router(router=pago1_router)
app.include_router(router=reunion1_router)
app.include_router(router=encuesta1_router)
app.include_router(router=acuerdo1_router)
app.title = "API de BarrioSeguro"
app.version = "1.0.1"



