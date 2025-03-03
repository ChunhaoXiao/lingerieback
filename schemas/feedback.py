from pydantic import Field, Secret, BaseModel, computed_field
import datetime
from core.config import Setting
from schemas.user import User as UserShema
import arrow

class FeedBack(BaseModel):
    description:str = Field(min_length=10,max_length=300)
    files:list[str] |None=[]
    
class FeebBackResponse(BaseModel):
    id:int
    description:str
    files:str |None = None
    User:UserShema |None = None
    created_at:datetime.datetime
    
    @computed_field
    @property
    def file_list(self) -> list[str]:
        #return [item for item in self.files.split(",")]
        if not self.files:
            return []
        file_list = []
        for item in self.files.split(","):
            file_list.append(f"{Setting.STATIC_URL}{Setting.UPLOAD_DIR}/{item}")
        return file_list
    
    @computed_field
    @property
    def created(self) -> str:
        utc = arrow.get(self.created_at)
        local = utc.to('US/Pacific')
        return local.humanize(locale='zh-cn')
        
    
    