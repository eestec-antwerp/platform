

def lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop

def async_lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    async def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, await fn(self))
        return getattr(self, attr_name)
    return _lazyprop

