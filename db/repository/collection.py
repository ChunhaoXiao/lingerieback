from sqlalchemy.orm import Session
from sqlalchemy import func, func, select,delete
from db.models.post import Post
from db.models.collection import Collection

def add_collection(db:Session,user_id:int, post:Post):
    stmt = select(func.count(Collection.id)).select_from(Collection).where(Collection.post_id==post.id,Collection.user_id==user_id)
    cnt = db.scalars(stmt).first()
    if cnt > 0:
        db.execute(delete(Collection).where(Collection.post_id==post.id,Collection.user_id==user_id))
        db.commit()
        return -1
    
    collection = Collection(user_id=user_id,post=post)
    db.add(collection)
    db.commit()
    return 1
    