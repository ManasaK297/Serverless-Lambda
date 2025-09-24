from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./functions.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Function(Base):
    __tablename__ = "functions"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String)
    language = Column(String)
    timeout = Column(Integer)

def create_db():
    Base.metadata.create_all(bind=engine)
