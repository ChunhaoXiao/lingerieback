
from schemas.post import PostCreate
from sqlalchemy.orm import query, session, selectinload, Session
from sqlalchemy import Select, func,select
from db.models.post import Post
from db.models.media import Media
from db.models.likes import Likes
from db.models.collection import Collection
from schemas.post_request import PostRequest

def create_post(post: PostCreate, db: Session):
    files = []
    for item in post.files:
        files.append(Media(url=item))
    
    post = Post(**post.model_dump(exclude={'files'}))
    post.files = files
    post.author="zhang san"
    print(f"post to be saved:{post}")
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post(db:Session,params:PostRequest, is_vip:int):
    page = params.page
    category_id = params.category_id
    keyword = params.keyword
    type = params.type
    
    query = Select(Post).options(selectinload(Post.files))
    if category_id > 0:
        query = query.where(Post.category_id == category_id)
    if is_vip == 0:
        query = query.where(Post.is_vip == 0)
    if keyword:
        print(f"keyword is:::{keyword}")
        query = query.where(Post.title.like(f"%{keyword}%"))
    if type =='vip':
        query = query.where(Post.is_vip == 1)
    if type == 'recommand':
        query = query.where(Post.is_recommand == 1)
    if type == 'hot':
        query = query.where(Post.is_hot == 1)
        
    query = query.limit(15).offset((page-1) * 15).order_by(Post.id.desc())
    
    return  db.scalars(query).all()
    
    # query = Select(Post).options(selectinload(Post.files)).limit(15).offset((page-1) * 15).order_by(Post.id.desc())
    # return db.scalars(query).all()

def show_post_detail(db:Session, id:int):
    query = select(Post,func.count(Likes.id).label("like_cnt"),func.count(Collection.id).label("collect_cnt")).options(selectinload(Post.files)).options(selectinload(Post.category)).join(Likes, Post.id==Likes.post_id,isouter=True).join(Collection, Post.id==Collection.post_id, isouter=True).where(Post.id == id)
    return db.execute(query).all()

def find_post(db:Session, id:int):
    return db.scalars(select(Post).where(Post.id==id)).first()

def update_post(id:int,post:PostCreate, db:Session):
    db_post = db.scalars(select(Post).where(Post.id==id)).one()
    
    for f in db_post.files:
        db.delete(f)
    for media in db_post.files:
        db_post.files.remove(media)
        
    for item in post.files:
        db_post.files.append(Media(url=item))
    
    db_post.author="zhang san"
    db_post.category_id=post.category_id
    db_post.title = post.title
    db_post.description = post.description
    db_post.is_vip = post.is_vip
    db_post.is_recommand=post.is_recommand
    db_post.is_hot=post.is_hot
    print(f"db_post:{db_post}")
    db.commit()
    
def removePost(id:int, db:Session):
    post = db.scalars(select(Post).where(Post.id==id)).one()
    print(f"post to be delete is:{post}")
    db.delete(post)
    db.commit()
    