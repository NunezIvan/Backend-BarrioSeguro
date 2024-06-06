from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:tucontraseña@localhost:3306/tubasededatos",pool_pre_ping=True)

meta_data = MetaData()


