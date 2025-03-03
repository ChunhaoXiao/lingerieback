
from sqlalchemy.orm import Session
from sqlalchemy import func, func, select,cast,Date
import datetime

from db.models.temp_uploaded_files import TempUploadedFile

def save_file(db:Session):
    pass
    
    
def get_upload_cnt(user_id:int,db:Session):
    today = datetime.datetime.now().date()
    
    cnt = db.scalars(select(func.count(TempUploadedFile.id)).select_from(TempUploadedFile).where(TempUploadedFile.user_id==user_id, cast(TempUploadedFile.created_at, Date)==today)).first()
    return cnt
    