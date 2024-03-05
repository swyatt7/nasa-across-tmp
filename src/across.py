from .api.base.app import api_app
from .web.app import web_app

from .web import routes  # noqa F401
# from .api.base import app  # noqa F401

from fastapi.middleware.wsgi import WSGIMiddleware

api_app.mount("/", WSGIMiddleware(web_app))
    
