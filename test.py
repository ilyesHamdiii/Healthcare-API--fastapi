from dotenv import load_dotenv
import os 
from app.db.base import SQL_ALCHEMY_DATABASE_URL
load_dotenv()
x=os.getenv("DATABASE_URL")
print(SQL_ALCHEMY_DATABASE_URL)