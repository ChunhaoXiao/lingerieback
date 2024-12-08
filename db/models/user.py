import datetime
from db.models.base_class import Base
from sqlalchemy.orm import column_property, relationship, Mapped, mapped_column,deferred
from sqlalchemy import DateTime, String, func
import arrow
from sqlalchemy.ext.hybrid import hybrid_property

class User(Base):
    __tablename__='users'
    id:Mapped[int] = mapped_column(primary_key=True)
    open_id:Mapped[str] = mapped_column(String(128))
    name:Mapped[str] = mapped_column(String(50), default="")
    avatar:Mapped[str] = mapped_column(String(150), default="")
    vip:Mapped["Vip"] = relationship(back_populates="user") # type: ignore
   # card:Mapped["Card"]
    is_admin:Mapped[int] = mapped_column(default=0)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    @hybrid_property
    def is_valid_vip(self):
        if self.is_admin == 1:
            return True
        if self.vip and self.vip.expire_date > datetime.datetime.now():
            return True
        return False
   # created:Mapped[str] = deferred("aaa")
    
    