from fastapi import BackgroundTasks, Depends, APIRouter, HTTPException,status
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.user import User
from apis.v1.route_login import get_current_user
from db.repository.collection import add_collection 
from db.repository.post import show_post_detail,find_post
from db.repository.statistic import update_collection_cnt


router = APIRouter(prefix="/api/collection")

@router.post("/{post_id}")

def save_collection(post_id:int,background_tasks: BackgroundTasks, db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    post = find_post(db,post_id)
    cnt = add_collection(db=db, user_id=current_user.id,post=post)
    background_tasks.add_task(update_collection_cnt(db, post,cnt))
    
    return {"code":1, "data":"success"}


