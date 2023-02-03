from unittest import IsolatedAsyncioTestCase, mock

from ucloud.api import rest


class TestApiRest(IsolatedAsyncioTestCase):
    async def test_get(self):
        """ Tests GET /get/{uid} """
        service = mock.AsyncMock()
        service.get.return_value = 'data'

        result = await rest.get('uid', service)
        self.assertEqual(result, 'data')
        service.get.assert_awaited_once_with('uid')

    async def test_put(self):
        """ Tests PUT /put/{uid} """
        service = mock.AsyncMock()
        service.put.return_value = 'data'

        result = await rest.put('uid', {}, service)
        self.assertEqual(result, 'data')
        service.put.assert_awaited_once_with('uid', {})

    async def test_post(self):
        """ Tests POST /post """
        service = mock.AsyncMock()
        service.post.return_value = 'data'

        result = await rest.post({}, service)
        self.assertEqual(result, 'data')
        service.post.assert_awaited_once_with({})

    async def test_delete(self):
        """ Tests DELETE /delete/{uid} """
        service = mock.AsyncMock()
        service.delete.return_value = 'data'

        result = await rest.delete('uid', service)
        self.assertEqual(result, 'data')
        service.delete.assert_awaited_once_with('uid')
