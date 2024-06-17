from datetime import datetime
from typing import List, Union

from pydantic import BaseModel


class Podcast(BaseModel):
    title: Union[str, None] = None
    type_: Union[str, None] = None
    xmlUrl: Union[str, None] = None
    htmlUrl: Union[str, None] = None


class OPMLFile(BaseModel):
    hash: Union[str, None] = None
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    podcasts_qty: int = 0
    podcasts: List[Podcast] = []
   

class User(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None
    email: Union[str, None] = None
    api_key: Union[str, None] = None
    opmlfile: OPMLFile
    

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str

class CreateUserResponse(BaseModel):
    username: str
    api_key: str
