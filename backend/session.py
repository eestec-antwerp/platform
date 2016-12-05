
import random
import hashlib

from sparrow import Unsafe

from util.exceptions import *
from model.user import *

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

        if (await model.user.verify(password, u.password)):
            # Password is right
            # TODO Code that survived since Overwatch, but still not sure
            # whether this is actually safe :)
            login_session = hashlib.md5(bytes(str(random.random())[2:] + "WowAnotherSaltFreelyAvailableOnGithub", "utf8")).hexdigest()
            s = Session(login_session, u)
            cls.sessions[login_session] = s
            return s
        else:
            raise PlatformException("wrong_password", "Wrong password")

