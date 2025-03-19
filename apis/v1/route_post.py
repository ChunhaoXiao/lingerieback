
from typing import Annotated
from fastapi import BackgroundTasks, HTTPException, Query, params, File, UploadFile, Request, APIRouter,Depends
import os
import uuid
from db.models.post_views import PostView
from db.repository.post_view import save_view_log
from db.session import get_db
from sqlalchemy.orm import selectinload, Session,joinedload
from sqlalchemy import literal_column, literal_column, literal_column, literal, literal, literal, null, null, null, case, desc, desc, desc, select
from schemas.base_response import GenericResponse
from schemas.post import PostCreate, PostShow, Statistic
from db.repository.post import create_post,show_post_detail,get_post,update_post
from db.models.user import User
from db.models.post import Post
from db.models.likes import Likes
from db.models.collection import Collection
from apis.v1.route_login import get_current_user
from sqlalchemy import func
from core.config import Setting

from schemas.post_request import PostRequest

router = APIRouter(prefix="/api/posts")
from db.redis import get_config

@router.get("/hot",  response_model=GenericResponse[list[PostShow]])
def index_hot(db:Session = Depends(get_db), current_user:User=Depends(get_current_user)):
    lmt = get_config('index_recommand_num')
    print(f"lmt....{lmt}")
    query = select(Post,func.count(Post.likes).label("like_cnt")).join(Post.likes,isouter=True).options(selectinload(Post.files))
    if not current_user.is_valid_vip:
        query = query.where(Post.is_vip==0)
    query = query.where(Post.is_hide == 0)
    #query = query.group_by(Post.id).order_by(Post.is_hot.desc(),desc("like_cnt")).limit(get_config('index_recommand_num'))
    orderby = get_config("index_recommand_order")
    if orderby == "like_cnt":
        query = query.group_by(Post.id).order_by(Post.is_hot.desc(),desc("like_cnt")).limit(get_config('index_recommand_num'))
    else:
      query = query.group_by(Post.id).order_by(func.random()).limit(get_config('index_recommand_num'))
    res = db.scalars(query).all()
    print(f"res======>{res}")
    return {"code":1, "data":res}

@router.get("/posts", response_model=GenericResponse[list[PostShow]])
def index(params:Annotated[PostRequest, Query()], db:Session = Depends(get_db), current_user:User=Depends(get_current_user)):
    is_vip = 0
    print(f"current use is##################{current_user}")
    if current_user.is_valid_vip or current_user.is_admin==1:
        is_vip = 1

    posts = get_post(db=db, params=params,is_vip=is_vip,include_hide=0)
    return {"code":1, "data":posts}


@router.get("/show/{id}",response_model=GenericResponse[PostShow])
def post_detail(id:int,  background_tasks: BackgroundTasks, db:Session = Depends(get_db), current_user:User=Depends(get_current_user)):
    stmt = select(Post).options(selectinload(Post.likes.and_(Likes.user_id==current_user.id))).options(selectinload(Post.category)).options(selectinload(Post.files)).options(selectinload(Post.statistic)).options(selectinload(Post.collections.and_(Collection.user_id==current_user.id))).where(Post.id == id)
    post = db.scalars(stmt).first()
    if post.is_hide == 1 and current_user.is_admin == 0:
        raise HTTPException(status_code=404)
        
    if post.is_vip:
        if not current_user.vip and current_user.is_admin == 0:
            raise HTTPException(status_code=404)
        
    
            #raise 
    # like_cnt = db.scalars(select(func.count(Likes.id)).where(Likes.post_id == id)).first()
    # collection_cnt = db.scalars(select(func.count(Collection.id)).where(Collection.post_id==id)).first()
    # datas = post.__dict__
    # datas.update({
    #     "like_cnt":like_cnt,
    #     "collection_cnt":collection_cnt
    # })

    #print(f"post dict:{datas}")  
    background_tasks.add_task(save_view_log,post,current_user,db)
    #save_view_log(post,current_user,db)
    
    # view = db.scalars(select(PostView).where(PostView.post_id == post.id,PostView.user_id==current_user.id)).first()
    # print(f"view is:=====>{view}")
    # if view:
    #     print("has view==============================================")
    #     #view.updated_at = datetime.datetime.now()
    #     #view.updated_at=func.now()
    #    # db.commit()
    # else:
    #     print(f"post before save statistic:{post}")
    #     print("NOT has VIEW=====================================")
    #     view = PostView(post_id=post.id, user_id=current_user.id)
    #     db.add(view)
    #     db.commit()
    #     print("will update view cnt~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     print("post is========================>")
    #     print(f"post after save statistic:{post}")

    #datas = post.__dict__
    #PostShow.model_validate(post)
    
    
    return {"code":1,"data":post}
    
    

@router.get("/tests")
def tests(db:Session = Depends(get_db)):
    res = db.execute(select(Post).where(Post.id > 0)).first()
    return {"code":1, "data":res}


    

