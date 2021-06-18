from typing import Dict

from aiohttp.test_utils import unittest_run_loop

from tests.currency import BaseTestHandlers


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
    async def test_path_data(self):
        """Тест: обновление данных"""
        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_currency)
        resp.read()

        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_update_currency)
        resp.read()

        self.assertEqual(resp.status, 200, await resp.text())

    @unittest_run_loop
    async def test_update(self):
        """Тест: инвалидация"""
        database_path = self.database_path.format(merge_state=1)
        resp = await self.client.post(path=database_path, json=self.data_currency)
        resp.read()

        database_path = self.database_path.format(merge_state=0)
        resp = await self.client.post(path=database_path, json=self.data_path_currency)
        resp.read()

        self.assertEqual(resp.status, 200, await resp.text())
