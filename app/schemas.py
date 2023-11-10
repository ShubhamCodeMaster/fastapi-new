from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class Postcreate(PostBase):
    pass
class Userout(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    owner:Userout
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str
    # class Config:
    #     orm_mode = True
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
    





