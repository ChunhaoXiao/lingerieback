from pydantic import computed_field, field_serializer, BaseModel
import datetime

from schemas.post import PostShow
class LikeResponse(BaseModel):
    id:int
    created_at:datetime.datetime | None=None
    post:PostShow | None=None
    