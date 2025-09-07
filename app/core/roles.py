from fastapi import Depends,status,HTTPException
from app.models.models import User,Role
from app.core.oauth import get_current_user
def require_role(*allowed_roles:Role):
    def dependency(current_user:User=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have permission to access this resource")
        return current_user
    return dependency

    