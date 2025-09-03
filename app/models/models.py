from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression  import text

class User(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
class Article(Base):
    __tablename__="articles"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    author=Column(Integer,ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"))
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    orm_mode=True
    author_user = relationship("User", backref="articles")

