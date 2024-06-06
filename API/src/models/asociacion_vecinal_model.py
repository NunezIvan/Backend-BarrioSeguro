from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String
from src.config.db import engine,meta_data

asociacion = Table("asociacion_vecinal",meta_data,
                   Column("id_asociacion",String(6),primary_key=True),
                   Column("nombre",String(60), nullable=False),
                   Column("distrito",String(40),nullable=False),
                   Column("provincia",String(40),nullable=False),
                   Column("est_plus",String(2),nullable=False),
                   Column("membresia",Integer,nullable=False),
                   Column("nombre_creador",String(50),nullable=False))


meta_data.create_all(engine)