from aiohttp.web_response import json_response, Response
from aiohttp.web_urldispatcher import View
from pydantic import ValidationError

from app.helpers.mixins import ConnectMixin
from app.helpers.models import DataAcquisitionScheme
from app.services.api.exceptions import CurrencyError


class ConvertView(View, ConnectMixin):
    """Представление перевода amount из валюты from в валюту to."""

    def get_params(self):
        return self.request.query

    def validate(self, *, params):
        return DataAcquisitionScheme(**params)

    async def get(self):
        currency_api = await self.currency_api
        params = self.get_params()

        try:
            validate_data = self.validate(params=params)
        except ValidationError as e:
            return Response(body=e.json())

        try:
            cur_from = await currency_api.get(validate_data.cur_from)
            cur_to = await currency_api.get(validate_data.cur_to)
        except CurrencyError as e:
            return Response(body=e.json(), status=400)
        result = dict(
            result=float((cur_from / cur_to) * validate_data.amount)
        )
        return json_response(result)
