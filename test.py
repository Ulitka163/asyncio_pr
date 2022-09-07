import asyncio
import datetime
import aiohttp
import asyncio_base
from cache import AsyncLRU


async def get_people(session, people_id):
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        json_data = await response.json()

        return json_data


@AsyncLRU(maxsize=1000)
async def get_film(session, film_url):
    async with session.get(f'{film_url}') as response:
        json_data = await response.json()
        return json_data


async def main():
    async with aiohttp.ClientSession() as session:
        coroutines = (get_people(session, i) for i in range(1, 20))
        result = await asyncio.gather(*coroutines)
        for item in result:
            coroutines_film = (get_film(session, i) for i in item['films'])
            result_films = await asyncio.gather(*coroutines_film)
            list_films = [film['title'] for film in result_films]
            people = asyncio_base.People(
                id=item['url'][-2:-1],
                birth_year=item['birth_year'],
                eye_color=item['eye_color'],
                films=', '.join(list_films),
                gender=item['gender'],
                hair_color=item['hair_color'],
                height=item['height'],
                homeworld=item['homeworld'],
                mass=item['mass'],
                name=item['name'],
                skin_color=item['skin_color'],
                species=item['species'],
                starships=item['starships'],
                vehicles=item['vehicles']
            )
            asyncio_base.session.add(people)
            asyncio_base.session.commit()
            print(item['films'][1])


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
