
from typing import Annotated
from fastapi import File, UploadFile, Request, APIRouter,Depends
import os
import uuid
from db.session import get_db
from sqlalchemy.orm import selectinload, Session,joinedload
from sqlalchemy import select
from schemas.base_response import GenericResponse
from schemas.post import PostCreate, PostShow
from db.repository.post import create_post,show_post_detail,get_post,update_post
from db.models.user import User
from db.models.post import Post
from db.models.likes import Likes
from db.models.collection import Collection
from apis.v1.route_login import get_current_user
from sqlalchemy import func


router = APIRouter(prefix="/api/swiper")

@router.get("/all", response_model=GenericResponse[list[PostShow]])
def get_list(db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    query = select(Post)
    if not current_user.is_valid_vip:
        query = query.where(Post.is_vip==0)
    query = query.limit(5).order_by(Post.is_recommand.desc())
    #stmt = select(Post).limit(5).order_by(Post.is_recommand.desc())
    data = db.scalars(query).all()
    print(f"swiper data:{data}")
    return {"code":1, "data":data}
    
    