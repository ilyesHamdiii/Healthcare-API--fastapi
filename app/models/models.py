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
    articles = relationship("Article", back_populates="author")
class Article(Base):
    __tablename__="articles"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    author_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"))
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    author = relationship("User", back_populates="articles")
    class config:
        orm_mode=True

