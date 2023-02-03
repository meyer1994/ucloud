from unittest import IsolatedAsyncioTestCase, mock

from ucloud.api import files


class TestApiFiles(IsolatedAsyncioTestCase):
    async def test_write(self):
        """ Tests POST /write """
        service = mock.AsyncMock()
        service.write.return_value = 'uid'

        result = await files.write('file', service)
        self.assertEqual(result, 'uid')
        service.write.assert_awaited_once_with('file')

    async def test_read(self):
        """ Tests GET /read/{uid} """
        service = mock.AsyncMock()
        service.read.return_value = 'uid'

        result = await files.read('uid', service)
        self.assertEqual(result, 'uid')
        service.read.assert_awaited_once_with('uid')

    async def test_remove(self):
        """ Tests DELETE /remove/{uid} """
        service = mock.AsyncMock()
        await files.remove('uid', service)
        service.remove.assert_awaited_once_with('uid')
