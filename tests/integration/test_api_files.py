import uuid
from tempfile import NamedTemporaryFile

from tests.mixins.base import BaseMixin


class TestApiFiles(BaseMixin):
    root = str(uuid.uuid4())

    async def test_write(self):
        """ PUT /{root}/files/write returns entry """
        with NamedTemporaryFile(mode='w+b') as file:
            file.write(b'hello world')
            file.flush()
            file.seek(0)

            # Send file
            response = self.client.put(
                f'/{self.root}/files/write',
                files={'file': (file.name, file, "text/plain")}
            )

        # Check response
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertDictEqual(data, {
            'uid': data.get('uid'),
            'root': self.root,
        })

        uid = data.get('uid')

        # Assert file exist
        response = self.client.get(f'/{self.root}/files/read/{uid}')
        self.assertEqual(response.status_code, 200)

    async def test_read(self):
        """ GET /{root}/files/read/{uid} returns entry """
        uid = self._send_file('hello world')

        with self.client.stream('GET', f'/{self.root}/files/read/{uid}') as s:
            data = s.iter_bytes()
            data = b''.join(data)

        self.assertEqual(s.status_code, 200)
        self.assertEqual(data, b'hello world')

    async def test_read_404(self):
        """ GET /{root}/files/read/{uid} returns 404 """
        uid = uuid.uuid4()

        response = self.client.get(f'/{self.root}/files/read/{uid}')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('detail', data)
        self.assertRegex(data['detail'], r'Item .+ from .+ not found in .+')

    async def test_remove(self):
        """ DELETE /{root}/files/remove/{uid} returns entry """
        uid = self._send_file('hello world')

        # Delete file
        response = self.client.delete(f'/{self.root}/files/remove/{uid}')
        self.assertEqual(response.status_code, 204)

        # Assert is deleted
        response = self.client.get(f'/{self.root}/files/read/{uid}')
        self.assertEqual(response.status_code, 404)

    async def test_remove_404(self):
        """ DELETE /{root}/files/remove/{uid} returns 404 """
        uid = uuid.uuid4()

        response = self.client.delete(f'/{self.root}/files/remove/{uid}')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('detail', data)
        self.assertRegex(data['detail'], r'Item .+ from .+ not found in .+')

    def _send_file(self, data: str) -> str:
        data = data.encode()

        with NamedTemporaryFile(mode='w+b') as file:
            file.write(data)
            file.flush()
            file.seek(0)

            response = self.client.put(
                f'/{self.root}/files/write',
                files={'file': (file.name, file, "text/plain")}
            )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertDictEqual(data, {
            'uid': data.get('uid'),
            'root': self.root,
        })

        return data.get('uid')
