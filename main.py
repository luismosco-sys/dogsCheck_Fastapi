from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column ,Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List, Dict

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

class MascotUpdate(BaseModel):
    name:Optional[str] = None
    race:Optional[str] = None
    sku:Optional[str] = None
    picture:Optional[str] = None
    available:Optional[str] = None

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
    mascot = db.query(Mascot).filter(Mascot.id == mascot_id).first()
    if not mascot:
        raise HTTPException(status_code=404, detail="No se encuentra ese registro")
    return mascot
    
@app.post("/mascot", response_model=MascotResponse)
def create_mascot(mascot:MascotCreate, db:Session = Depends(get_db)):
    #Crear nuevo registro
    if db.query(Mascot).filter(Mascot.sku ==mascot.sku).first():
        raise HTTPException(status_code=404, detail="!Esta mascota ya ha sido registrada!")

    new_register = Mascot(**mascot.model_dump())
    db.add(new_register)
    db.commit()
    db.refresh(new_register)
    return new_register


#Actualizar Registro
# @app.put("/mascot/{mascot_id}", response_model=MascotUpdate)
# def update_mascot(mascot_id:int, mascot_update=MascotUpdate, db:Session = Depends(get_db))-> Dict:
#     db_mascot = db.query(Mascot).filter(Mascot.id == mascot_id).first()
#     if not db_mascot:
#         raise HTTPException(status_code=404, detail="Registro de mascota no encontrado")
    
#     update_data = mascot_update.dict() 

#     for key, value in update_data.items():
#         setattr(db_mascot, key, value)

#     db.commit()
#     db.refresh(update_data)
#     return db_mascot 

#Borrar Registro 
@app.delete("/mascot/{mascot_id}")
def delete_mascot(mascot_id:int, db:Session =Depends(get_db)):
    mascot = db.query(Mascot).filter(Mascot.id == mascot_id).first()
    if not mascot:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    db.delete(mascot)
    db.commit()
    return{"message":"Registro eliminado"}

#Obtener todos los registros 
@app.get("/mascot/", response_model=List[MascotResponse])
def get_all_mascots(db:Session = Depends(get_db)):
    return db.query(Mascot).all()

#Actualizar Registro
@app.put("/users/{mascot_id}", response_model=MascotResponse)
def update_user(mascot_id: int, user: MascotUpdate, db: Session = Depends(get_db)):
    """Update a user"""
    db_user = db.query(Mascot).filter(Mascot.id == mascot_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user
