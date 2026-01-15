from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from fastapi.staticfiles import StaticFiles 
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
import shutil, os 
import google.generativeai as genai
import os
from groq import Groq 
from dotenv import load_dotenv

load_dotenv()
IAGroq = os.getenv("GROQ_API_KEY")


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/Imagenes_Tesis", StaticFiles(directory = "Imagenes_Tesis"), name = "Imagenes_Tesis")
def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/Familia/")
def crear_usuario(Familia: schemas.FamiliaCrear, db: Session = Depends(get_db)):
    
    if Familia.Padre.nombre.strip() == '' or Familia.Padre.correo.strip() == '' or Familia.Hijo.nombre.strip() == '' or Familia.Hijo.edad.strip() == '':
        raise HTTPException(status_code = 404, detail = "ERROR A INGRESAR EL PADRE Y EL HIJO, INTENTAR OTRA VEZ")
    else:
        try:
            nuevo_usuario = models.Usuario(

                nombre = Familia.Padre.nombre,
                correo = Familia.Padre.correo,
                contraseña = Familia.Padre.contraseña
            )
            
            db.add(nuevo_usuario)
            db.flush()
            db.refresh(nuevo_usuario)

            nuevo_hijo = models.Hijo(

                nombre = Familia.Hijo.nombre,
                edad = Familia.Hijo.edad,
                autismo = Familia.Hijo.autismo,
                DatosExtra = Familia.Hijo.DatosExtra,
                padre_id = nuevo_usuario.id
            )
            
            db.add(nuevo_hijo)
            db.commit()
            db.refresh(nuevo_hijo)

            return {"padre": nuevo_usuario, "hijo": nuevo_hijo}
        except:
            db.rollback()
            raise HTTPException(status_code = 404, detail = "ERROR A INGRESAR EL PADRE Y EL HIJO, INTENTAR OTRA VEZ")

    
@app.post("/Iniciar_Sesion")
def Iniciar_Sesion(sesion: models.IniciarSesion, db: Session = Depends(get_db)):
   
    buscar_Padre = db.query(models.Usuario).filter(models.Usuario.correo == sesion.correo).first()

    if buscar_Padre:  
        if sesion.contraseña == buscar_Padre.contraseña:  
            paquete_Hijo = db.query(models.Hijo).filter(models.Hijo.padre_id == buscar_Padre.id).first()
            return  {"nombre": buscar_Padre.nombre, "correo": buscar_Padre.correo, "id": buscar_Padre.id, "id_Hijo": paquete_Hijo.id}
        else:  
            raise HTTPException(status_code = 404, detail = "el correo o la contraseña no coinciden, rechaza o explota :v")  
    else: 
        raise HTTPException(status_code = 404, detail = "el correo o la contraseña no coinciden, rechaza o explota :v")
    
    
""" Esta es la clase del articulo, aqui estamos haciendo la conexion entre la creacion de la tabla, la base de datos y la aplicacion, pasando los datos"""
@app.post("/Articulo")
def Creando_Articulo(Def_Articulo: schemas.ArticuloCrear, db: Session = Depends(get_db)):
    nuevo_Articulo = models.Articulos(

        titulo = Def_Articulo.titulo,
        autor = Def_Articulo.autor,
        fuente = Def_Articulo.fuente,
        fecha = Def_Articulo.fecha,
        parrafo = Def_Articulo.parrafo,
        
    )

    db.add(nuevo_Articulo)
    db.commit()
    db.refresh(nuevo_Articulo)

    return nuevo_Articulo

""" Esta función lo que hará es buscar y agarrar los datos que estan en esa tabla, para poder hacer los articulos"""
@app.get("/Articulo/")
def Buscando_Articulo(Buscar_Articulo: Session = Depends(get_db)):

    return Buscar_Articulo.query(models.Articulos).all()

@app.post("/Especialista/")
def Buscando_Especialista(nombre: str = Form(...),
    cedula: int = Form(...), 
    correo: str = Form(...),
    contraseña: str = Form(...), 
    Instituto: str = Form(...),
    especialidad: str = Form(...),
    
    Comprobante: UploadFile = File(...),db: Session = Depends(get_db)):

    if not os.path.exists("Comprobantes"):
        os.makedirs("Comprobantes")

    Destino = f"Comprobantes/{Comprobante.filename}"
    
    with open(Destino, "wb") as buffer:
        shutil.copyfileobj(Comprobante.file, buffer)

    Nuevo_Especialista = models.Especialistas(

        nombre = nombre,
        cedula = cedula,
        correo = correo,
        contraseña = contraseña,
        Instituto = Instituto,
        especialidad = especialidad,
        estado = "Pendiente",
        Comprobante = Destino
    )

    db.add(Nuevo_Especialista)
    db.commit()
    db.refresh(Nuevo_Especialista)

    return {"Creo que todo funcionó bien":"exito"}

@app.post("/Inicio_Sesion_Especialista")
def Iniciar_Sesion_Especialista(sesion_Especialista: models.IniciarSesion, db: Session = Depends(get_db)):

    Buscar_Especialista = db.query(models.Especialistas).filter(models.Especialistas.correo == sesion_Especialista.correo).first()

    if Buscar_Especialista:
        if sesion_Especialista.contraseña == Buscar_Especialista.contraseña:
            if Buscar_Especialista.estado == "Aprobado":
                return {"correo": Buscar_Especialista.correo, "id": Buscar_Especialista.id}
            else:
                raise HTTPException(status_code = 404, detail = "Aun no se ha aprobado su comprobante")
        else:
            raise HTTPException(status_code = 404, detail = "OLI!!el correo o la contraseña no coinciden, rechaza o explota :v") 
    else:
        raise HTTPException(status_code = 404, detail = "El correo o la contraseña no coinciden, vamos mal")
    

@app.post("/Consejos_IA")
def Consejos_IA(Consejo_Hijo: int, db: Session = Depends(get_db)):

    Buscar_Consejo_IA = db.query(models.Hijo).filter(models.Hijo.id == Consejo_Hijo).first()

    if Buscar_Consejo_IA: 
        chat_completion = IAGroq.chat.completions.create(

            messages =[
                {
                    "role": "user",
                "content": f""" Actúa como experto en autismo. Genera un consejo práctico sin generar caracteres especiales. No uses asterisco para negrita, ni otro estilo". Perfil del niño:
        Nombre:{Buscar_Consejo_IA.nombre} Edad:{Buscar_Consejo_IA.edad} grado_de_autismo:{Buscar_Consejo_IA.autismo} Datos_Extra: {Buscar_Consejo_IA.DatosExtra}
        Dame un consejo con título y que diga 'Titulo:' antes, y pasos a seguir"""
                
                }
            ],
            model = "llama-3.1-8b-instant",
        )
        Consejo = chat_completion.choices[0].message.content
        return Consejo
    else:
        raise HTTPException(status_code = 404, detail = "NO EXISTE EL NIÑOOO!")


