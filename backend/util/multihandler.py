
import copy
import json

import tornado.web

from .exceptions import *

# no routes!
def minihandler(methods, _func):
    class Handler(tornado.web.RequestHandler):
        func = _func
        routes = []
        
        def __init__(self, *args, **kwargs):
            self._actualself = kwargs.pop("_actualself")
            super(Handler, self).__init__(*args, **kwargs)
        
        def _handle(self, *args, **kwargs):
            #print("_handle got kwargs: ", kwargs, "args:", args)
            try:
                return _func(self._actualself, self, *args, **kwargs)
            except PlatformException as e:
                import traceback
                traceback.print_exc()
                self.write(str(e))
                self.set_status(500, reason=e.short)
        
        def __getattr__(self, attr):
            # I'm done with this shit
            return getattr(self.request, attr)
        
    for m in methods:
        setattr(Handler, m, Handler._handle)
    return Handler

def route(handler, *routes):
    handler = copy.copy(handler)
    handler.routes = routes
    return handler


def make_make_handler(_method):
    def make_handler(*routes):
        def decorator(func, _routes=routes, _method=_method):
            h = minihandler([_method], wrap_errors(func))  # default wraps errors
            h = route(h, *_routes)
            return h
        return decorator
    return make_handler

# easy shortcuts
post = make_make_handler("post")
get = make_make_handler("get")

class MultiHandler:
    def __init__(self, app):
        self.app = app
    
    def get_routes(self):
        if hasattr(self, "_routes"):
            return self._routes
        
        routes = []
        for i in dir(self):
            obj = getattr(self, i)
            try:
                if issubclass(obj, tornado.web.RequestHandler):
                    for r in obj.routes:
                        routes.append((r.replace("@", "([^/]+)"), obj, {"_actualself": self}))
            except TypeError:
                pass
        
        self._routes = routes
        return routes
    
"""
Example:

class Bla(MultiHandler):
    @post("/posthere/(@")
    async def posthere(self: Bla, req: tornado.web.RequestHandler, url_arg):
        req.write(url_arg.upper())

"""
