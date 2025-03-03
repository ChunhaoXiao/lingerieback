from typing import Annotated
from fastapi import HTTPException, Depends, APIRouter, Query
from db.models.post_views import PostView
from db.session import get_db
from schemas.category import Category,CategoryCreate,CategoryResponse
from sqlalchemy.orm import selectinload, Session;
from db.models.notice import Notice
from db.models.user import User
from db.models.vip import Vip
from apis.v1.route_login import get_admin_user
from schemas.base_response import GenericResponse
from sqlalchemy import func, func, select

from db.models.likes import Likes

from schemas.user import UserParam, UserRequest, UserResponse,UserListResponse,UserDetailResponse
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/admin/user", dependencies=[Depends(get_admin_user)])

@router.get("",response_model=GenericResponse[UserListResponse])
def get_users(param:Annotated[UserParam, Query()], db:Session=Depends(get_db)):
    query = select(User).options(selectinload(User.vip.and_(Vip.expire_date > func.now())))
    if param.name:
        print(f"name is:::::{param.name}")
        query = query.where(User.name.like(f"%{param.name}%"))
    if param.vip == 1:
        query = query.where(User.vip.has(Vip.expire_date > datetime.now()))
    #query = query.where(User.is_admin==0)
    query = query.offset((param.page - 1) * 15).limit(15)
    users = db.scalars(query.order_by(User.id.desc())).all()
    total_cnt = db.scalars(select(func.count(User.id)).select_from(User)).first()
    vip_cnt = db.scalars(select(func.count(Vip.id)).select_from(Vip).where(Vip.expire_date > func.now())).first()
    return {"code":1, "data":{"users":users, "total_cnt":total_cnt,"vip_cnt":vip_cnt}}


@router.get("/{id}", response_model=GenericResponse[UserDetailResponse])
def find_user(id:int,db:Session=Depends(get_db)):
    user = db.scalars(select(User).options(selectinload(User.vip.and_(Vip.expire_date > func.now()))).where(User.id==id)).first()
    last_visit_time = None
    data = db.scalars(select(PostView).where(PostView.user_id==id).order_by(PostView.updated_at.desc())).first()
    if data:
        last_visit_time = data.updated_at
    total_view = db.scalars(select(func.count(PostView.id)).select_from(PostView).where(PostView.user_id == id)).first()
    like_cnt = db.scalars(select(func.count(Likes.id)).where(Likes.user_id==id)).first()
    
    return {
        "code":1, 
        "data":{
            "user":user,
            "last_visit_time":last_visit_time,
            "total_view":total_view,
            "like_cnt":like_cnt
        }
    }

@router.put("/{id}")
def update_user(id:int,data:UserRequest, db:Session=Depends(get_db)):
    user = db.scalars(select(User).where(User.id==id)).first()
    if not user:
        return {"code":0,"data":"user not found"}
    name = data.name
    vip_period = data.vip_period
    if name:
        existsUser = db.scalars(select(User).where(User.id != id,User.name == name)).first()
        if existsUser:
            return {"code":0, "data":"用户名已被占用"}
        
        user.name = name
        db.commit()
    print(f"vip peroiod:{vip_period}")
    if vip_period > 0:
        print(f"user.vip is#######{user.vip}")
        #print(f"user.vip.expire_date:#######{user.vip.expire_date}")
        if not user.vip:
            print("not vip..............")
            expire_date = datetime.now() + timedelta(days=31 * vip_period)
            print('not has old vip')
            vip = Vip(user=user,open_id=user.open_id,expire_date=expire_date)
            db.add(vip)
            db.commit()
            return {"code":1,"data":"success"}
        else:
            expire_date = ""
            vip = user.vip
            if vip.expire_date > datetime.now():
                expire_date = vip.expire_date + timedelta(days=31 * vip_period)
            else:
                expire_date = datetime.now() + timedelta(days=31 * vip_period)
            print("is vip..............")
            vip.expire_date = expire_date
            db.commit()
            return {"code":1,"data":"success"}
            
              
    if vip_period == 0:
        #取消vip
        if user.vip:
            if user.vip.expire_date > datetime.now():
                 vip = user.vip
                 vip.expire_date = datetime.now()
                 db.commit()
        return {"code":1,"data":"success"}
            
            
        
    
    
    
 