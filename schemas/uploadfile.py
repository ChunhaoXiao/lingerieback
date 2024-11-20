from pydantic import computed_field, field_serializer, BaseModel
from core.config import Setting

class UploadResponse(BaseModel):
    file_name:str
    #full_path:str | None = None
    
    @computed_field
    @property
    def full_path(self)->str:
        return Setting.STATIC_URL+self.file_name