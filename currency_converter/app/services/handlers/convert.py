from aiohttp.web_response import json_response, Response
from aiohttp.web_urldispatcher import View
from pydantic import ValidationError

from app.helpers.validate import DataAcquisitionScheme


class ConvertView(View):
    """Представление перевода amount из валюты from в валюту to."""

    def get_params(self):
        return self.request.query

    def validate(self, *, params):
        return DataAcquisitionScheme(**params)

    async def get(self):
        params = self.get_params()
        try:
            validate_data = self.validate(params=params)
            return json_response(validate_data.json(by_alias=True))
        except ValidationError as e:
            return Response(body=e.json())
