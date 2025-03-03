
from fastapi import Depends, File, UploadFile, Request, APIRouter
import os
import uuid
from schemas.base_response import GenericResponse
from schemas.uploadfile import UploadResponse
from schemas.user import User
from db.models.user import User as Dbuser
from core.config import Setting
from apis.v1.route_login import get_admin_user

def upload_file(file):
    file_name = str(uuid.uuid4())
    filepath, ext = os.path.splitext(file.filename)
    file_name = f"{file_name}{ext}"
    
    try:
        PATH = Setting.STATIC_DIR+'/'+Setting.UPLOAD_DIR
        if not os.path.exists(PATH):
          os.makedirs(PATH)
        with open(Setting.STATIC_DIR+'/'+Setting.UPLOAD_DIR+'/'+file_name, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                    f.write(contents)
            return {
                "code":1, "data":{"file_name":file_name}
            }
            
    except Exception as e:
        return {"code":0, "msg":"upload failed"}