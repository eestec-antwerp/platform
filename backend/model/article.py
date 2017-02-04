
from datetime import datetime

from sparrow import *

from .user import User

valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-")

class Article(Entity):
    slug = Property(str, constraint = lambda s: all(c in valid_chars for c in s))
    key = Key(slug)
    
    author = Reference(User)
    front = Property(bool)
    title = Property(str)
    summary = Property(str)
    content = Property(str)
    date = Property(int)
