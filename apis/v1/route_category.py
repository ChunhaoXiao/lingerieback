from fastapi import Depends, APIRouter, HTTPException
from db.session import get_db
from schemas.category import Category,CategoryCreate,CategoryResponse
from sqlalchemy.orm import Session;
from db.models.category import Category as DbCategory
from schemas.base_response import GenericResponse
from db.repository.category import get_category_list,find_category
router = APIRouter(prefix="/api/category")

@router.post("/save", response_model=GenericResponse[str])
def save(data:CategoryCreate, db:Session=Depends(get_db)):
    #print(f"posted data:{data}")
    category = DbCategory(**data.model_dump())
    db.add(category)
    db.commit() 
    #db.refresh(category)
    return {"code":1, "data":"success"}

@router.get("/", response_model=GenericResponse[list[CategoryResponse]])
def index(db:Session=Depends(get_db)):
    print(f"categories with post count:{get_category_list(db)}")
    return {"code":1, "data":get_category_list(db)}

@router.get("/validcategories", response_model=GenericResponse[list[CategoryResponse]])
def index(db:Session=Depends(get_db)):
    return {"code":1, "data": get_category_list(db)}

@router.get("/{id}")
def show(id:int,db:Session=Depends(get_db)):
    category = find_category(id, db)
    if not category:
        #raise HTTPException(status_code=404)
        return {"code":0, "data":"分类不存在"}
    return {"code":1, "data":find_category(id, db)}
    

@router.get("/ttt", response_model=GenericResponse[list[CategoryResponse]])
def get_cate(db:Session=Depends(get_db)):
    return get_category_list(db)
    
    