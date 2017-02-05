
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
                session = await Session.get_session(req.json["session"]["hash"])
                if User.level_type.inv_options[session.user.level] < User.level_type.inv_options[_level]:
                    raise access_denied
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
    <p>We're happy to have you. To verify your email address, please <a href="{link}">click here</a>.</p>      
    <p>If the link doesn't work, you can copy-paste the following link in your browser: {link}</p>
</body>
</html>
"""

change_user_mail = """
<html>
<body>
    <h1>You requested a change of email address!</h1>
    <hr></hr>
    <p>To verify your new email address, please <a href="{link}">click here</a>.</p>      
    <p>If the link doesn't work, you can copy-paste the following link in your browser: {link}</p>
</body>
</html>
"""

class UserAPI(API):
    model = User
    
    _get = post("/_user/get")(API.get)
    
    @post("/_user/check_session")
    @wrap_errors
    @auth("USER")
    async def check_session(self, req, session):
        req.write("{}")
    
    @post("/_user/login")
    @wrap_errors
    async def login(self, req):
        """
        Expects the arguments (as dictionary)
          - username
          - password

        Returns (in case of succesful login):
          - session: session info

        Might throw an error if the password is wrong.
        """
        s = await Session.new_session(req.json["email"], req.json["password"])
        req.write(json.dumps({"session": s.to_json()}))

    
    @post("/_user/logout")
    @auth("USER")
    async def logout(self, req, session):
        """
        Expects the arguments:
        - session

        Returns (in case of succesful logout): an empty JSON dictionary.

        Might throw an error if the session is not found.
        """
        await Session.del_session(req.json["session"]["hash"])
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
        users = await User.get(User.email == Unsafe(req.json["email"])).all()
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
            u = User(email = req.json["email"],
                     password = (await model.user.encrypt(req.json["password"])),
                     name = req.json["name"],
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
        UID = req.json["UID"]
        registration_code = req.json["registration_code"]
        u = await User.find_by_key(UID)
        if (u.registration_code != "" and u.registration_code == registration_code):
            u.registration_code = ""
            await u.update()
            s = Session.new_free_session(u)
            req.write({"success": {"short": "registration_complete",
                                   "long": "The registration has completed"},
                       "session": s.to_json()})
        else:
            self.app.logger.warning(f"Wrong registration code provided: {registration_code} should be {u.registration_code}")
            req.write({"error": {"short": "wrong_code",
                                 "long": "The provided registration code is wrong. Perhaps try registering again?"}})
    
    
    @post("/_user/change_account")
    @wrap_errors
    @auth("USER")
    async def change_account(self, req, session):
        changes = {}
        u = session.user
        if (await model.user.verify(req.json["old_password"], u.password)):
            if req.json["email"] != u.email and len(req.json["email"]) > 2:
                u.email = req.json["email"]
                u.reset_registration_code()
                await self.send_registration_mail(u, text=change_user_mail)
                changes["email"] = {"status": "success", "message": "Email address changed, please check your email for a new confirmation message"}
            
            if req.json["name"] != u.name and len(req.json["name"]) > 1:
                u.name = req.json["name"]
                changes["name"] = {"status": "success", "message": "Name changed"}
            
            if len(req.json["new_password"]) > 3:
                hashed_new_password = await model.user.encrypt(req.json["new_password"])
                if hashed_new_password != u.password:
                    u.password = hashed_new_password
                    changes["password"] = {"status": "success", "message": "Password changed"}
            
            await u.update()
            
            req.write({"changes": changes})
        else:
            raise wrong_password
        
    
    async def send_registration_mail(self, u, text=new_user_mail):
        link = self.app.config["base_url"] + u.registration_path
        msg = Message("EESTEC LC Antwerp Email Verification",
                        text.format(name=u.name, link=link))
        await (await self.app.mailer).send(msg, to=u.email)

