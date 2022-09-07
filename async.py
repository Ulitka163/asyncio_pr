import asyncio
import datetime
import aiohttp
from more_itertools import chunked

MAX_CHUNK = 30


async def get_people(session, people_id):
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        json_data = await response.json()

        return json_data


async def main():
    async with aiohttp.ClientSession() as session:
        coroutines = (get_people(session, i) for i in range(1, 10))
        for coroutines_chunk in chunked(coroutines, MAX_CHUNK):
            result = await asyncio.gather(*coroutines_chunk)
            for item in result:
                print(item)


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
