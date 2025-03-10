from fastapi import Depends, APIRouter, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import create_access_token
from core.config import Setting
import requests
from db.repository.user import create_user
import jwt
from sqlalchemy import Select
from db.models.user import User
from core.config import Setting

router = APIRouter(prefix="/api")

@router.post("/login")
def login(data:dict, db:Session=Depends(get_db)):
    code = data["code"]
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {"appid":Setting.APP_ID,"secret":Setting.APP_SECRET,"js_code":code, "grant_type":"authorization_code"}
    res = requests.get(url=url, params=params)
    print(f"login wechat res:{res}")
    datas = res.json()
    print(f"=============================================================================================>{datas}")
    
    if datas['openid']:
      create_user({"openid":datas['openid']}, db)
      access_token = create_access_token(data={"sub": datas["openid"]})
      return {"code":1,"data":access_token}
    return {"code":0, "data":"获取用户信息失败"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, Setting.SECRET_KEY, algorithms=[Setting.ALGORITHM])
        openid:str = payload.get("sub")
        if openid is None:
            raise credentials_exception
        
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_db_user(db, openid=openid)
    return user
    
def get_db_user(db:Session,openid:str):
    return db.scalars(Select(User).where(User.open_id == openid)).first()

def get_admin_user(token:str = Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, Setting.SECRET_KEY, algorithms=[Setting.ALGORITHM])
        openid:str = payload.get("sub")
        if openid is None:
            raise credentials_exception
        
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_db_user(db, openid=openid)
    if not user:
        raise credentials_exception
    print(f"is admin:{user.is_admin}")
    
    if user.is_admin != 1:
        raise credentials_exception
        
    return user
    
    