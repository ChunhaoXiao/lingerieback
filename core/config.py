from dotenv import load_dotenv
import os
from os.path import join, dirname
from pathlib import Path


dotenv_path = join(dirname(dirname(__file__)), '.uat.env')
print(f"dotenvpath is:{dotenv_path}")

load_dotenv(dotenv_path,override=True)

class Settings:
    
    DB_USER:str = os.getenv("DB_USER")
    DB_PASSWORD:str = os.getenv("DB_PASSWORD")
    DB_HOST:str = os.getenv("DB_HOST")
    DB_NAME:str = os.getenv("DB_NAME")
    DB_PORT:str = os.getenv("DB_PORT")
    REDIS_HOST:str = os.getenv("REDIS_HOST")
    STATIC_URL:str = os.getenv("STATIC_URL")
    SECRET_KEY:str = os.getenv("SECRET_KEY")
    ALGORITHM:str = os.getenv("ALGORITHM")
    APP_ID:str = os.getenv("APPID")
    APP_SECRET:str = os.getenv("APPSECRET")
    STATIC_DIR:str = os.getenv("STATIC_DIR")
    ADMIN_OPENID = os.getenv("ADMIN_OPENID")
    UPLOAD_DIR:str = os.getenv("UPLOAD_DIR")
    

Setting = Settings()



    
