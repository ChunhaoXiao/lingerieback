from fastapi import FastAPI, Depends, APIRouter, HTTPException,status,UploadFile, Request,File
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from db.models.app_setting import AppSetting
from schemas.feedback import FeedBack

from sqlalchemy.orm import Session
from apis.v1.route_login import get_current_user
from db.session import get_db
from db.models.user import User
from db.models.feedback import FeedBack as ModelFeedBack
import datetime
from sqlalchemy import delete, delete, select,func,cast,Date
from db.repository.app_setting import get_app_setting
from db.repository.temp_uploaded_file import get_upload_cnt
from schemas.uploadfile import UploadResponse
from schemas.base_response import GenericResponse
from utils.files import upload_file
from db.models.temp_uploaded_files import TempUploadedFile
import os
from core.config import Setting
from core.exceptions_handler import validation_exception_handler
from db.repository.app_setting import get_app_setting
router = APIRouter(prefix="/api/feedback")


@router.get("/status")
def feeb_back_status(db:Session=Depends(get_db)):
    row = db.scalars(select(AppSetting).where(AppSetting.setting_name=="feed_back_status")).first()
    return {"code":1,"data":row}
    

@router.post("/save")
def save(data:FeedBack,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    status = get_app_setting("feed_back_status")
    print(f"status is::::{status}") 
    print(f"------{get_app_setting('app_status')}")
    if status == '0':
        return {"code":0, "data":"已关闭该功能"}
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
    
@router.post("/upload",response_model=GenericResponse[UploadResponse])
def upload(request:Request,file:UploadFile = File(...),user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    cnt = get_upload_cnt(user.id, db)
    if cnt >= int(get_app_setting('feedback_max_files')):
        return {
            "code":0,
            "data":{"file_name":"", "full_path":""}
        }
    print(f"upload cnt::{cnt}")
    print(f"current user is{user.name}")
    res = upload_file(file)
    print(f"res is::::{res}")
    if res['code'] == 1:
        temp_uploaded_file = TempUploadedFile(file_name=res['data']['file_name'],user_id=user.id)
        db.add(temp_uploaded_file)
        db.commit()
    return res

@router.delete("/delete-img")
def deleteImg(data:dict, db:Session=Depends(get_db)):
    base_file = os.path.basename(data["filename"])
    print(f"file name is:{base_file}")
    file_name = f"{Setting.STATIC_DIR}/{Setting.UPLOAD_DIR}/{base_file}"
    if os.path.exists(file_name):
        os.remove(file_name)
        print("file eixsts")
        db.execute(delete(TempUploadedFile).where(TempUploadedFile.file_name==base_file))
        db.commit()
        
        
    
    return {"code":1, "data":"success"}

@router.get("/uploaded-files",response_model=GenericResponse[list[UploadResponse]])
def get_files(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    today = datetime.datetime.now().date()
    res = db.scalars(select(TempUploadedFile).where(TempUploadedFile.user_id==user.id, cast(TempUploadedFile.created_at,Date)==today)).all()
    return {"code":1, "data":res}
    
    
        
  