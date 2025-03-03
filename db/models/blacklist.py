import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column,column_property
from sqlalchemy import Text, Text, DateTime, ForeignKey, ForeignKey, String, func, select

class BlackList(Base):
    __tablename__="black_list"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[str] = mapped_column(String(50))
    expire_time:Mapped[datetime.datetime] = mapped_column(nullable=True)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    