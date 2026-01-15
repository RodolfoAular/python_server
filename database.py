from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


USUARIO = "postgres"
PASSWORD = "Rodolfo.15"  
HOST = "localhost"               
PUERTO = "5432"                  
NOMBRE_DB = "base_datos"           

SQLALCHEMY_DATABASE_URL = f"postgresql://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{NOMBRE_DB}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

print("Configuración de base de datos cargada correctamente. (mensaje de database de python, este soy yo)")