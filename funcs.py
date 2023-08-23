import io
import string
import aiohttp


async def justify_track_fn(full_track_fn: str):
    return ''.join([i for i in list(full_track_fn) if i in string.ascii_letters])


async def download_file(request_url: str, storage: io.BytesIO | None = None) -> io.BytesIO:
    storage = io.BytesIO() if storage is None else storage
    storage.seek(0)

    async with aiohttp.client.ClientSession() as client:
        response = await client.get(request_url)

        storage.write(await response.read())
        storage.seek(0)
    return storage
