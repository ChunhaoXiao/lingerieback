
from sqlalchemy.orm import Session
from sqlalchemy import select,and_, or_
from db.models.notice import Notice
from db.models.notice_position import NoticePosition
import datetime

def get_active_notice(position:str,db:Session):
    # query = select(Notice).where(Notice.enabled==1).where(Notice.positions.any(NoticePosition.postion_name==position))
    
    # query = query.where()
    times = datetime.datetime.now().strftime('%H:%M')
    print(f"times========>{times}")
    stmt = select(Notice).where(and_(or_(and_(Notice.start_time == "",Notice.end_time ==""),and_(Notice.start_time <= times,Notice.end_time >= times)),Notice.enabled==1,Notice.positions.any(NoticePosition.postion_name==position),)).limit(1).order_by(Notice.id.desc())
    
    print(f"stmt ================={stmt}")
    
    # stmt = select(Notice).where(Notice.enabled==1).where(Notice.positions.any(NoticePosition.postion_name==position)).limit(1).order_by(Notice.id.desc())
    return db.scalars(stmt).first()

def show_notice(id:int, db:Session):
    return db.scalars(select(Notice).where(Notice.id==id)).first()