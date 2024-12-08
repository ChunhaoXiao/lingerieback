from fastapi import Depends, APIRouter, HTTPException,status

from schemas.feedback import FeedBack

from sqlalchemy.orm import Session
from apis.v1.route_login import get_current_user
from db.session import get_db
from db.models.user import User
from db.models.feedback import FeedBack as ModelFeedBack

router = APIRouter(prefix="/api/feedback")

@router.post("/save")
def save(data:FeedBack,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    files = ",".join(data.files)    
    feedback = ModelFeedBack(description=data.description, files=files,user_id=current_user.id)
    db.add(feedback)
    db.commit()
    return {"code":1, "data":"success"}
    #data.user_id=current_user.id