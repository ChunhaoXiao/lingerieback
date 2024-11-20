from pydantic import computed_field, field_serializer, BaseModel
from datetime import datetime
import arrow
from core.config import Setting
class NoticeCreate(BaseModel):
    title:str
    content:str
    position:list[str]
    enabled:str | None=1
    pictures:list[str] | None= None

class NoticePosition(BaseModel):
    id:int
    postion_name:str
    start_time:datetime |None=None
    end_time:datetime |None=None
    
    pass
    
class NoticeResponse(BaseModel):
    id:int
    title:str
    content:str
    positions:list[NoticePosition] | None=None
    enabled:int | None=1
    pictures:str | None= None
    created_at:datetime
    
    @computed_field
    @property
    def created(self) -> str:
        utc = arrow.get(self.created_at)
        local = utc.to('US/Pacific')
        return local.humanize(locale='zh-cn')
    
    @field_serializer('pictures')
    def pictures_serializer(self, pictures: str, _info):
        if pictures:
            return pictures.split(",")
        return []
    
    @computed_field
    @property
    def picture_full_path(self) -> str:
        pic_list = []
        if self.pictures:
            pics = self.pictures.split(",")
            for item in pics:
                pic_list.append(f"{Setting.STATIC_URL}{item}")
        return pic_list
            
            
        