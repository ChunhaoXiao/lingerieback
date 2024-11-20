from db.models.charge_lock import ChargeLock
from sqlalchemy.orm import Session
from sqlalchemy import delete, delete, select
import datetime

def save_lock(ip_address:str,db:Session):
    data = db.scalars(select(ChargeLock).where(ChargeLock.ip_address == ip_address)).first()
    if not data:
        db.add(ChargeLock(ip_address=ip_address))
        db.commit()
    else:
        if (datetime.datetime.now() - data.created_at).total_seconds() > 600:
            data.cnt = 1
            data.created_at = datetime.datetime.now()
        else:
            data.cnt = data.cnt+1
        db.commit()        
             
def is_locked(ip_address:str, db:Session):
    data = db.scalars(select(ChargeLock).where(ChargeLock.ip_address == ip_address,ChargeLock.cnt == 5)).first()
    if not data:
        return False
    if (datetime.datetime.now()-data.created_at).total_seconds()>600:
        db.delete(data)
        db.commit()
        return False
    return True
    