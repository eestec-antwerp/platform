
import json
import sparrow
from functools import wraps

class PlatformException(Exception):
    def __init__(self, short, long):
        self.short = short
        self.long = long
    
    def json_repr(self):
        return {"short": self.short, "long": self.long}
    
    def __str__(self):
        return json.dumps(self.json_repr())
        

def wrap_errors(method):
    @wraps(method)
    async def wrapper(self, req, *args, **kwargs):
        try:
            return await method(self, req, *args, **kwargs)
        except PlatformException as e:
            self.app.logger.error("PlatformException: " + str(e))
            req.write(json.dumps({"error": e.json_repr()}))
        except sparrow.NotSingle as e:
            self.app.logger.error("Sparrow Error: " + str(e))
            req.write(json.dumps({"error": {"short": "not_single", "long": str(e)}}))
        except sparrow.Error as e:
            self.app.logger.error("Sparrow Error: " + str(e))
            req.write(json.dumps({"error": {"short": "sparrow_error", "long": str(e)}}))
    return wrapper
