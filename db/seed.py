import datetime
from sqlalchemy import func, select
from db.models.media import Media
from db.repository.category import get_valid_categories
from sqlalchemy.orm import properties, session, Session
from fastapi import Depends
from db.session import engine
from db.models.post import Post
from db.models.category import Category
from db.models.user import User
from db.models.vip import Vip
import uuid
from faker import Factory
import os
from urllib.parse import urlencode
import requests
from random import randint
import time



def seed_data():
    session = Session(engine)
    cates = get_valid_categories(session)
    print(f"cates in database----> {cates}")
    if len(cates) == 0:
        for i in range(1,4):
          print(f"i is:{i}")
          cate = Category(name=f"分类{i}", icon="b28ea314-eb9d-444f-ae45-fd533db1b361.webp")
          session.add(cate)
          session.commit()
    
        cates = get_valid_categories(session)
        
    index = 1
    print(f"cates is######################################{cates}")
    for category in cates:
        print(f"category==================================>{category.Category}")
        
        if category.cnt < 10:
            print(f"posts length=============================>{category.cnt}")
            for i in range(1,40):
                index = index+1
            # print(f"{category}----------------------->{i}")
                is_vip = 1 if i % 2 ==1 else 0 
                pictures = get_unsplash_images(index)
                medias = []
                for pic in pictures:
                    medias.append(Media(url=pic))
                post = Post(
                    title=f"{category.Category.name}+-post title{i}",
                    author="zslisi",
                    is_vip=is_vip,
                    description="this is a post",
                    category=category.Category,
                    
                    files = medias
                    )
                print(post)
                session.add(post) 
                session.commit()
                
    
    user_cnt = session.scalars(select(func.count(User.id)).select_from(User)).first()
    print(user_cnt)
    if user_cnt < 200:
        fake = Factory.create()
        for i in range(1,200):
            open_id = str(uuid.uuid4())
            print(f"openid:{open_id}")
            user = User(open_id=open_id, name=f"{fake.name()}{i}")
            session.add(user)
            session.commit()
            #user = session.refresh(user)
        #     if(i % 3 == 0):
        #         vip = Vip(user=user,open_id=user.open_id, expire_date = datetime.now() + datetime.timedelta(days=31))
        #         session.add(vip)
        #         session.commit()
        #    session.commit()
      

def download_image(num_count:int):
    
        """
        num_count is the number of images to be downloaded
        """
        print(f"=====>{os.getcwd()}")
        url = generate_image_url()
        images = []
        file_name = f"{uuid.uuid4()}.jpg"
        for i in range(0, num_count, 1):
            image_path = f"{os.getcwd()}/static/{file_name}"
            response = requests.get(url)
            with open(image_path, mode='wb') as fp:
                fp.write(response.content)    
            images.append(file_name)  
        return images

def generate_image_url():
        url = f"https://picsum.photos/400/300.jpg"
        data = {}
        data['grayscale'] = None
        data['blur'] = None
        url = f"{url}?{urlencode(data)}"
        return url
    
def get_unsplash_images(page):
    url = f"https://api.unsplash.com/photos?client_id=q3WNqpM9V4hlxfFcriQEFO6L-C8ohzFs8XtY-wHUOwc&per_page=5&page={int(page)}"
    res = requests.get(url).json()
    pic_arr = []
    for item in res:
        pic_arr.append(item['urls']['regular'])
    
    return pic_arr
    #print(f"unsplash response:{res}")