from pydantic import BaseModel, computed_field, field_serializer, model_serializer
from core.config import Setting
from schemas.category import Category
import datetime 

import arrow

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
    is_admin:int | None=None
    
    @computed_field
    @property
    def created(self) -> str:
        utc = arrow.get(self.created_at)
        local = utc.to('US/Pacific')
        return local.humanize(locale='zh-cn')
    
    #collection:list["Likes"]
    # like_cnt:int | None=0
    # collection_cnt:int |None=0
    
    
class MediaShow(BaseModel):
    id:int
    url:str
    @computed_field
    @property
    def fullpath(self) -> str:
        #return f"{Setting.STATIC_URL}{self.url}"
        if "http" in self.url:
            return self.url
        return f"{Setting.STATIC_URL}{self.url}"
    
class Likes(BaseModel):
    id:int
    user_id:int
    post_id:int
        