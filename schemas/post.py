from pydantic import BaseModel, computed_field, field_serializer, model_serializer
from core.config import Setting
from schemas.category import Category
import datetime 

import arrow
import os

class PostCreate(BaseModel):
    title:str
    category_id:int
    is_vip:int | None=1
    is_recommand:int | None=0
    is_hot:int | None=0
    description:str | None=None
    files:list[str]
    
class MediaPost(BaseModel):
    url:str
    
class Statistic(BaseModel):
    like_cnt:int |None=0
    collection_cnt:int | None=0
    view_cnt:int | None = 0
    
class PostShow(BaseModel):
    id:int 
    title:str
    is_vip:int
    description:str
    is_recommand:int | None=0
    is_hot:int |None=0
    files:list["MediaShow"]
    category:Category | None=None
    likes:list["Likes"] | None=None
    collections:list["Likes"] | None=None
    statistic:Statistic | None =None
    created_at:datetime.datetime
    
    @computed_field
    @property
    def created(self) -> str:
        utc = arrow.get(self.created_at)
        local = utc.to('US/Pacific')
        return local.humanize(locale='zh-cn')
    
    @computed_field
    @property
    def list_cover(self) -> str:
        if  len(self.files)==1 and ".mp4" in self.files[0].url:
            image_file = os.path.basename(self.files[0].url)
            file_name = image_file+'.jpg'
            return f"{Setting.STATIC_URL}/{Setting.UPLOAD_DIR}/{file_name}"
        if "http" in self.files[0].url:
            return self.files[0].url
        return f"{Setting.STATIC_URL}/{Setting.UPLOAD_DIR}/{self.files[0].url}"
    
    @computed_field
    @property
    def is_video(self)->bool:
        return len(self.files)==1 and ".mp4" in self.files[0].url
        
    
    @computed_field
    @property
    def video_img(self)->str:
        if len(self.files)==1 and ".mp4" in self.files[0].url:
            print(f"self.files[0].url::::{self.files[0].url}")
            image_file = os.path.basename(self.files[0].url)
            print(f"image_file::::{image_file}")
            file_name = image_file+'.jpg'
            return f"{Setting.STATIC_URL}/{Setting.UPLOAD_DIR}/{file_name}"
        return ""
    
    #collection:list["Likes"]
    # like_cnt:int | None=0
    # collection_cnt:int |None=0
    
    
class MediaShow(BaseModel):
    id:int
    url:str
    is_video:int
    @computed_field
    @property
    def fullpath(self) -> str:
        #return f"{Setting.STATIC_URL}{self.url}"
        if "http" in self.url:
            return self.url
        return f"{Setting.STATIC_URL}{Setting.UPLOAD_DIR}/{self.url}"
    
class Likes(BaseModel):
    id:int
    user_id:int
    post_id:int
        