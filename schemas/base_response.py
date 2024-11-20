from typing import TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel

M = TypeVar("M", bound=BaseModel)

class GenericResponse(GenericModel, Generic[M]):
    code:int
    data:M