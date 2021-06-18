from aiohttp.web import run_app
from aiohttp.web_app import Application

from app.helpers.klasses import Environ
from app.routes import routes

env = Environ()

app = Application()
app.add_routes(routes=routes)

if __name__ == '__main__':
    run_app(app, host=env['SERVICE_HOST'], port=env['SERVICE_PORT'])
