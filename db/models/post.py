
import datetime
from db.models.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey, ForeignKey, DateTime, String, func

class Post(Base):
    __tablename__="posts"
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(100))
    author:Mapped[str] = mapped_column(String(100))  
    is_vip:Mapped[int] = mapped_column(default=1)
    is_recommand:Mapped[int] = mapped_column(default=0)
    is_hot:Mapped[int] = mapped_column(default=0)
    description:Mapped[str]= mapped_column(String(1000), default="")
    files:Mapped[list["Media"]] = relationship(back_populates="post", cascade="all, delete-orphan") # type: ignore
    likes:Mapped[list["Likes"]] = relationship(back_populates="post", cascade="all, delete-orphan") # type: ignore
    views:Mapped[list["PostView"]] = relationship(back_populates="post", cascade="all, delete-orphan") # type: ignore
    collections:Mapped[list["Collection"]] = relationship(back_populates="post", cascade="all, delete-orphan") # type: ignore
    category_id:Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category:Mapped["Category"] = relationship(back_populates="posts") # type: ignore
    statistic:Mapped["PostStatistic"] = relationship(back_populates="post",cascade="all, delete-orphan") # type: ignore
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"Post({self.id},{self.title})"