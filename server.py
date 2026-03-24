from fastapi import FastAPI, Request, Query, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse, Response, HTMLResponse

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, String, Integer
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"

engine = create_engine(CONNECTION_STRING)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def retrieve_db():
    db = sessionlocal()
    try:
        yield db
    except:
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
    # name: str = Query(None, alias="country.name"),
    db: Session = Depends(retrieve_db)
):
    # CONSULTA
    countries = db.query(Country).all()
    return countries#PlainTextResponse(content=name, status_code=200)


@app.get("/cities")
async def cities(
    # name: str = Query(None, alias="country.name"),
    db: Session = Depends(retrieve_db)
):
    # CONSULTA
    cities = db.query(City).all()
    return cities#PlainTextResponse(content=name, status_code=200)

@app.get("/buscar")
async def buscar(nombre: str,
    db: Session = Depends(retrieve_db)):
    return db.query(Country).filter(Country.name == nombre).all()
