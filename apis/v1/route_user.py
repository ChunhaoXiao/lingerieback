
from fastapi import HTTPException, APIRouter,Depends
from db.models.user import User
from schemas.base_response import GenericResponse
from schemas.user import User as UserSchema, UserResponse
from apis.v1.route_login import get_current_user
from sqlalchemy.orm import Session
from db.session import get_db
from sqlalchemy import func, select, select, update

from core.config import Setting

router = APIRouter(prefix="/api/user")

@router.get("/me", response_model=GenericResponse[UserResponse])
def get_logined_user(current_user:User=Depends(get_current_user)):
    return {"code":1, "data":current_user}
    
@router.put("/update")
def set_username(user:UserSchema,db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    cnt = db.scalars(select(User).where(User.name==user.name,User.id != current_user.id)).first()
    print(f"cnt is:{cnt}")
    if cnt:
        return {"code":2, "data":"用户名已被占用"}
       #raise HTTPException(status_code=400, detail="用户名已被使用")
    db.execute(update(User).where(User.id==current_user.id).values(name=user.name))
    db.commit()
    user = db.scalars(select(User).where(User.id==current_user.id)).first()
    return {"code":1,"data":user}