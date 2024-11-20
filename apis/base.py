from fastapi import APIRouter
from apis.v1 import route_charge, route_post, route_category,route_login,route_user,route_like,route_collection,route_swiper,route_notice,route_my
from apis.admin import route_category as admin_category
from apis.admin import route_post as admin_post 
from apis.admin import route_notice as admin_notice
from apis.admin import route_user as admin_user
from apis.admin import route_card as admin_card
from apis.admin import route_statistic
from apis.admin import route_upload as admin_upload

api_router = APIRouter()

api_router.include_router(admin_upload.router)
api_router.include_router(route_post.router)
api_router.include_router(route_category.router)
api_router.include_router(route_login.router)
api_router.include_router(route_user.router)
api_router.include_router(route_like.router)
api_router.include_router(route_collection.router)
api_router.include_router(route_notice.router)
api_router.include_router(route_my.router)
api_router.include_router(route_charge.router)
#api_router.include_router(route_card.router)


api_router.include_router(admin_category.router)
api_router.include_router(admin_post.router)
api_router.include_router(route_swiper.router)
api_router.include_router(admin_notice.router)
api_router.include_router(admin_user.router)
api_router.include_router(admin_card.router)
api_router.include_router(route_statistic.router)
