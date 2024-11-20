import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, ForeignKey, DateTime, String, func

class Vip(Base):
    __tablename__="vip_user"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column() 
    open_id:Mapped[str] = mapped_column(String(100))
    expire_date:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    user:Mapped["User"] = relationship(back_populates="vip") # type: ignore
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())