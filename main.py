from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from api_schemas import MascotCreate, MascotResponse, MascotUpdate
from db_setup import Mascot,get_db
from typing import List
from sqlalchemy.orm import Session


app = FastAPI(title="Rescue Doggy Register")

# ENDPOINTS
@app.get("/")
def root():
    return("Terminal messsage: System Working")

#GET Registro especifico
@app.get("/mascot/{mascot_id}", response_model=MascotResponse)
def get_mascot(mascot_id:int, db:Session=Depends(get_db)):
    mascot = db.query(Mascot).filter(Mascot.id == mascot_id).first()
    if not mascot:
        raise HTTPException(status_code=404, detail="No se encuentra ese registro")
    return mascot

#POST Crear registro
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

#DELETE Borrar Registro 
@app.delete("/mascot/{mascot_id}")
def delete_mascot(mascot_id:int, db:Session =Depends(get_db)):
    mascot = db.query(Mascot).filter(Mascot.id == mascot_id).first()
    if not mascot:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    db.delete(mascot)
    db.commit()
    return{"message":"Registro eliminado"}

#GET Obtener todos los registros 
@app.get("/mascot/", response_model=List[MascotResponse])
def get_all_mascots(db:Session = Depends(get_db)):
    return db.query(Mascot).all()

#PUT Actualizar Registro
@app.put("/mascot/{mascot_id}", response_model=MascotResponse)
def update_mascot(mascot_id: int, mascot: MascotUpdate, db: Session = Depends(get_db)):
    db_mascot = db.query(Mascot).filter(Mascot.id == mascot_id).first()
    if not db_mascot:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    for field, value in mascot.dict().items():
        setattr(db_mascot, field, value)
    
    db.commit()
    db.refresh(db_mascot)
    return db_mascot
