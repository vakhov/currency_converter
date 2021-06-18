from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import View


class DatabaseView(View):
    """Представление принимает данные по валютам и сохраняет их в хранилище."""

    async def post(self):
        return json_response(dict(status='OK'))
