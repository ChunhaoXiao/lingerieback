from sqlalchemy.orm import session, selectinload, Session

from db.models.post import Post
from db.models.post_statistic import PostStatistic

def update_like_cnt(db:Session, post:Post, cnt:int):
    if not post.statistic:
        statistic = PostStatistic(like_cnt=1,post=post)
        db.add(statistic)
        db.commit()
    else:
        if post.statistic.like_cnt + cnt < 0:
            return
        statistic = post.statistic
        statistic.like_cnt = statistic.like_cnt+cnt
        db.commit()
    

def update_collection_cnt(db:Session, post:Post, cnt:int):
    
    if not post.statistic:
        statistic = PostStatistic(collection_cnt=1,post=post)
        db.add(statistic)
        db.commit()
    else:
        if post.statistic.collection_cnt+cnt < 0:
            return 
        statistic = post.statistic
        statistic.collection_cnt = statistic.collection_cnt+cnt
        db.commit()
        
def update_view_cnt(db:Session,post:Post):
    print(f"post statistic=================================>{post.statistic}")
    if not post.statistic:
        print("dont has statistic##################################################")
        statistic = PostStatistic(view_cnt=1,post=post)
        db.add(statistic)
        db.commit()
    else:
        print("has statistic=============================================>")
        statistic = post.statistic
        print(f"statistic id is:{statistic.id}")
        cnt = statistic.view_cnt
        print(f"statistic cnt================================>{cnt}")
        statistic.view_cnt = cnt+1
        db.commit()