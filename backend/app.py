
import sys
import os

def localdir(location):
    return os.path.join(os.path.dirname(__file__), location)

# Standard library
import logging
import types
from functools import wraps

# Tornado
import tornado.ioloop
import tornado.log
import tornado.web

# Sparrow: sparrow.readthedocs.org
import sparrow

# Own code
import api
import model
import special_handlers
from util.mail import Mailer

# Small utilities
# ===============

default_config = {
    "debug": True,
    "tornado_app_settings": {},
    "port": 8080,
    "database": {
        "dbname": "eestec",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": 5432,
    },
    "mails": {
        "from_address": "admin@eestec.be",
        "username": "admin@eestec.be",
        "password": "yeah right not posting that one to github"
    },
    "base_url": "http://localhost:8080"
}

def parse_config(conf, default):
    d = {}
    for (k, v) in default.items():
        if k in conf:
            if isinstance(v, dict):
                d[k] = parse_config(conf[k], v)
            else:
                d[k] = conf[k]
        else:
            d[k] = v
    return d

def get_config(filename="config.py"):
    if os.path.isfile(filename):
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            glob = {}
            loc = {}
            exec(code, glob, loc)
            return parse_config(loc["config"], default_config)
    else:
        print("WARNING: Using default config. A `config.py` file can change this. (See app.py for template).")
        return default_config


def simple_async_catch(method):
    @wraps(method)
    async def wrapper(self):
        try:
            await method(self)
        except sparrow.Error as e:
            self.logger.error(str(e))
    return wrapper

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


# Central class
# =============

ioloop = tornado.ioloop.IOLoop.current()

class EestecPlatform:
    def __init__(self, config, ioloop=ioloop):
        self.config = config
        self.debug = config["debug"]
        self.ioloop = ioloop
        
        self.logger = logging.getLogger("EESTEC")
        self.logger.setLevel(logging.DEBUG if config["debug"] else logging.INFO)
        self.logger.debug("EESTEC Platform webserver starting")
        
        self.mailer = Mailer(**config["mails"])
        self.logger.info(f"Sending mail from {config['mails']['from_address']}")

        classes = [model.User, model.Article]
        self.model = sparrow.SparrowModel(ioloop, db_args=config["database"], debug=config["debug"], classes=classes, set_global_db=True)
        
        StaticClass = NoCacheStaticFileHandler if self.debug else tornado.web.StaticFileHandler
        
        tornado_app_settings = config["tornado_app_settings"]
        
        self.handlers = [mh_cls(self) for mh_cls in api.APIs]
        routes = sum((mh.get_routes() for mh in self.handlers), [])
        
        routes += [
            (r'/static/(.*)', StaticClass, {'path': localdir("../frontend/static")}),
            (r'/build/(.*)', StaticClass, {'path': localdir("../frontend/build")}),
            (r'/(.*)', special_handlers.create_MainHandler(self)),
        ]
        
        self.app = tornado.web.Application(routes, **tornado_app_settings, debug=self.debug)

    def run(self):
        self.ioloop.run_sync(self.mailer.connect)
        self.app.listen(self.config['port'])
        self.ioloop.start()
    
    @simple_async_catch
    async def install(self):
        self.logger.info("Installing...")
        await self.model.install()
    
    @simple_async_catch
    async def uninstall(self):
        self.logger.info("Uninstalling...")
        await self.model.uninstall()
    
    @simple_async_catch
    async def reinstall(self):
        await self.uninstall()
        await self.install()

# Main
# ====

def unknown_action(_logger):
    def f(logger=_logger):
        logger.info("I don't know that action.")
    return f

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    config = get_config()
    srv = EestecPlatform(config)
    action = "run" if len(sys.argv) == 1 else sys.argv[1]
    try:
        # Some magic to allow both synchronous and asynchronous usage
        f = getattr(srv, action, unknown_action(srv.logger))()
        if isinstance(f, types.CoroutineType):
            async def await_f():
                await f
            ioloop.run_sync(await_f)
    except KeyboardInterrupt:
        ioloop.stop()
        srv.logger.info("Stopping because of KeyboardInterrupt")
