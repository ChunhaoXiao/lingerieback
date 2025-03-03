
from schemas.post import PostCreate
from sqlalchemy.orm import query, session, selectinload, Session
from sqlalchemy import desc, desc, over, over, Select, func,select
from db.models.post import Post
from db.models.media import Media
from db.models.likes import Likes
from db.models.collection import Collection
from schemas.post_request import PostRequest
import cv2
from core.config import Setting
import os
from db.redis import get_config

from PIL import Image, ImageDraw
from db.models.category import Category

def create_post(post: PostCreate, db: Session):
    files = []
    for item in post.files:
        is_video = 0
        if ".mp4" in item:
            get_video_image(item)
            print("is mp4")
            is_video=1
            # cam = cv2.VideoCapture(f"{Setting.STATIC_DIR}/{item}")
            # cam.set(cv2.CAP_PROP_POS_MSEC,2000)
            # ret,frame = cam.read()
            # name = Setting.STATIC_DIR+"/test111.jpg"
            # print(f"frame is:{frame}")
            # cv2.imwrite(name,frame)
            # is_video=1
            
            #cam.release()
            #cv2.destroyAllWindows()
            
        files.append(Media(url=item,is_video=is_video))
    
    post = Post(**post.model_dump(exclude={'files'}))
    post.files = files
    post.author="zhang san"
    print(f"post to be saved:{post}")
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post(db:Session,params:PostRequest, is_vip:int,include_hide:int=0,all_category:int=0):
    page = params.page
    category_id = params.category_id
    keyword = params.keyword
    type = params.type
    orderby=params.order_by
    
    query = Select(Post, func.count(Post.likes).label("like_cnt")).join(Post.likes,isouter=True).options(selectinload(Post.files))
    if category_id:
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
    if type == 'hidden':
        query = query.where(Post.is_hide == 1)
    if include_hide == 0:
        query = query.where(Post.is_hide == 0)
    if all_category == 0:
        query = query.where(Post.category.has(Category.enabled == 1))
    #query = query.where(Post.is_hide ==0)
    perpage = int(get_config('category-list-count'))
    if orderby =='id':
      query = query.group_by(Post.id).limit(perpage).offset((page-1) * perpage).order_by(Post.id.desc())
    else:
      query = query.group_by(Post.id).limit(perpage).offset((page-1) * perpage).order_by(desc("like_cnt"))
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
    is_video = 0
    for item in post.files:
        if ".mp4" in item:
            get_video_image(item)
            is_video=1
        db_post.files.append(Media(url=item,is_video=is_video))
    
    db_post.author="admin"
    db_post.category_id=post.category_id
    db_post.title = post.title
    db_post.description = post.description
    db_post.is_vip = post.is_vip
    db_post.is_recommand=post.is_recommand
    db_post.is_hot=post.is_hot
    db_post.is_hide=post.is_hide
    print(f"db_post:{db_post}")
    db.commit()
    
def removePost(id:int, db:Session):
    post = db.scalars(select(Post).where(Post.id==id)).one()
    print(f"post to be delete is:{post}")
    db.delete(post)
    db.commit()
    
def get_video_image(url):
    file_name = os.path.basename(url)
    cam = cv2.VideoCapture(f"{Setting.STATIC_DIR}/{Setting.UPLOAD_DIR}/{url}")
    cam.set(cv2.CAP_PROP_POS_MSEC,2000)
    ret,frame = cam.read()
    name =f"{Setting.STATIC_DIR}/{Setting.UPLOAD_DIR}/{file_name}.jpg"
    print(f"name is:{name}")
    cv2.imwrite(name,frame)
    
    
    #加水印
    
    add_icon_to_image(name, name)
    """
    img = cv2.imread(name)
    # Read the watermark image
    wm = cv2.imread(f"{Setting.STATIC_DIR}/video-icon.jpeg")
    print(f"vm is:##########{wm}")
    # height and width of the watermark image
    h_wm, w_wm = wm.shape[:2]
    print(f"h_wm is{h_wm},w_wm is:{w_wm}")
    # height and width of the image
    h_img, w_img = img.shape[:2]

    # calculate coordinates of center of image
    center_x = int(w_img/2)
    center_y = int(h_img/2)
    
    # calculate rio from top, bottom, right and left
    top_y = center_y - int(h_wm/2)
    left_x = center_x - int(w_wm/2)
    bottom_y = top_y + h_wm
    right_x = left_x + w_wm

    # add watermark to the image
    roi = img[top_y:bottom_y, left_x:right_x]
    result = cv2.addWeighted(roi, 1, wm, 0.3, 0)
    img[top_y:bottom_y, left_x:right_x] = result
    cv2.imwrite(name,img=img)
    """
    

def add_icon_to_image(file_name,out_filename):
    image = Image.open(file_name)
    w = image.width
    h = image.height
    iconheight=250
    iconwidth =200
    draw = ImageDraw.Draw(image)
    draw.rectangle([w/2-iconwidth/2, h/2-iconheight/2,w/2+iconwidth, h/2+iconheight/2],fill="gray")

    draw.polygon(((w/2-iconwidth/2, h/2+iconheight/2), (w/2+iconwidth, h/2), (w/2-iconwidth/2, h/2-iconheight/2)),fill="white")  # Draw a rectangle with top-left corner at (100, 100) and bottom-right corner at (320, 320)
    image.save(out_filename)