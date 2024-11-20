from pydantic import Field, BaseModel

class PostRequest(BaseModel):
    page:int = Field(default=1)
    category_id:int = Field(default=0)
    is_vip:int = Field(default=0)
    keyword:str = Field(default="")
    type:str | None=None