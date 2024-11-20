
from fastapi import File, UploadFile, Request, APIRouter,Depends
from sqlalchemy.orm import Session
from db.session import get_db
from sqlalchemy import select

from db.repository.notice import get_active_notice,show_notice
from schemas.base_response import GenericResponse
from schemas.notice import NoticeResponse

router = APIRouter(prefix="/api/notice")

@router.get("")
def get_notice(position:str,db:Session = Depends(get_db)):
    datas = get_active_notice(position=position,db=db)
    return {"code":1, "data":datas}

@router.get("/{id}", response_model=GenericResponse[NoticeResponse])
def show(id:int, db:Session = Depends(get_db)):
    data = show_notice(id=id, db=db)
    return {"code":1, "data":data}
    