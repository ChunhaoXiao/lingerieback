from fastapi.staticfiles import StaticFiles
from db.base import Base
from db.session import engine
from fastapi import FastAPI,Depends
from apis.base import api_router
from db.session import get_db
import os, time
from core.config import Setting

#os.environ['TZ'] = 'Asia/Shanghai'
#time.tzset()

Base.metadata.create_all(engine)    
app = FastAPI()
app.include_router(api_router)
import pathlib
pt = pathlib.Path(__file__).parent.resolve()
from db.seed import seed_data,get_unsplash_images
seed_data()
app.mount("/static", StaticFiles(directory=Setting.STATIC_DIR), name="static")


    