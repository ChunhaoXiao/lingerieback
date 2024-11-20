from fastapi import Depends, APIRouter, HTTPException,status,BackgroundTasks
from sqlalchemy.orm import Session
from db.models.post_statistic import PostStatistic
from db.session import get_db
from db.models.user import User
from apis.v1.route_login import get_current_user
from db.repository.like import add_like 
from db.repository.post import show_post_detail,find_post
from db.models.post import Post
from db.repository.statistic import update_like_cnt


router = APIRouter(prefix="/api/like")

@router.post("/{post_id}")
def save_like(post_id:int, background_tasks: BackgroundTasks,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    post = find_post(db,post_id)
    print(f"post is::::{post}")
    cnt = add_like(db=db,user_id=current_user.id,post=post)
    background_tasks.add_task(update_like_cnt(db,post,cnt))
    return {"code":1,"data":"success"}

    