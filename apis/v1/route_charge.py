from typing import Annotated
from fastapi import Depends, Depends, Depends, FastAPI,Request,APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select,null
from db.models.card import Card
from db.models.user import User
from db.session import get_db
import datetime
from dateutil.relativedelta import relativedelta

from db.models.vip import Vip
from db.repository.charge_lock import save_lock,is_locked

router = APIRouter()

@router.get("/charge", response_class=HTMLResponse)
async def show_form(request: Request):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        request=request, name="charge.html"
    )
    
@router.post("/charge")

async def charge(request: Request,name: Annotated[str, Form()], cardnumber: Annotated[str, Form()],db:Session=Depends(get_db)):
    if is_locked(request.client.host,db):
        return {
            "data":"错误次数太多，请稍后再试"
        }
    print(f"name is:{name},card is:{cardnumber}")
    if not name:
        return {"data":"用户名不能为空"}
    if not cardnumber:
        return {"data":"卡号不能为空"}              
    user = db.scalars(select(User).where(User.name == name)).first()
    if not user:
        return {"data":"用户不存在"}
    if user.is_permanent_vip:
        return {
            "data":"已经是永久vip用户，无需充值"
        }
    card = db.scalars(select(Card).where(Card.number==cardnumber,Card.user_id.is_(null()))).first()
    if not card:
        save_lock(request.client.host,db)
        return {
            "data":"卡号不正确"
        }
    card.user_id = user.id
    card.used_at=datetime.datetime.now()
    
    if not user.vip:
        if card.period < 999:
          expire_time = datetime.datetime.now() + relativedelta(months=card.period)
        else:
          expire_time = None
        vip = Vip(expire_date=expire_time,user=user,open_id=user.open_id)
        db.add(vip)
        db.commit()
        return {"data":"操作成功"}
    vip = user.vip
    if vip.expire_date > datetime.datetime.now():
       expire_time = vip.expire_date+relativedelta(months=card.period)
    else:
        expire_time = datetime.datetime.now() + relativedelta(months=card.period)
    vip.expire_date = expire_time
    db.commit()
    return {"data":"操作成功！"}
        
        
    
    
