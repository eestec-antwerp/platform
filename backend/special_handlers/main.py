import tornado

from app import localdir

# Handlers are instantiated for every request!
def create_MainHandler(app):
    if not app.debug:
        f = open(localdir("../frontend/index.html"), "r")
        content = str(f.read())

    class MainHandler(tornado.web.RequestHandler):
        def get(self, *args):
            if app.debug:
                f = open(localdir("../frontend/index.html"), "r")
                _content = str(f.read())
                self.write(_content)
            else:
                self.write(content)

        post = get

    return MainHandler
