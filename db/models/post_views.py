
import datetime
from db.models.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey, ForeignKey, DateTime, String, func,Index, text

class PostView(Base):
    __tablename__="post_views"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int]
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post:Mapped["Post"] = relationship(back_populates="views") # type: ignore
    #created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
Index('view_index', PostView.user_id, PostView.post_id)