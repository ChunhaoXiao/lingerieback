from fastapi import HTTPException, Depends, APIRouter
from db.models.app_setting import AppSetting
from db.session import get_db
from schemas.category import Category,CategoryCreate,CategoryResponse
from sqlalchemy.orm import selectinload, Session;
from db.models.notice import Notice
from db.models.user import User
from apis.v1.route_login import get_admin_user
from schemas.base_response import GenericResponse
from sqlalchemy import delete, delete, select
from db.repository.app_setting import update_setting

router = APIRouter(prefix="/api/admin/setting", dependencies=[Depends(get_admin_user)])

@router.get("")
def index(db:Session=Depends(get_db)):
    datas = db.scalars(select(AppSetting)).all()
    return {"code":1, "data":datas}

@router.put("/save")
def update(datas:dict,db:Session=Depends(get_db)):
    
    print(f"datas:::{datas}")
    update_setting(datas, db)
    return {"code":1,"data":"success"}