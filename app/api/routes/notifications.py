from fastapi import FastAPI,APIRouter,status,Depends,HTTPException
from app.models.schemas import NotificationSchema
from sqlalchemy.orm import Session
from app.core.roles import require_role
from app.db.base import get_db
from app.models import models


app=FastAPI()
router=APIRouter(
    tags=["notifications"]
)
@router.get(
    "/notifications",
    response_model=list[NotificationSchema],
    status_code=status.HTTP_200_OK,
    summary="Get User Notifications",
    description="Retrieve all notifications for the currently authenticated doctor or admin."
)
def getNotificaions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(models.Role.DOCTOR, models.Role.ADMIN,models.Role))
):
    notification = db.query(models.Notification).filter(models.Notification.user_id == current_user.id).all()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You do not have any notifications right now.")
    return notification