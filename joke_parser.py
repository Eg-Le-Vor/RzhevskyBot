import aiohttp
from bs4 import BeautifulSoup

import random


BASE_URL = 'https://baneks.ru/'


async def get_joke(available_jokes: list):
    joke_number = random.SystemRandom().choice(available_jokes)
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + str(joke_number)) as joke_response:
            print(joke_response.charset)
            joke = await joke_response.text(errors='ignore')
    joke = BeautifulSoup(joke, 'lxml').find('p').text.replace('\n\n', '\n').strip().strip('\n')
    return joke, joke_number