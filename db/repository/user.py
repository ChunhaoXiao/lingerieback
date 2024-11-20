

from sqlalchemy.orm import Session
from db.models.user import User
from sqlalchemy import Select

def create_user(datas:dict, db:Session):
    openid = datas["openid"]
    user = db.scalars(Select(User).where(User.open_id == openid)).first()
    if not user:
        user = User(open_id=openid)
        db.add(user)
        db.commit()
    return user