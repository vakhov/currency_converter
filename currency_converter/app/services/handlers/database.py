
import json

from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import View

from app.helpers.mixins import RedisConnectMixin


class DatabaseView(View, RedisConnectMixin):
    """Представление принимает данные по валютам и сохраняет их в хранилище."""

    def is_merge(self) -> bool:
        return bool(int(self.request.query.get('merge', '1')))

    async def post(self):
        currency_api = await self.currency_api
        body: bytes = await self.request.content.read()
        data = json.loads(body)
        await currency_api.update(data=data, merge=self.is_merge())
        return json_response(dict(result='OK'))
