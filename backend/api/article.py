
import json

from util.multihandler import *
from model.article import Article
from .base import API
from .user import auth

class ArticleAPI(API):
    model = Article
    
    # TODO add auth back!
    #_add = post("/_article/add")(auth("BOARD")(API.add))
    _add = post("/_article/add")(API.add)
    
    _get = get("/_article/get/@")(API.get)

