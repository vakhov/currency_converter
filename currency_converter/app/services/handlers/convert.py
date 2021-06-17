from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import View


class ConvertView(View):
    """Представление перевода amount из валюты from в валюту to."""

    async def get(self):
        return json_response(dict(status='OK'))
