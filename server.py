from fastapi import FastAPI, Request, Query, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse, Response, HTMLResponse

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, String, Integer
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la conexión a la base de datos
CONNECTION_STRING = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"

engine = create_engine(CONNECTION_STRING)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def retrieve_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

class Country(Base):
    __tablename__ = "country"

    code = Column(String, primary_key=True, index=True)
    name = Column(String)
    continent = Column(String)
    region = Column(String)


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    countryCode = Column(String)
    district = Column(String)

app = FastAPI()

@app.get("/countries")
async def countries(
    db: Session = Depends(retrieve_db)
):
    # Consulta segura usando el ORM
    countries = db.query(Country).all()
    return countries


@app.get("/cities")
async def cities(
    db: Session = Depends(retrieve_db)
):
    # Este endpoint fallará en la Actividad 2 (Menor Privilegio) 
    # si se revoca el permiso SELECT sobre la tabla 'city'.
    cities = db.query(City).all()
    return cities

@app.get("/buscar")
async def buscar(nombre: str, db: Session = Depends(retrieve_db)):
    # VULNERABLE: Este endpoint es el objetivo de la Actividad 1 (SQL Injection)
    # Utiliza concatenación directa de strings en lugar de parámetros o el ORM.
    query = f"SELECT * FROM city WHERE Name = '{nombre}'"
    
    # Nota: Se usa text() de SQLAlchemy para permitir la ejecución de strings crudos,
    # pero la vulnerabilidad persiste por la concatenación de '{nombre}'.
    resultado = db.execute(text(query))
    return resultado.mappings().all()
