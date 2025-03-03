import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column,column_property
from sqlalchemy import DateTime, ForeignKey, ForeignKey, String, func, select

class TempUploadedFile(Base):
    __tablename__="temp_uploaded_files"
    id:Mapped[int] = mapped_column(primary_key=True)
    file_name:Mapped[str] = mapped_column(String(300))
    user_id:Mapped[int]
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())