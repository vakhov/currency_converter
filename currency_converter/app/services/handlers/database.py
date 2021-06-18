import json

from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import View

from app.helpers.mixins import ConnectMixin


class DatabaseView(View, ConnectMixin):
    """Представление принимает данные по валютам и сохраняет их в хранилище."""

    def get_params(self):
        return self.request.query

    async def post(self):
        currency_api = await self.currency_api
        body: bytes = await self.request.content.read()
        data = json.loads(body)
        await currency_api.update(data=data)
        return json_response(dict(result='OK'))
