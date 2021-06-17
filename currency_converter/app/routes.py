from aiohttp.web_routedef import view

from app.services.handlers.convert import ConvertView
from app.services.handlers.database import DatabaseView

routes = (
    view(path='/convert', handler=ConvertView),
    view(path='/database', handler=DatabaseView)
)
