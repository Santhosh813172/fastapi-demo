from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg, psycopg2, psycopg_binary

db_url = "postgresql+psycopg2://postgres:postgre%401@localhost:5432/fastapidemo"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
       yield db
    finally:
       db.close()