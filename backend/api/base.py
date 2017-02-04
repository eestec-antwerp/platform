
import json

from util.multihandler import *

class API(MultiHandler):
    
    # static methods, so they can be reused later (unbound)
    
    @staticmethod
    async def add(self, req):
        d = json.loads(req.body)
        obj = self.model(json_dict=d["what"])
        await obj.insert()
        req.write(json.dumps({"what": obj.json_repr()}))
    
    add_cls = minihandler([], add)
    
    @staticmethod
    async def get(self, req, key):
        obj = await self.model.find_by_key(self.model.key.single_prop.type.python_type(key))
        req.write(json.dumps({"what": obj.json_repr()}))

    get_cls = minihandler([], get)
