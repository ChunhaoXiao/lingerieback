from fastapi import Depends, APIRouter
from db.session import get_db
from schemas.category import Category,CategoryCreate,CategoryResponse
from sqlalchemy.orm import Session;
from db.models.category import Category as DbCategory
from db.models.user import User
from apis.v1.route_login import get_admin_user
from schemas.base_response import GenericResponse
from db.repository.category import get_category_list,get_valid_categories
from sqlalchemy import select

router = APIRouter(prefix="/api/admin/category", dependencies=[Depends(get_admin_user)])

@router.get("/", response_model=GenericResponse[list[CategoryResponse]])
def index(db:Session=Depends(get_db)):
    print(f"categories with post count:{get_category_list(db)}")
    return {"code":1, "data":get_category_list(db,is_all=1)}

@router.get("/{id}", response_model=GenericResponse[Category])
def find(id:int, db:Session=Depends(get_db)):
    stmt = select(DbCategory).where(DbCategory.id == id)
    res = db.scalars(stmt).first()
    return {"code":1, "data":res} 

@router.put("/{id}")
def update(id:int, params:CategoryCreate, db:Session= Depends(get_db)):
    category = db.scalars(select(DbCategory).where(DbCategory.id == id)).first()
    category.name = params.name
    category.enabled = params.enabled
    category.icon = params.icon
    db.commit()
    return {"code":1, "data":"success"}

@router.delete("/{id}")
def remove(id:int, db:Session= Depends(get_db)):
    category = db.scalars(select(DbCategory).where(DbCategory.id == id)).first()
    #conlumn_property
    if category.post_count > 0:
        return {"code":2,"data":"此分类下有数据，不能直接删除"}
    db.delete(category)
    db.commit()
    return {
        "code":1,
        "data":"sucess"
    }
    
