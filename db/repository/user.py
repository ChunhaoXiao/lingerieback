

from sqlalchemy.orm import Session
from db.models.user import User
from sqlalchemy import Select
from core.config import Setting
def create_user(datas:dict, db:Session):
    openid = datas["openid"]
    user = db.scalars(Select(User).where(User.open_id == openid)).first()
    if not user:
        user = User(open_id=openid)
        db.add(user)
        db.commit()
        db.refresh(user)
    if user.open_id == Setting.ADMIN_OPENID:
        if user.is_admin == 0:
          user.is_admin = 1
          db.commit()
    return user