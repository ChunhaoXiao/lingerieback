from datetime import datetime, timedelta, timezone
from core.config import Setting
import jwt

def create_access_token(data:dict, expires_delta:timedelta | None=None):
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Setting.SECRET_KEY, algorithm=Setting.ALGORITHM)
    return encoded_jwt