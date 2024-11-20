
import datetime
from db.models.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Text, Text, ForeignKey, ForeignKey, DateTime, String, func

class Likes(Base):
    __tablename__="post_likes"
    id:Mapped[int] = mapped_column(primary_key=True)
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    post:Mapped["Post"] = relationship(back_populates="likes") # type: ignore