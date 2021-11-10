from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

    class Config:
        expire: float = 7.5


external_data = {
    'id': '123', 
    'signup_ts': '2017-06-01 12:22', 
    'friends': [1, '2', b'3']
}
user = User(**external_data)

print(user)
print(user.__fields__)
print(user.__config__)
print(user.__config__.expire)

# ModelField has the possibility to define a default type that is 
# mutable ie. a list; that will be created per instance
class A(object):

    def __init__(self, lst: List[int] = [1,2,3]) -> None:
        super().__init__()
        self.lst = lst

a = A()
print(a.lst)
a.lst[0] = 5

b = A()
print(b.lst)  # !!!

import pdb; pdb.set_trace()
