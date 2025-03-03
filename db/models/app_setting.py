import datetime
from db.models.base_class import Base
from sqlalchemy.orm import relationship, Mapped,mapped_column,column_property
from sqlalchemy import Text, Text, DateTime, ForeignKey, ForeignKey, String, func, select

class AppSetting(Base):
    __tablename__="app_setting"
    id:Mapped[int] = mapped_column(primary_key=True)
    setting_name:Mapped[str] = mapped_column(String(100))
    setting_value:Mapped[str] = mapped_column(String(100))
    type:Mapped[str] = mapped_column(String(50))
    description:Mapped[str] = mapped_column(String(100), nullable=True)
    last_update_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())