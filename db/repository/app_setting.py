from db.models.app_setting import AppSetting
from db.session import session
from sqlalchemy import select,update
from db.redis import set_config,get_config
from core.app_setting import settings
from sqlalchemy.orm import Session

# def get_all_setting():
#     pass
#   #return session.scalars(select(AppSetting)).all()

def set_app_config():
    
    for setting_key, setting in settings.items():
        row = session.scalars(select(AppSetting).where(AppSetting.setting_name == setting_key)).first()
        if not row:
            data = AppSetting(
                setting_name=setting_key, 
                setting_value=setting["value"],
                description=setting['description'],
                type=setting['type']
                )
            session.add(data)
            session.commit()
        else:
            row.setting_name=setting_key
            #row.setting_value = setting["value"]
            row.description = setting['description']
            row.type = setting['type']
            session.commit()
            
            
    configs = session.scalars(select(AppSetting)).all()
    
    for item in configs:
        set_config(item.setting_name,item.setting_value)
        
def update_setting(data, db:Session):
    for k, v in data.items():
      db.execute(update(AppSetting).where(AppSetting.setting_name == k).values(setting_value = v))
      db.commit()
    fill_setting_to_redis(db)
      
def fill_setting_to_redis(db:Session):
    configs = db.scalars(select(AppSetting)).all()
    for item in configs:
        print(f"##############################################{item.setting_value}")
        set_config(item.setting_name,item.setting_value)
        
def get_app_setting(key):
    return get_config(key)
    
      
    
    
    