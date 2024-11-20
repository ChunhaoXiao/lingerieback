import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column,column_property
from sqlalchemy import DateTime, ForeignKey, ForeignKey, String, func, select

class Card(Base):
    __tablename__="cards"
    id:Mapped[int] = mapped_column(primary_key=True)
    number:Mapped[str] = mapped_column(String(50))
    period:Mapped[int]
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=True)
    used_at:Mapped[datetime.datetime] = mapped_column(nullable=True)
    group_id:Mapped[int] = mapped_column(ForeignKey("card_groups.id"))
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    card_group:Mapped["CardGroup"] = relationship(back_populates="cards") # type: ignore
    
    user:Mapped["User"] = relationship() # type: ignore

    
    