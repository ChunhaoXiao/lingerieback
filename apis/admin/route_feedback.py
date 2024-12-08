import datetime
from fastapi import Depends, APIRouter, HTTPException,status,BackgroundTasks
from db.models.user import User
from sqlalchemy.orm import selectinload, outerjoin, Session;
from db.session import get_db
from sqlalchemy import func, select
from apis.v1.route_login import get_admin_user
from db.models.feedback import FeedBack
from schemas.base_response import GenericResponse
from schemas.feedback import FeebBackResponse

router = APIRouter(prefix="/api/admin/feedback")

@router.get("", response_model=GenericResponse[list[FeebBackResponse]])
def index(page:int|None=1,db:Session=Depends(get_db)):
    offset = (page -1) *20
    stmt = select(FeedBack.id, FeedBack.description,FeedBack.files,FeedBack.created_at,User).join(User,FeedBack.user_id==User.id).offset(offset).limit(20).order_by(FeedBack.id.desc())
    res = db.execute(stmt).all()
    return {"code":1,"data":res}
