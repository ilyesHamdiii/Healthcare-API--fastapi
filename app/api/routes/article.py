from fastapi import FastAPI,APIRouter,status,Depends,HTTPException,Query
from sqlalchemy import or_
from app.db.base import get_db
from sqlalchemy.orm import Session,joinedload
from app.models.schemas import ResArticle
from app.models import models,schemas
from app.core import oauth
from app.models.models import  Article
from app.models.models import Role
from app.core.roles import require_role

app=FastAPI()
router=APIRouter(
    prefix="/article",
    tags=["articles"]
)
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ResArticle],
    summary="List Articles",
    description="Retrieve a list of articles. You can search by title or content and limit the number of results."
)
def get_articles(
    db: Session = Depends(get_db),
    limit: int = Query(default=10, le=100),
    search: str = "",
    current_user: models.User = Depends(require_role(Role.ADMIN, Role.DOCTOR, Role.PATIENT)),
):
    articles = db.query(Article).options(joinedload(Article.author)).filter(or_(Article.content.startswith(search), Article.title.startswith(search))).all()
    paginated_articles = articles[0:limit]
    print("articles", articles)
    return paginated_articles

@router.get(
    "/My_Articles",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ResArticle],
    summary="Get My Articles",
    description="Retrieve all articles authored by the currently authenticated doctor or admin."
)
def get_my_articles(
    current_user: models.User = Depends(require_role(Role.ADMIN, Role.DOCTOR)),
    db: Session = Depends(get_db)
):
    articles = db.query(Article).options(joinedload(Article.author)).filter(Article.author_id == current_user.id).all()
    print("my articles", articles)
    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You do not have any articles until now.")
    return articles

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResArticle,
    summary="Get Article by ID",
    description="Retrieve a single article by its ID."
)
def get_single(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).options(joinedload(Article.author)).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find an article with the provided id ({id})")
    return article

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResArticle,
    summary="Create Article",
    description="Create a new article. Only admins and doctors can create articles."
)
def create(
    article: schemas.CreateArticle,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(Role.ADMIN, Role.DOCTOR))
):
    new_article = models.Article(**article.dict())
    new_article.author_id = current_user.id
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.patch(
    "/update/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResArticle,
    summary="Update Article",
    description="Update an existing article. Only the author can update their article."
)
def update_article(
    id: int,
    article: schemas.CreateArticle,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth.get_current_user)
):
    article_db = db.query(Article).options(joinedload(Article.author)).filter(Article.id == id).first()
    if not article_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find an article with the provided id ({id})")
    if article_db.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to update this post.")
    article_db.title = article.title
    article_db.content = article.content
    db.commit()
    db.refresh(article_db)
    return article_db

@router.delete(
    "/delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Article",
    description="Delete an article by its ID. Only the author can delete their article."
)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth.get_current_user)
):
    article = db.query(Article).options(joinedload(Article.author)).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find an article with the provided id ({id})")
    if article.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorised to delete this post")
    db.delete(article)
    db.commit()
    return {"message": f"Article with id ({id}) is deleted"}