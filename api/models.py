from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class Usuario(Base):
   
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key = True, index = True) 
    nombre = Column(String, index = True)
    correo = Column(String, unique = True, index = True) 
    contraseña = Column(String) 
    Hijo = relationship("Hijo", back_populates = "Padre")

class Hijo(Base):

    __tablename__ = "hijos"

    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String, index = True)
    edad = Column(String, index = True)
    autismo = Column(String, index = True)
    DatosExtra = Column(String, index = True)
    padre_id = Column(Integer, ForeignKey("usuarios.id"), index = True)
    Padre = relationship("Usuario", back_populates = "Hijo")

class IniciarSesion(BaseModel):

    correo: str
    contraseña: str

class Articulos(Base):

    __tablename__ = "Articulo"

    id = Column(Integer, primary_key = True, index = True)
    titulo = Column(String, index = True)
    autor = Column(String, nullable = True)
    fuente = Column(String, nullable = True)
    fecha = Column(String, nullable = True)
    parrafo = Column(String)

class Especialistas(Base):

    __tablename__ = "Especialista"

    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String, index = True)
    cedula = Column(Integer, index = True, unique = True)
    correo = Column(String, index = True, unique = True)
    contraseña = Column(String, index = True)
    Instituto = Column(String, index = True)
    especialidad = Column(String, index = True)
    Comprobante = Column(String, index = True)
    estado = Column(String, index = True)

