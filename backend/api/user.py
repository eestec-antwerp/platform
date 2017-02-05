
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
                session = await Session.get_session(req.get_argument("login"))
                if User.level_type.inv_options[session.user.level] < User.level_type.inv_options[_level]:
                    raise PlatformException("no_access", "You are not permitted to perform this action")
                return await method(self, req, session, *args, **kwargs)
            except KeyError:
                raise PlatformException("session_not_found", "The server could not find your session. Try logging in again.")

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
    @wrap_errors
    async def login(self, req):
        """
        Expects the arguments (as dictionary)
          - username
          - password

        Returns (in case of succesful login):
          - login: login info

        Might throw an error if the password is wrong.
        """
        d = json.loads(req.body)
        s = await Session.new_session(d["email"], d["password"])
        req.write(json.dumps({"login": s.to_json()}))
    
    
    @post("/_user/logout")
    #@auth("USER")
    async def logout(self, req):
        """
        Expects the arguments:
        - login

        Returns (in case of succesful logout): an empty JSON dictionary.

        Might throw an error if the session is not found.
        """
        d = json.loads(req.body)
        print(d)
        await Session.del_session(d["login"]["hash"])
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
        users = await User.get(User.email == Unsafe(d["email"])).all()
        if (len(users)) == 1:
            u = users[0]
            if u.registration_code == "":
                raise PlatformException("email_taken", "That email is already taken")
            else:
                u.reset_registration_code()
                await u.update()
                await self.send_registration_mail(u)
                raise PlatformException("email_resent", "We've sent another registration mail")
        else:
            u = User(email = d["email"],
                     password = (await model.user.encrypt(d["password"])),
                     name = d["name"],
                     level = "USER")  # Admins/Board members are made by DB admin
            u.reset_registration_code()
            await u.insert()
            await self.send_registration_mail(u)
            req.write(u.to_json())
    
    
    @post("/_user/complete_registration")
    @wrap_errors
    async def complete_registration(self, req):
        """
        Expects the arguments (as dictionary):
          - UID
          - registration_code
        
        Returns success or error message...
        """
        d = json.loads(req.body)
        UID = d["UID"]
        registration_code = d["registration_code"]
        u = await User.find_by_key(UID)
        if (u.registration_code != "" and u.registration_code == registration_code):
            u.registration_code = ""
            await u.update()
            s = Session.new_free_session(u)
            req.write({"success": {"short": "registration_complete",
                                   "long": "The registration has completed"},
                       "login": s.to_json()})
        else:
            self.app.logger.warning(f"Wrong registration code provided: {registration_code} should be {u.registration_code}")
            req.write({"error": {"short": "wrong_code",
                                 "long": "The provided registration code is wrong. Perhaps try registering again?"}})
    
    
    async def send_registration_mail(self, u):
        link = self.app.config["base_url"] + u.registration_path
        msg = Message("EESTEC LC Antwerp Registration Completion", 
                        new_user_mail.format(name=u.name, link=link))
        await self.app.mailer.send(msg, to=u.email)

