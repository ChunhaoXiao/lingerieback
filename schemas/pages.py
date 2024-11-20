from fastapi import Query
from pydantic import computed_field, field_serializer, BaseModel



class Page(BaseModel):
    page:int
    per_page:int

def page_params(page:int = Query(default=1),per_page:int=Query(default=20)):
    return Page(page=page,per_page=per_page)