from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import loadenv
import os 
loadenv()
SQL_ALCHEMY_DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(SQL_ALCHEMY_DATABASE_URL)
Sessionlocal=sessionmaker(auto_commit=False,auto_flush=False,bind=engine)
Base=declarative_base()
def get_db():
    
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()