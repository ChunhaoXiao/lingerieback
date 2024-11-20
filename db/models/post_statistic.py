
import datetime
from db.models.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey, ForeignKey, DateTime, String, func

class PostStatistic(Base):
    __tablename__="post_statistic"
    id:Mapped[int] = mapped_column(primary_key=True)
    like_cnt:Mapped[int] = mapped_column(default=0)
    collection_cnt:Mapped[int] = mapped_column(default=0)
    view_cnt:Mapped[int] = mapped_column(default=0)
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post:Mapped["Post"] = relationship(back_populates="statistic") # type: ignore
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    