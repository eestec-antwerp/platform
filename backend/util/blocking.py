
from concurrent.futures import ThreadPoolExecutor

from tornado.platform.asyncio import to_tornado_future
from functools import wraps

class Executor:    
    def __init__(self, size=32):
        self.pool = ThreadPoolExecutor(size)

    @property
    def blocking(executor):
        "Wraps the method in an async method."
        def decorator(method, _executor=executor):
            @wraps(method)
            async def wrapper(*args, **kwargs):
                fut = _executor.pool.submit(method, *args, **kwargs)
                return await to_tornado_future(fut)
            return wrapper
        return decorator

executor = Executor()
