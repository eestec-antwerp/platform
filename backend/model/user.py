
import passlib.hash
import secrets

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
    
    registration_code = Property(str, json=False, required=False)
    
    def reset_registration_code(self):
        self.registration_code = secrets.token_urlsafe(32)
    
    @property
    def registration_path(self):
        return f"/userdetails/{self.UID}?code={self.registration_code}"
    
