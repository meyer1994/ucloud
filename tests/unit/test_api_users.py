from unittest import IsolatedAsyncioTestCase, mock

from ucloud.api import users


class TestApiUsers(IsolatedAsyncioTestCase):
    async def test_create(self):
        """ Tests POST /create """
        service = mock.AsyncMock()
        service.create.return_value = 'data'

        result = await users.create({}, service)

        self.assertEqual(result, 'data')

        service.create.assert_awaited_once_with({})

    async def test_delete(self):
        """ Tests DELETE /delete/{uid} """
        service = mock.AsyncMock()
        service.delete.return_value = 'data'

        result = await users.delete('uid', service)

        self.assertEqual(result, 'data')

        service.delete.assert_awaited_once_with('uid')

    async def test_login(self):
        """ Tests POST /login """
        service = mock.AsyncMock()
        service.login.return_value = 'data'

        result = await users.login('uid', {}, service)

        self.assertEqual(result, 'data')

        service.login.assert_awaited_once_with('uid', {})

    async def test_delete(self):
        """ Tests DELETE /delete/{uid} """
        service = mock.AsyncMock()
        service.delete.return_value = 'data'

        result = await users.delete('uid', service)

        self.assertEqual(result, 'data')

        service.delete.assert_awaited_once_with('uid')
