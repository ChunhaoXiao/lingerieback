from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from db.models.vip import Vip
from db.session import get_db
from sqlalchemy import func, func, select,Date,cast
from db.models.post_statistic import PostStatistic
from db.models.post_views import PostView
from db.models.likes import Likes
from db.models.user import User
import datetime

router = APIRouter(prefix="/api/admin/stats")

@router.get("/index")
def index(db:Session=Depends(get_db)):
    result = {}
    yesterday = (datetime.datetime.now()- datetime.timedelta(1)).date()
    #阅读数
    stmt = select(func.count(PostView.id)).select_from(PostView).where(cast(PostView.updated_at,Date)==yesterday)
    read_cnt = db.scalars(stmt).first()
    
    #点赞数
    stmt = select(func.count(Likes.id)).select_from(Likes).where(cast(Likes.created_at,Date) == yesterday)
    like_cnt = db.scalars(stmt).first()

    #用户数量
    stmt = select(func.count(User.id)).select_from(User).where(cast(User.created_at,Date)==yesterday)
    user_cnt = db.scalars(stmt).first()
    #新增VIP用户数量
    new_vip_user_cnt = db.scalars(select(func.count(Vip.id)).select_from().where(cast(Vip.created_at,Date)==yesterday)).first()
    
    result["read_cnt"] = read_cnt
    result["like_cnt"] = like_cnt
    result["user_cnt"] = user_cnt
    result["new_vip_cnt"] = new_vip_user_cnt
    
    return {"code":1,"data":result}
    
    