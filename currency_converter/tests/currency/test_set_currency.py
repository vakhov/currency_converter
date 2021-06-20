from typing import Dict
from unittest import mock
from unittest.mock import MagicMock

from aiohttp.test_utils import unittest_run_loop

from tests.currency import BaseTestHandlers, RedisMock


class TestDatabaseHandler(BaseTestHandlers):
    """Тесты ручки обновление валют /database"""
    database_path = '/database?merge={merge_state}'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.data_currency: Dict[str, float] = dict(
            USD=72.5048,
            EUR=86.7012,
            JPY=65.5500
        )
        cls.data_path_currency: Dict[str, float] = dict(
            USD=73.5048,
        )
        cls.data_update_currency: Dict[str, float] = dict(
            USD=62.5048,
            EUR=76.7012,
            JPY=85.5500
        )

    @unittest_run_loop
    @mock.patch('app.helpers.mixins.RedisConnectMixin.connect', new_callable=RedisMock)
    async def test_non_valid_http_method(self, redis_connect: MagicMock):
        """Тест: не валидный http метод"""
        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.get(path=database_path, json=self.data_update_currency)
        await resp.read()

        self.assertStatusCode(resp, 405)
        self.assertEqual(0, redis_connect.call_count)

    @unittest_run_loop
    @mock.patch('app.helpers.mixins.RedisConnectMixin.connect', new_callable=RedisMock)
    async def test_path_data(self, redis_connect: MagicMock):
        """Тест: обновление данных"""
        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_currency)
        await resp.read()

        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_update_currency)
        await resp.read()

        self.assertStatusCode(resp)
        self.assertEqual(2, redis_connect.call_count)

    @unittest_run_loop
    @mock.patch('app.helpers.mixins.RedisConnectMixin.connect', new_callable=RedisMock)
    async def test_update(self, redis_connect: MagicMock):
        """Тест: инвалидация"""
        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_currency)
        await resp.read()

        database_path = self.database_path.format(merge_state=0)
        resp = await self.client.post(path=database_path, json=self.data_path_currency)
        await resp.read()

        self.assertStatusCode(resp)
        self.assertEqual(2, redis_connect.call_count)
