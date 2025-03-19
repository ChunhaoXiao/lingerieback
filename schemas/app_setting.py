from pydantic import computed_field, BaseModel
from typing import Any
import json
class SettingResponse(BaseModel):
    id:int
    setting_name:str | None=None
    setting_value:str | None=None
    type:str | None=None
    options:str | None=None
    description:str | None=None


    @computed_field
    @property
    def setting_options(self)->Any:
        if self.options:
            return json.loads(self.options)
        return []
        
       