
import datetime
from db.models.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Text, Text, ForeignKey, ForeignKey, DateTime, String, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property

class FeedBack(Base):
    __tablename__="feed_back"
    id:Mapped[int] = mapped_column(primary_key=True)
    description:Mapped[str] = mapped_column(String(1000))
    #files = mapped_column("files",String)
    files:Mapped[str] = mapped_column(String(500),nullable=True)
    user_id:Mapped[int]
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    
    # @hybrid_property
    # def filess(self):
    #     return self.files.split(",")

    # @files.setter
    # def files(self, fileslist):
    #     self.files = ",".join(fileslist)