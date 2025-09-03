from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column ,Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Rescue Doggy Register")

#Database Setup
engine = create_engine("sqlite:///dogs.db", connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Database Model
class Mascot(Base):
    __tablename__ = "Mascotas"

    id= Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    race=Column(String,nullable=True)
    picture=Column(String, nullable=True)
    sku=Column(String,nullable=False,unique=True)
    available=Column(String,nullable=False)

Base.metadata.create_all(engine)

# Pydantic models
class MascotCreate(BaseModel):
    name:str
    race:str
    sku:str
    picture:str
    available:str

class MascotResponse(BaseModel):
    id:int
    name:str
    sku:str
    picture:str
    race:str
    available:str

    class Config:
        from_attributes = True

#Coneccion a db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()

# ENDPOINTS
@app.get("/")
def root():
    return("Terminal messsage: System Working")

@app.get("/mascot/{mascot_id}", response_model=MascotResponse)
def get_mascot(mascot_id:int, db:Session=Depends(get_db)):
    mascot = db.query(Mascot).filter(Mascot.id == mascot.id).first()
    if not mascot:
        raise HTTPException(status_code=404, detail="No se encuentra ese registro")
    
@app.post("/mascot", response_model=MascotResponse)
def create_mascot(mascot:MascotCreate, db:Session = Depends(get_db)):
    #Crear nuevo registro
    if db.query(Mascot).filter(Mascot.sku ==mascot.sku).first():
        raise HTTPException(status_code=404, detail="!Esta mascota ya ha sido registrada!")

    new_register = Mascot(mascot.model_dump())
    db.add(new_register)
    db.commit()
    db.refresh(new_register)
    return new_register
