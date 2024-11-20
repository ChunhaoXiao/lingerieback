import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column
from sqlalchemy import DateTime, ForeignKey, ForeignKey, String, func


class Media(Base):
    __tablename__="media"
    id:Mapped[int] = mapped_column(primary_key=True)
    url:Mapped[str] = mapped_column(String(200))
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post:Mapped["Post"] = relationship(back_populates="files") # type: ignore
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"Media(id={self.id},url={self.url},post_id={self.post_id})"