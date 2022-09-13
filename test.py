import asyncio
import datetime
import aiohttp
import asyncio_base
import re
from cache import AsyncLRU, AsyncTTL


async def get_people(session, people_id):
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        json_data = await response.json()

        return json_data


@AsyncLRU(maxsize=1024)
async def get_film(session, film_url):
    async with session.get(f'{film_url}') as response:
        json_data = await response.json()
        return json_data


@AsyncLRU(maxsize=500)
async def get_species(session, species_url):
    async with session.get(f'{species_url}') as response:
        json_data = await response.json()
        return json_data


@AsyncLRU(maxsize=500)
async def get_starships(session, starships_url):
    async with session.get(f'{starships_url}') as response:
        json_data = await response.json()
        return json_data


@AsyncLRU(maxsize=500)
async def get_vehicles(session, vehicles_url):
    async with session.get(f'{vehicles_url}') as response:
        json_data = await response.json()
        return json_data


async def main():
    async with aiohttp.ClientSession() as session:
        coroutines = (get_people(session, i) for i in range(1, 20))
        result = await asyncio.gather(*coroutines)
        for item in result:
            if 'url' not in item.keys():
                continue
            coroutines_film = (get_film(session, i) for i in item['films'])
            result_films = await asyncio.gather(*coroutines_film)
            list_films = [film['title'] for film in result_films]
            coroutines_species = (get_species(session, i) for i in item['species'])
            result_species = await asyncio.gather(*coroutines_species)
            list_species = [species['name'] for species in result_species]
            coroutines_starships = (get_starships(session, i) for i in item['starships'])
            result_starships = await asyncio.gather(*coroutines_starships)
            list_starships = [starships['name'] for starships in result_starships]
            coroutines_vehicles = (get_vehicles(session, i) for i in item['vehicles'])
            result_vehicles = await asyncio.gather(*coroutines_vehicles)
            list_vehicles = [vehicles['name'] for vehicles in result_vehicles]

            people = asyncio_base.People(
                id=int(re.findall(r'\d\d{0,2}', item['url'])[0]),
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
                species=', '.join(list_species),
                starships=', '.join(list_starships),
                vehicles=', '.join(list_vehicles)
            )
            asyncio_base.session.add(people)
            asyncio_base.session.commit()
            print(people.id)


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
