from sqlalchemy.orm import Session
from sqlalchemy import func, func, select,delete
from db.models.post import Post

from db.models.likes import Likes

def add_like(db:Session, user_id:int, post:Post):
    stmt = select(func.count(Likes.id)).select_from(Likes).where(Likes.post_id==post.id,Likes.user_id==user_id)
    cnt = db.scalars(stmt).first()
    print(f"count is:{cnt}")
    if cnt > 0:
        db.execute(delete(Likes).where(Likes.post_id==post.id,Likes.user_id==user_id))
        db.commit()
        return -1
        
    print(f"post in add like:::{post}")
    likes = Likes(user_id=user_id, post=post)
    db.add(likes)
    db.commit()
    return 1
    