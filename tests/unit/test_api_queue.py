from unittest import IsolatedAsyncioTestCase, mock

from ucloud.api import queue


class TestApiQueue(IsolatedAsyncioTestCase):
    async def test_push(self):
        """ Tests POST /push """
        service = mock.AsyncMock()
        service.push.return_value = 'uid'

        result = await queue.push({}, service)
        self.assertEqual(result, 'uid')
        service.push.assert_awaited_once_with({})

    async def test_pop(self):
        """ Tests GET /pop """
        service = mock.AsyncMock()
        service.pop.return_value = 'data'

        result = await queue.pop(service)
        self.assertEqual(result, 'data')
        service.pop.assert_awaited_once_with()

    async def test_empty(self):
        """ Tests DELETE /empty """
        service = mock.AsyncMock()
        await queue.empty(service)
        service.empty.assert_awaited_once_with()

    async def test_total(self):
        """ Tests GET /total """
        service = mock.AsyncMock()
        service.total.return_value = 123

        result = await queue.total(service)
        self.assertEqual(result, 123)
        service.total.assert_awaited_once_with()
