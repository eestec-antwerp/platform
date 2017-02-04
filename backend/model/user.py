
import passlib.hash

from sparrow import *
from util.blocking import executor

@executor.blocking
def encrypt(password) -> str:
    return passlib.hash.bcrypt.encrypt(password, rounds=10)

@executor.blocking
def verify(password, hashed) -> bool:
    return passlib.hash.bcrypt.verify(password, hashed)

class UserDetails(Entity):
    key = UDID = KeyProperty()
    interests = Property(List(str))
    location = Property(str, required=False)
    
    
class User(Entity):
    level_type = Enum("USER", "BOARD", "ADMIN")
    
    key = UID = KeyProperty()
    email = Property(str, sql_extra="UNIQUE")
    password = Property(str, json=False)
    name = Property(str)
    level = Property(level_type)

    
