import aioredis
from aiohttp.web import run_app
from aiohttp.web_app import Application

from app.helpers.klasses import Environ
from app.routes import routes
from app.services.api.converter import ConverterApi


async def connect_to_redis(url: str):
    redis = await aioredis.create_redis_pool(url)
    return redis


class RedisConnetion:

    def __init__(self, app: Application) -> None:
        self._app = app

    async def on_startup(self):
        setattr(self._app, 'client', ConverterApi())

    async def cleanup(self):
        pass


env = Environ()

app = Application()
app.add_routes(routes=routes)

if __name__ == '__main__':
    run_app(app, host=env['SERVICE_HOST'], port=env['SERVICE_PORT'])
