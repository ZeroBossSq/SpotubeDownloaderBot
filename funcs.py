import io
import string
import aiohttp
import sqlite3
import settings


async def justify_track_fn(full_track_fn: str):
    return ''.join([i for i in list(full_track_fn) if i in f'{string.ascii_letters} -']).replace(' ', '_')


async def download_file(request_url: str, storage: io.BytesIO | None = None) -> io.BytesIO:
    storage = io.BytesIO() if storage is None else storage
    storage.seek(0)

    async with aiohttp.client.ClientSession() as client:
        response = await client.get(request_url)

        storage.write(await response.read())
        storage.seek(0)
    return storage


async def search_track_info_in_db(full_track_name: str) -> io.BytesIO | None:
    with sqlite3.connect(settings.DB_FN) as sql:
        cursor = sql.cursor()
        res = cursor.execute(f'SELECT * FROM tracks WHERE full_name="{full_track_name}"').fetchone()

        if res is None:
            return None

        _, data = res
        return io.BytesIO(data)
