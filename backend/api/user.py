
import json

from sparrow.sql import Unsafe

from util.multihandler import *
import model.user
from model import User
from .base import API

from session import Session
from util.mail import *

def auth(level):
    def decorator(method, _level=level):
        @wraps(method)
        async def wrapper(self, req, *args, **kwargs):
            try:
                session = await Session.get_session(req.get_argument("login_session"))
                if User.level_type.inv_options[session.user.level] < User.level_type.inv_options[_level]:
                    raise ClientError("no_access", "You are not permitted to perform this action")
                return await method(self, req, session, *args, **kwargs)
            except KeyError:
                raise ClientError("session_not_found", "The server could not find your session. Try logging in again.")

        return wrapper
    return decorator

new_user_mail = """
<html>
<body>
    <h1>Welcome to EESTEC LC Antwerp, {name}!</h1>
    <hr></hr>
    <p>We're happy to have you. To complete your registration, please <a href="{link}">click here</a>.</p>      
    <p>If the link doesn't work, you can copy-paste the following link in your browser: {link}</p>
</body>
</html>
"""


class UserAPI(API):
    model = User
    
    @post("/_user/login")
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
        s = await Session.new_session(d["email"], d["password"])
        req.write(json.dumps({"login_session": s.hash}))
    
    @post("/_user/logout")
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
    
    @post("/_user/register")
    @wrap_errors
    async def register(self, req):
        """
        Expects the arguments (as dictionary):
          - email
          - name
          - password

        Returns the User as JSON, or an error if the username already exists
        """
        d = json.loads(req.body)
        if (await User.get(User.email == Unsafe(d["email"])).count()) > 0:
            raise PlatformException("email_taken", "That email is already taken")
        else:
            u = User(email = d["email"],
                     password = (await model.user.encrypt(d["password"])),
                     name = d["name"],
                     level = "USER")  # Admins/Board members are made by DB admin
            await u.insert()
            
            # TODO links
            msg = Message("EESTEC LC Antwerp Registration Completion", 
                          new_user_mail.format(name=u.name, link="http://google.com"))
            await self.app.mailer.send(msg, to=u.email)
            
            req.write(u.to_json())
