
from pydantic import computed_field, BaseModel
import datetime

import arrow
class User(BaseModel):
    name:str
    open_id:str |None=None
    #age:int = 
    
class Vip(BaseModel):
    id:int
    user_id:int
    expire_date:datetime.datetime
    
    @computed_field
    @property
    def vip_expire_date(self)->str:
        if not self.expire_date:
            return ""
        return self.expire_date.strftime('%Y-%m-%d')
    
    
class UserResponse(BaseModel):
    id:int
    name:str | None=None
    open_id:str | None = None
    created_at:datetime.datetime
    is_admin:int
    vip:Vip | None = None
    # last_visit_time:str |None=None
    # view_cnt:int |None=0
    #open_id:str | None = None
    
    #vip:Vip | None =None
    @computed_field
    @property
    def created(self) -> str:
        utc = arrow.get(self.created_at)
        local = utc.to('US/Pacific')
        return local.humanize(locale='zh-cn')
    
class UserListResponse(BaseModel):
    users:list[UserResponse]
    total_cnt:int | None = 0
    vip_cnt:int | None = 0

class UserDetailResponse(BaseModel):
    user:UserResponse
    last_visit_time:datetime.datetime |None = None
    total_view:int |None=None
    like_cnt:int | None=None
    
class UserRequest(BaseModel):
    name:str | None= None
    vip_period:int | None=None
    
class UserParam(BaseModel):
    name:str | None=None
    vip:int | None = None
    page:int | None = 1

    