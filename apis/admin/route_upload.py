
from fastapi import Depends, File, UploadFile, Request, APIRouter
import os
import uuid
from schemas.base_response import GenericResponse
from schemas.uploadfile import UploadResponse
from schemas.user import User
from db.models.user import User as Dbuser
from core.config import Setting
from apis.v1.route_login import get_admin_user


router = APIRouter(prefix="/api/admin/upload", dependencies=[Depends(get_admin_user)])

@router.post("",response_model=GenericResponse[UploadResponse])
def upload(request:Request,file:UploadFile = File(...)):
    file_name = str(uuid.uuid4())
    filepath, ext = os.path.splitext(file.filename)
    file_name = f"{file_name}{ext}"
    
    try:
        PATH = Setting.STATIC_DIR+'/'+Setting.UPLOAD_DIR
        if not os.path.exists(PATH):
          os.makedirs(PATH)
        with open(Setting.STATIC_DIR+'/'+Setting.UPLOAD_DIR+'/'+file_name, 'wb') as f:
            #f.write(file.file.read(1024*1024))
            while contents := file.file.read(1024 * 1024):
                    f.write(contents)
            return {
                "code":1, "data":{"file_name":file_name}
            }
            # return BaseResponse.success({
            #     "filename":file_name,
            #     "url":f"{req.base_url}static/{file_name}"
            # })
    except Exception as e:
        print(f"upload error:{e}")
       # pass
        return {"msg":"upload failed"}

@router.get("/user", response_model=GenericResponse[User])
def myres():
    dbuser = Dbuser(id=1,name="zhang san")
    return {"code":2, "data":dbuser}

@router.get("/list/user",response_model=GenericResponse[list[User]])
def user_list():
    users = []
    users.append(Dbuser(id=3,name="lisi"))
    users.append(Dbuser(id=4, name="wang wu"))
    
    
    return {"code":1, "data":users}

   
    