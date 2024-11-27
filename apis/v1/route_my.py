

from fastapi import File, UploadFile, Request, APIRouter,Depends
from sqlalchemy.orm import selectinload, Session
from db.session import get_db
from sqlalchemy import select
from apis.v1.route_login import get_current_user
from db.models.user import User
from db.models.likes import Likes
from db.models.post import Post
from schemas.base_response import GenericResponse
from schemas.likes import LikeResponse
from db.models.collection import Collection
 
router = APIRouter(prefix="/api/my")

@router.get("/likes", response_model=GenericResponse[list[LikeResponse]])
def mylikes(user:User=Depends(get_current_user),page:int=1, db:Session = Depends(get_db)):
    pageSize = 20
    offset = (page -1) * pageSize 
    stmt = select(Likes).options(selectinload(Likes.post)).join(Post,Post.id==Likes.post_id).where(Likes.user_id==user.id).offset(offset).limit(pageSize).order_by(Likes.id.desc())
    res = db.scalars(stmt).all()
    return {"code":1,"data":res}

@router.get("/collection", response_model=GenericResponse[list[LikeResponse]])
def my_collection(page:int | None =1,user:User=Depends(get_current_user),db:Session = Depends(get_db)):
    pageSize = 20
    stmt = select(Collection).options(selectinload(Collection.post)).join(Post, Post.id==Collection.post_id).where(Collection.user_id == user.id).limit(pageSize).offset((page-1) * pageSize).order_by(Collection.id.desc())
    res = db.scalars(stmt).all()
    return {"code":1, "data":res}
