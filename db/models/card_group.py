import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column,column_property
from sqlalchemy import Text, Text, DateTime, ForeignKey, ForeignKey, String, func, select

class CardGroup(Base):
    __tablename__="card_groups"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    quantity:Mapped[int]
    period:Mapped[int]
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    cards:Mapped[list["Card"]] = relationship(back_populates="card_group",cascade="all, delete-orphan") # type: ignore