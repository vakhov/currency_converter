from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import View


class DatabaseView(View):
    """Представление заливает данные по валютам в хранилище."""

    async def post(self):
        return json_response(dict(status='OK'))
