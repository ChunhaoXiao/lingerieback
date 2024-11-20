import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column,column_property
from sqlalchemy import DateTime, ForeignKey, ForeignKey, String, func, select

class ChargeLock(Base):
    __tablename__="charge_lock"
    id:Mapped[int] = mapped_column(primary_key=True)
    ip_address:Mapped[str] = mapped_column(String(50))
    cnt:Mapped[int] = mapped_column(default=1)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())