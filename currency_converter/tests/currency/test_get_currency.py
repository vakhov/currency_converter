from typing import Dict
from unittest import mock
from unittest.mock import MagicMock

from aiohttp.test_utils import unittest_run_loop

from tests.currency import BaseTestHandlers, RedisMock


class TestConvertHandler(BaseTestHandlers):
    """Тесты ручки получения валют /convert"""
    database_path = '/database?merge={merge_state}'
    convert_path = '/convert?from={cur_from}&to={cur_to}&amount={amount}'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.data_currency: Dict[str, float] = dict(
            USD=72.5048,
            EUR=86.7012,
            JPY=65.5500
        )

    @unittest_run_loop
    @mock.patch('app.helpers.mixins.RedisConnectMixin.connect', new_callable=RedisMock)
    async def test_non_valid_http_method(self, redis_connect: MagicMock):
        """Тест: не валидный http метод"""
        convert_path = self.convert_path.format(
            cur_from='RUB',
            cur_to='USD',
            amount=42
        )
        resp = await self.client.post(path=convert_path)
        resp.read()

        self.assertStatusCode(resp, 405)
        self.assertEqual(0, redis_connect.call_count)

    @unittest_run_loop
    async def test_convert_rub_to_usd(self):
        """Тест: конвертация валют"""
        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_currency)
        resp.read()

        convert_path = self.convert_path.format(
            cur_from='RUB',
            cur_to='USD',
            amount=42
        )
        resp = await self.client.get(path=convert_path)
        currencies = await resp.json()
        self.assertStatusCode(resp)
        self.assertDictEqual(currencies, {'result': 0.5792719930266685})

    @unittest_run_loop
    async def test_convert_rub_to_usd_camel_case_currency_name(self):
        """Тест: конвертация валют с camel case currency name"""
        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_currency)
        resp.read()

        convert_path = self.convert_path.format(
            cur_from='rUb',
            cur_to='UsD',
            amount=42
        )
        resp = await self.client.get(path=convert_path)
        currencies = await resp.json()
        self.assertStatusCode(resp)
        self.assertDictEqual(currencies, {'result': 0.5792719930266685})

    @unittest_run_loop
    async def test_convert_invalid_currency(self):
        """Тест: конвертация валют с невалидным значением валюты"""
        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_currency)
        resp.read()

        convert_path = self.convert_path.format(
            cur_from='RUBBBBBB',
            cur_to='UsD',
            amount=42
        )
        resp = await self.client.get(path=convert_path)
        self.assertStatusCode(resp, 400)
