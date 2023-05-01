import requests
from bs4 import BeautifulSoup

import random


BASE_URL = 'https://baneks.ru/'
# JOKE_COUNT = 1143


# class Joke:

#     def __init__(self, available_jokes):
#         self.numbers = list(range(1, available_jokes))

async def get_joke(available_jokes: list):
    joke_number = random.SystemRandom().choice(available_jokes)
    joke_request = requests.get(BASE_URL + str(joke_number))
    joke_request.encoding = 'utf-8'
    joke = BeautifulSoup(joke_request.text, 'lxml').find('p').text.replace('\n\n', '\n').strip().strip('\n')
    return joke_number, joke