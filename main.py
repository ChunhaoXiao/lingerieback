from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import redis
from db.base import Base
from db.session import engine
from fastapi import FastAPI,Depends, Request
from apis.base import api_router
from db.session import get_db
import os, time
from core.config import Setting
from db.repository.app_setting import set_app_config
from app import app
from db.redis import get_config
from starlette.responses import Response
#os.environ['TZ'] = 'Asia/Shanghai'
#time.tzset()

Base.metadata.create_all(engine)    
# = FastAPI() #FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)
print(f"redis is:{redis}")

app.include_router(api_router)
import pathlib
pt = pathlib.Path(__file__).parent.resolve()
from db.seed import seed_data,get_unsplash_images
seed_data()
set_app_config()



print("seeded......................................................................")
app.mount("/static", StaticFiles(directory=Setting.STATIC_DIR), name="static")

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request:Request, exc:RequestValidationError):
#     print(f"body is:{exc.body}, error is:{exc.errors()}")
    
#     return JSONResponse(
#         #status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": "aassdsadsadasds", "body": exc.body}),
#     )


@app.middleware("http")
async def check_is_open(request:Request, call_next):
    urls = request.url
    print(f"request middle ware.......{urls}")
    response = await call_next(request)
    is_open = get_config("app_status")
    print(f"response is#######{response}")
    print(f"is open======{is_open}")
    
    if is_open == "0":
        if "admin" not  in str(urls) and "/me" not in str(urls):
            print("closed================")
            response.status_code=499
            #return {"code":0,"data":"closed"}
            return response
    
    return response


