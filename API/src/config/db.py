from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:KazumaHumilde123@localhost:3306/DB_BarrioSeguro",pool_pre_ping=True)

meta_data = MetaData()


