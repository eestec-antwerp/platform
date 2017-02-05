
import secrets

from sparrow import Unsafe

from util.exceptions import *
from model.user import User, verify

class Session:
    # TODO automatic expiration of sessions? Map could get rather big...
    sessions = {}

    def __init__(self, _hash, user):
        self.hash = _hash
        self.user = user

    @classmethod
    async def get_session(cls, _hash):
        return cls.sessions[_hash]

    @classmethod
    async def del_session(cls, _hash):
        del cls.sessions[_hash]

    @classmethod
    async def new_session(cls, email, password):
        u = await User.get(User.email == Unsafe(email)).single()

        if (await verify(password, u.password)):
            # Password is right
            return cls.new_free_session(u)
        else:
            raise wrong_password
    
    @classmethod
    def new_free_session(cls, user):
        login_session = secrets.token_urlsafe(32)
        s = Session(login_session, user)
        cls.sessions[login_session] = s
        return s
    
    def assert_same_UID(self, UID):
        if self.user.UID != UID:
            raise access_denied
    
    def to_json(self):
        return {"UID": self.user.UID, "hash": self.hash}
    
