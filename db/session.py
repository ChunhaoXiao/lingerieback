from sqlalchemy import select, select, create_engine
from core.config import Setting
from sqlalchemy.orm import session, Session
from db.models.category import Category

# host = Setting.DB_HOST
# password = Setting.DB_PASSWORD
# user = Setting.DB_USER
# database = Setting.DB_NAME


user = "root"
password = "123456"
host= "db"
database= "lingerie"


engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}?charset=utf8mb4")
session = Session(engine)
#cates = session.scalars(select(Category)).all()
#print(f"cates in database are:::{cates}")

def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

