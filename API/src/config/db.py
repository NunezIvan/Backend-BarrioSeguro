from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Obtener las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear la conexión a la base de datos
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

meta_data = MetaData()

