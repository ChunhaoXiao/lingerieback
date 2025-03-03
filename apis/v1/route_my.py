

from fastapi import File, UploadFile, Request, APIRouter,Depends
from sqlalchemy.orm import joinedload, joinedload, selectinload, Session
from db.models.post_views import PostView
from db.session import get_db
from sqlalchemy import select
from apis.v1.route_login import get_current_user
from db.models.user import User
from db.models.likes import Likes
from db.models.post import Post
from schemas.base_response import GenericResponse
from schemas.likes import LikeResponse
from db.models.collection import Collection
from sqlalchemy.orm import aliased
 
router = APIRouter(prefix="/api/my")

@router.get("/likes", response_model=GenericResponse[list[LikeResponse]])
def mylikes(user:User=Depends(get_current_user),page:int=1, db:Session = Depends(get_db)):
    pageSize = 20
    offset = (page -1) * pageSize 
    stmt = select(Likes).options(selectinload(Likes.post)).join(Post,Post.id==Likes.post_id).where(Likes.user_id==user.id,Post.is_hide==0).offset(offset).limit(pageSize).order_by(Likes.id.desc())
    res = db.scalars(stmt).all()
    return {"code":1,"data":res}

@router.get("/collection", response_model=GenericResponse[list[LikeResponse]])
def my_collection(page:int | None =1,user:User=Depends(get_current_user),db:Session = Depends(get_db)):
    pageSize = 20
    stmt = select(Collection).options(selectinload(Collection.post)).join(Post, Post.id==Collection.post_id).where(Collection.user_id == user.id,Post.is_hide==0).limit(pageSize).offset((page-1) * pageSize).order_by(Collection.id.desc())
    res = db.scalars(stmt).all()
    return {"code":1, "data":res}

@router.get("/history", response_model=GenericResponse[list[LikeResponse]])
def my_histoty(page:int | None =1, user:User=Depends(get_current_user),db:Session = Depends(get_db)):
    offset = (page-1) * 20
    
    query = select(PostView).options(selectinload(PostView.post)).where(PostView.user_id==user.id)
    if not user.is_valid_vip and user.is_admin==0:
        query = query.where(PostView.post.has(Post.is_vip==0))
    query = query.where(PostView.post.has(Post.is_hide == 0)).offset(offset).limit(20).order_by(PostView.updated_at.desc())
    #stmt = select(PostView).options(selectinload(PostView.post)).where(PostView.user_id==user.id,PostView.post.has(Post.is_vip==0),PostView.post.has(Post.is_hide==0)).offset(offset).limit(20).order_by(PostView.updated_at.desc())
    res = db.scalars(query).all()
    for item in res:
        print(item.id)
        print("==============================")
        print(item.post)
    
    return {"code":1,"data":res}
    
    

# @router.get("/mylk")

# def mythumb(db:Session = Depends(get_db)):
#     stmt = select(Post).join(Post.likes).where(Likes.user_id ==200, Post.is_vip==0)
#     res1 = db.scalars(stmt).all()
#     print(res1)
#     return res1

