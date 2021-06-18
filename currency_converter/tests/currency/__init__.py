from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web_app import Application

from app.routes import routes


class BaseTestHandlers(AioHTTPTestCase):
    async def get_application(self):
        app = Application()
        app.add_routes(routes=routes)
        return app
