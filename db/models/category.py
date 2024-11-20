import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column,column_property
from sqlalchemy import DateTime, ForeignKey, ForeignKey, String, func, select
from db.models.post import Post

class Category(Base):
    __tablename__="categories"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100)) 
    enabled:Mapped[int] = mapped_column(default=1)
    icon:Mapped[str] = mapped_column(String(200), nullable=True)
    posts:Mapped[list["Post"]] = relationship(back_populates="category") # type: ignore
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    post_count=column_property(
        select(func.count(Post.id))
        .where(Post.category_id == id)
        .correlate_except(Post)
        .scalar_subquery()
    )