from sqlalchemy import Table,Column,ForeignKey
from sqlalchemy.sql.sqltypes import Integer,String,Date,Float,Time,Boolean
from src.config.db import engine,meta_data

vecinos = Table("Vecinos",meta_data, 
              Column("dni",Integer,primary_key=True,autoincrement=False),
              Column("nombre",String(45),nullable=False),
              Column("apellido",String(45),nullable=False),
              Column("direccion",String(180),nullable=False),
              Column("genero",String(10),nullable=False),
              Column("clas_vecino",String(12),nullable=False),
              Column("id_asociacion",String(6),ForeignKey('asociacion_vecinal.id_asociacion'),nullable=True),
              Column("num_celular",String(9),nullable=False),
              Column("correo",String(45),nullable=False),       
              Column("contraseña",String(200),nullable=False))



asociaciones = Table("asociacion_vecinal",meta_data,
                   Column("id_asociacion",String(6),primary_key=True),
                   Column("nombre",String(60), nullable=False),
                   Column("distrito",String(40),nullable=False),
                   Column("provincia",String(40),nullable=False),
                   Column("est_plus",String(1),nullable=False),
                   Column("membresia",Integer,nullable=False),
                   Column("nombre_creador",String(50),nullable=False))



gastos = Table("gasto" , meta_data,
               Column("id_gasto",Integer,primary_key=True,autoincrement=True),
               Column("fecha_gasto",Date,nullable=False),
               Column("tit_gasto",String(180), nullable=False),
               Column("monto_gastado",Float,nullable=False),
               Column("id_asociacion",String(6),ForeignKey('asociacion_vecinal.id_asociacion'),nullable=False))



cargo = Table("cargo", meta_data, 
              Column("id_cargo",Integer,primary_key=True,autoincrement=True),
              Column("nombre_cargo",String(20),nullable=False),
              Column("fecha_inicio",Date,nullable=False),
              Column("fecha_fin",Date,nullable=False),
              Column("sueldo",Integer,nullable=False),
              Column("vecino_dni",Integer,ForeignKey('Vecinos.dni'),nullable=False),
              Column("id_asociacion",String(6),ForeignKey('Vecinos.id_asociacion'),nullable=False))



security = Table("seguridad",meta_data,
                 Column("dni",Integer,primary_key=True,autoincrement=False),
                 Column("nombre",String(25),nullable=False),
                 Column("apellido",String(35),nullable=False),
                 Column("num_celular",String(9),nullable=False),
                 Column("salario",Integer,nullable=False,autoincrement=False),
                 Column("fecha_inicio",Date,nullable=False),
                 Column("fecha_fin",Date,nullable=False),
                 Column("id_asociacion",String(6),ForeignKey('asociacion_vecinal.id_asociacion'),nullable=False))



pagos = Table("pago" , meta_data,
              Column("id_pago",Integer,primary_key=True,autoincrement=True),
              Column("vecino_dni",Integer,ForeignKey('Vecinos.dni'),nullable=False,autoincrement=False),
              Column("fecha_pago",Date,nullable=False),
              Column("hora_pago",Time,nullable=False),
              Column("monto_pago",Float,nullable=False),
              Column("metodo_pago",String(35),nullable=False),
              Column("cancel_pago",Boolean,nullable=False))



reuniones = Table("reunion", meta_data,
                   Column("id_reunion",String(6),primary_key=True),
                   Column("hora_reunion",Time,nullable=False),
                   Column("fecha_reunion",Date,nullable=False),
                   Column("asunto_reunion",String(50),nullable=False),
                   Column("id_asociacion",String(6),ForeignKey('asociacion_vecinal.id_asociacion'),nullable=False),
                   Column("reu_realizada",Boolean,nullable=False),
                   Column("asist1",String(90),nullable=False),
                   Column("asist1_dni",Integer,ForeignKey('Vecinos.dni'),nullable=False))



encuestas = Table("encuesta",meta_data,
                  Column("id_encuesta",Integer,primary_key=True,autoincrement=True),
                  Column("titulo",String(100),nullable=False),
                  Column("opc_win",String(50),nullable=True),
                  Column("vot_total",Integer,nullable=False),
                  Column("fecha_inicio",Date,nullable=False),
                  Column("fecha_fin",Date,nullable=False),
                  Column("hora_encuesta",Time,nullable=False),
                  Column("id_asociacion",String(6),ForeignKey('asociacion_vecinal.id_asociacion'),nullable=False))




acuerdos = Table("acuerdo", meta_data,
                 Column("id_acuerdo",Integer,primary_key=True,autoincrement=True),
                 Column("titulo",String(100),nullable=False),
                 Column("descripcion",String(250),nullable=False),
                 Column("id_reunion",String(6),ForeignKey('reunion.id_reunion'),nullable=False))




meta_data.create_all(engine)

