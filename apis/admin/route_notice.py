from fastapi import HTTPException, Depends, APIRouter
from db.session import get_db
from schemas.category import Category,CategoryCreate,CategoryResponse
from sqlalchemy.orm import selectinload, Session;
from db.models.notice import Notice
from db.models.user import User
from apis.v1.route_login import get_admin_user
from schemas.base_response import GenericResponse
from sqlalchemy import delete, delete, select
from db.models.notice_position import NoticePosition

from schemas.notice import NoticeCreate, NoticeResponse

router = APIRouter(prefix="/api/admin/notice", dependencies=[Depends(get_admin_user)])

@router.post("/save")
def save(data:NoticeCreate,db:Session=Depends(get_db)):
    pictures = ""
    if data.pictures:
        pictures = ",".join(data.pictures)
    if data.position:
        positions = []
        for pos in data.position:
            positions.append(NoticePosition(postion_name=pos))      
    notice = Notice(title=data.title,content=data.content, pictures=pictures,enabled=data.enabled,positions=positions)
    db.add(notice)
    db.commit()
    return {"code":1, "data":"success"}

@router.get("/index", response_model=GenericResponse[list[NoticeResponse]])
def index(db:Session=Depends(get_db)):
    datas = db.scalars(select(Notice).order_by(Notice.id.desc())).all()
    print(f"notice list:{datas}")
    return {"code":1, "data":datas}

@router.get("/{id}", response_model=GenericResponse[NoticeResponse])
def find_notice(id:int, db:Session=Depends(get_db)):
    notice = db.scalars(select(Notice).options(selectinload(Notice.positions)).where(Notice.id==id)).first()
    print(f"notice====>{notice}")
    if not notice:
        raise HTTPException(status_code=404)
    return {"code":1,"data":notice}

@router.put("/{id}")
def update(id:int,data:NoticeCreate,db:Session=Depends(get_db)):
    notice = db.scalars(select(Notice).where(Notice.id==id)).first()
    if not notice:
        raise HTTPException(status_code=404)
    if len(notice.positions) > 0:
        db.execute(delete(NoticePosition).where(NoticePosition.notice_id==id))
        db.commit()
    if data.position:
        positions = []
        for pos in data.position:
            positions.append(NoticePosition(postion_name=pos))      
    notice.title = data.title
    notice.content = data.content
    notice.pictures = ",".join(data.pictures)
    notice.enabled = data.enabled
    notice.positions=positions
    db.commit()
    return {"code":1,"data":"success"}

@router.put("/{id}/status")
def toggleStatus(id:int,db:Session=Depends(get_db)):
    notice = db.scalars(select(Notice).where(Notice.id==id)).first()
    if not notice:
        raise HTTPException(status_code=404)
    status = 1 if notice.enabled == 0 else 0
    notice.enabled = status
    db.commit()
    db.refresh(notice)
    return {"code":1,"data": notice}


@router.delete("/{id}")
def remove(id:int, db:Session=Depends(get_db)):
    notice = db.get(Notice, id)
    db.delete(notice)
    db.commit()
    return {"code":1, "data":"success"}
    