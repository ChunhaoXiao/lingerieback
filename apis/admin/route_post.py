from typing import Annotated
from fastapi import Depends, APIRouter, Query
from sqlalchemy import select
from db.models.likes import Likes
from db.models.user import User
from db.session import get_db
from sqlalchemy.orm import Session,selectinload
# from db.models.category import Category as DbCategory
from db.models.post import Post
from apis.v1.route_login import get_admin_user, get_current_user
from schemas.base_response import GenericResponse
from db.repository.post import removePost,update_post,get_post,create_post
#from db.repository.category import get_category_list,get_valid_categories
from schemas.post import PostCreate, PostShow
from schemas.post_request import PostRequest


router = APIRouter(prefix="/api/admin/post", dependencies=[Depends(get_admin_user)])


@router.get("", response_model=GenericResponse[list[PostShow]])
def index(params:Annotated[PostRequest, Query()], db:Session = Depends(get_db)):
    print(f"paramssss{params}")
    posts = get_post(db=db, params=params,is_vip=1,include_hide=1,all_category=1)
    print(f"admin post:::{posts}")
    return {"code":1, "data":posts}

@router.post("/posts")
def save(post:PostCreate, db:Session = Depends(get_db)):
    create_post(post,db)
    return {"code":1, "data":"success"}


@router.get("/show/{id}", response_model=GenericResponse[PostShow])
def post_detail(id:int, db:Session = Depends(get_db)):
    stmt = select(Post).options(selectinload(Post.files)).options(selectinload(Post.category)).where(Post.id == id)
    post = db.scalars(stmt).first()    
    datas = post.__dict__   
    return {"code":1,"data":datas}

@router.delete("/{id}")
def deletePost(id:int,db:Session=Depends(get_db)):
    print(f"postid is:#####################{id}")
    removePost(id, db)
    return {"code":1, "data":"success"}

@router.put("/update/{id}")
def update(id:int, post:PostCreate, db:Session = Depends(get_db)):
    print(post)
    update_post(id,post,db)
    return {"code":1, "data":"success"}