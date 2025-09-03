from fastapi import FastAPI,APIRouter,status,Depends,HTTPException
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.schemas import ResArticle
from app.models import models,schemas
from app.core import oauth

app=FastAPI()
router=APIRouter(
    prefix="/article",
    tags=["articles"]
)
@router.get("/",status_code=status.HTTP_200_OK,response_model=schemas.ResArticle)
def get_articles(db:Session=Depends(get_db)):
    articles=db.query(models.Article).first()
    return articles
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.ResArticle)
def create(
    article: schemas.CreateArticle,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth.get_current_user)  
):
    new_article = models.Article(**article.dict())
    new_article.author = current_user.id
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article