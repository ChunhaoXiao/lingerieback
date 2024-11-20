from sqlalchemy import ForeignKey, String,DateTime,func
from db.models.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
import datetime

from db.models.notice import Notice

class NoticePosition(Base):
    __tablename__="notice_position"
    id:Mapped[int] = mapped_column(primary_key=True)
    notice_id:Mapped[int] = mapped_column(ForeignKey("notice.id"))
    postion_name:Mapped[str] = mapped_column(String(100))
    start_time:Mapped[datetime.datetime] = mapped_column(nullable=True)
    end_time:Mapped[datetime.datetime] = mapped_column(nullable=True)
    notice:Mapped[Notice] = relationship(back_populates="positions")
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())