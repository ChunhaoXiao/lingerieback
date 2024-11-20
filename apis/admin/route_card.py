import datetime
from fastapi import Depends, APIRouter, HTTPException,status,BackgroundTasks

from db.models.card import Card
from db.models.card_group import CardGroup
from db.models.user import User
from schemas.card import CardCreate
from sqlalchemy.orm import selectinload, outerjoin, Session;
from db.session import get_db
import uuid
from sqlalchemy import func, select
from apis.v1.route_login import get_admin_user

router = APIRouter(prefix="/api/admin/cards", dependencies=[Depends(get_admin_user)])

@router.get("")
def index(db:Session=Depends(get_db)):
    datas = db.scalars(select(CardGroup).order_by(CardGroup.id.desc())).all()
    return {"code":1, "data":datas}

@router.post("/save")
def save(data:CardCreate,db:Session=Depends(get_db)): 
    cnt = data.quantity
    cards = []
    for n in range(0,cnt):
        cards.append(Card(period=data.period,number=str(uuid.uuid4().hex)))
        
    grp_name=datetime.datetime.now().strftime("%Y%m%d%H%M")
    card_grp = CardGroup(name=grp_name, quantity=cnt,period=data.period,cards=cards)
    db.add(card_grp)
    db.commit()
    return {"data":"success"}

@router.get("/{id}")
def show(id:int, db:Session=Depends(get_db)):
    datas = db.scalars(select(Card).options(selectinload(Card.user)).where(Card.group_id == id).order_by(Card.used_at.desc())).all()
    return {"code":1,"data":datas}

@router.delete("/{id}")
def deleteCard(id:int, db:Session=Depends(get_db)):
    card_grp = db.get(CardGroup, id)
    if not card_grp:
        return {"code":0, "data":'数据不存在'}
    
    stmt = select(func.count(Card.id)).select_from(Card).where(Card.user_id > 0,Card.group_id==id)
    cnt = db.scalars(stmt).first()
    if cnt > 0:
        return {
            "code":0,
            "data":"已经有使用的卡密"
        }
    #card = db.get(Card, id)
    db.delete(card_grp)
    db.commit()
    return {"code":1,'data':'删除成功'}
    
