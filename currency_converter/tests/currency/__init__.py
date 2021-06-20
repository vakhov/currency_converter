import json
from unittest.mock import MagicMock

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web_app import Application

from app.helpers.functionals import lazy
from app.routes import routes


class BaseTestHandlers(AioHTTPTestCase):

    async def tearDownAsync(self) -> None:
        return await super().tearDownAsync()

    async def get_application(self):
        app = Application()
        app.add_routes(routes=routes)
        return app

    def assertStatusCode(self, res, status_code: int = 200):
        def get_error_message() -> str:
            try:
                message = json.dumps(res.json(), indent=4, sort_keys=True, ensure_ascii=False)
            except (ValueError, TypeError):
                message = res.content.decode()
            return f'Invalid status code. Expected: {status_code}, Actual: {res.status_code}\n' + str(message)

        lazy_get_error_message = lazy(get_error_message)
        self.assertEqual(res.status, status_code, lazy_get_error_message())


class RedisMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)
