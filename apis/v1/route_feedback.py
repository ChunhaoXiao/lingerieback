from fastapi import Depends, APIRouter, HTTPException,status

from schemas.feedback import FeedBack

from sqlalchemy.orm import Session
from apis.v1.route_login import get_current_user
from db.session import get_db
from db.models.user import User
from db.models.feedback import FeedBack as ModelFeedBack
import datetime
from sqlalchemy import select,func,cast,Date

router = APIRouter(prefix="/api/feedback") 

@router.post("/save")
def save(data:FeedBack,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    today = datetime.datetime.now().date()
    print(f"today is:{today}")
    cnt = db.scalars(select(func.count(ModelFeedBack.id)).select_from(ModelFeedBack).where(cast(ModelFeedBack.created_at,Date) == today),ModelFeedBack.user_id==current_user.id).first()
    if cnt > 0:
        return {"code":0,"data":"请勿重复提交"}
    files = ",".join(data.files)    
    feedback = ModelFeedBack(description=data.description, files=files,user_id=current_user.id)
    db.add(feedback)
    db.commit()
    return {"code":1, "data":"success"}
    #data.user_id=current_user.id