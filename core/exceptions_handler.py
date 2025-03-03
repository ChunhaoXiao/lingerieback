from fastapi import FastAPI, HTTPException,Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app import app
from core.validations import msg 

#from main  import app

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request, exc:RequestValidationError):
    first_error = exc.errors()[0]
    print(f"first error is:{first_error}")
    validation_error_msg  = first_error['msg']
    type= first_error['type']
    # default_msg = exc.errors[0]['msg']
    # print(f"defauot msg:{default_msg}")
    print(f"type is:#######{type}")
    if type in msg:
        print(f"fields is:{first_error['loc'][1]}")
        field_name = first_error['loc'][1]
        if 'ctx' in first_error:
            ctx =first_error['ctx']
            print(f"ctx is:####{ctx}")
            if 'min_length' in ctx:
                validation_error_msg = f"{field_name}{msg[type]}{ ctx['min_length']}个字符"
            if 'max_length' in ctx:
                validation_error_msg = f"{field_name}{msg[type]}{ ctx['max_length']}个字符"
        if type=='missing':
            validation_error_msg = f"{field_name}不能为空"
        if type == 'too_short':
            validation_error_msg = f"{field_name}不能为空"
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": [validation_error_msg], "body": exc.body}),
    )