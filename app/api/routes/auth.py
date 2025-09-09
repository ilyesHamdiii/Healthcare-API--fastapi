from fastapi import FastAPI,APIRouter,status,HTTPException
from fastapi.params import Depends
from app.models import schemas
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import models
from app.core import utility,oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.core.oauth import get_current_user
from jose import JWTError,jwt
from app.core.oauth import oauth2_scheme
app=FastAPI()
router=APIRouter(
    tags=["authorisation"]
)

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Token,
    summary="User Login",
    description="Authenticate a user using email and password. Returns a JWT access token if credentials are valid."
)
def login_alternative(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    """
    user = db.query(models.User).filter(models.User.email == login_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not utility.verify(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = oauth.create_access_token({"user_id": str(user.id)})
    print(token)
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=schemas.UserRead,
    summary="Get Current User",
    description="Retrieve details of the currently authenticated user using the provided JWT token."
)
def get_current_user(
    current_user: models.User = Depends(get_current_user)
):
    """
    Return the authenticated user's information.
    """
    return current_user