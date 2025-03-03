import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column
from sqlalchemy import DateTime, ForeignKey, ForeignKey, String, func

class Notice(Base):
    __tablename__="notice"
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(200))
    content:Mapped[str] = mapped_column(String(3000))
    enabled:Mapped[int] = mapped_column(default=1)
    start_time:Mapped[str] = mapped_column(String(100), default="")
    end_time:Mapped[str] = mapped_column(String(100),default="")
    pictures:Mapped[str] = mapped_column(String(500), default="")
    positions:Mapped[list["NoticePosition"]] = relationship(back_populates="notice",cascade="all, delete-orphan") # type: ignore
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())