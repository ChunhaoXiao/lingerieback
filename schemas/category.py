from pydantic import computed_field, BaseModel
from core.config import Setting

class Category(BaseModel):
    id:int
    name:str
    enabled:int | None = None
    icon:str | None=None
    
    
    @computed_field
    @property
    def pic_path(self)->str:
        return Setting.STATIC_URL+self.icon

class CategoryCreate(BaseModel):
    name:str
    enabled:int | None = None
    icon:str | None=None
    
class CategoryResponse(BaseModel):
    Category:Category
    cnt:int | None=None
    
        
