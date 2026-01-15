from pydantic import BaseModel

class config: orm_mode = True

class UsuarioCrear(BaseModel):
    nombre: str
    correo: str
    contraseña: str

class HijoCrear(BaseModel):
    nombre: str
    edad: str
    autismo: str
    DatosExtra: str = None

class ArticuloCrear(BaseModel):
    titulo: str
    autor: str = None
    fuente: str = None
    fecha: str = None
    parrafo: str

class EspecialistaCrear(BaseModel):
    nombre: str
    cedula: str
    correo: str
    contraseña: str
    instituto: str
    especialidad: str
    comprobante: str
    estado: str

class FamiliaCrear(BaseModel):

    Padre: UsuarioCrear
    Hijo: HijoCrear