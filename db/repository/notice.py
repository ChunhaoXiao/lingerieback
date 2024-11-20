
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models.notice import Notice
from db.models.notice_position import NoticePosition

def get_active_notice(position:str,db:Session):
    stmt = select(Notice).where(Notice.enabled==1).where(Notice.positions.any(NoticePosition.postion_name==position)).limit(1).order_by(Notice.id.desc())
    return db.scalars(stmt).first()

def show_notice(id:int, db:Session):
    return db.scalars(select(Notice).where(Notice.id==id)).first()