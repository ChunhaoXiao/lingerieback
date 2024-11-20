from sqlalchemy.orm import selectinload, Session
from sqlalchemy import select, select, select, Select
from db.models.category import Category
from db.models.post import Post
from sqlalchemy import func
from db.session import session



def get_category_list(db:Session):
    stmt = select(Category,func.count(Post.id).label("cnt")).join_from(Category,Post,isouter=True).group_by(Category.id)
    res = db.execute(stmt).all()
    for item in res:
        print(item.Category)
        print(item.cnt)
    return res
    # results = []
    # for a, b in res:
    #     results.append({"data":a, "count":b})
    # return results

    #return db.scalars(Select(Category).options(selectinload(func.count(Category.posts)))).all()

def get_valid_categories(db:Session):
    stmt = select(Category,func.count(Post.id).label("cnt")).join_from(Category,Post,isouter=True).where(Category.enabled==1).group_by(Category.id)
    res = db.execute(stmt).all()
    return res
#     #pass
# def get_category_list_val(db:Session):
#     stmt = select(Category,func.count(Post.id).label("cnt")).join_from(Category,Post,isouter=True).group_by(Category.id)
#     res = db.execute(stmt).all()
#     for item in res:
#         print(item.Category)
#         print(item.cnt)
#     return res
