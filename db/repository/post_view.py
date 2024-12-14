from db.models.post import Post
from db.models.post_views import PostView
from db.models.user import User
from sqlalchemy import func, func, select
from sqlalchemy.orm import Session
import datetime

from db.repository.statistic import update_view_cnt

def save_view_log(post, user,db):
    print("execute post view save log.......")
    view = db.scalars(select(PostView).where(PostView.post_id == post.id,PostView.user_id==user.id)).first()
    print(f"view is:=====>{view}")
    if view:
        print("has view==============================================")
        #view.updated_at = datetime.datetime.now()
        view.updated_at=func.now()
        db.commit()
    else:
        print("NOT has VIEW=====================================")
        view = PostView(post_id=post.id, user_id=user.id)
        db.add(view)
        db.commit()
        print("will update view cnt~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("post is========================>")
        update_view_cnt(db,post)
        
    