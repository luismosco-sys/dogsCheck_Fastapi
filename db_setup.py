from sqlalchemy import create_engine, Column ,Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

#Coneccion a db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()