
import json

from util.multihandler import *
from model import User
from .base import API

def auth(level):
    def decorator(method, _level=level):
        @wraps(method)
        async def wrapper(self, req, *args, **kwargs):
            try:
                session = await Session.get_session(req.get_argument("login_session"))
                #if User.level_type.inv_options[session.user.level] < User.level_type.inv_options[_level]:
                    #raise ClientError("no_access", "You are not permitted to perform this action")
                return await method(self, req, session, *args, **kwargs)
            except KeyError:
                raise ClientError("session_not_found", "The server could not find your session. Try logging in again.")

        return wrapper
    return decorator


class UserAPI(API):
    model = User
    
    @post("/user/login")
    async def login(self, req):
        """
        Expects the arguments (as dictionary)
          - username
          - password

        Returns (in case of succesful login):
          - login_session: the hash for the session

        Might throw an error if the password is wrong.
        """
        d = json.loads(req.body)
        s = await Session.new_session(d["username"], d["password"])
        req.write(json.dumps({"login_session": s.hash}))
    
    @post("/user/logout")
    @auth("USER")
    async def logout(self, req):
        """
        Expects the arguments:
        - login_session

        Returns (in case of succesful logout): an empty JSON dictionary.

        Might throw an error if the session is not found.
        """
        await Session.del_session(session.hash)
        req.write("{}")
    
    @post("/user/signup")
    @wrap_errors
    async def signup(self, req):
        """
        Expects the arguments (as dictionary):
          - username
          - password

        Returns the User as JSON, or an error if the username already exists
        """
        d = json.loads(req.body)
        if (await User.get(User.username == Unsafe(d["username"])).count()) > 0:
            raise PlatformException("username_taken", "That username is already taken")
        else:
            u = User(username = d["username"],
                     password = (await model.user.encrypt(d["password"])),
                     level = "USER")  # Admins are made by DB admin
            await u.insert()
            req.write(u.to_json())
