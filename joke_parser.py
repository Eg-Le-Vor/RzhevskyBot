import requests
from bs4 import BeautifulSoup

import random


BASE_URL = 'https://baneks.ru/'
JOKE_COUNT = 1143


class Joke:

    def __init__(self):
        self.numbers = list(range(1, JOKE_COUNT))

    def get_joke(self):
        random_number = random.SystemRandom().choice(self.numbers)
        request = requests.get(BASE_URL + str(random_number))
        request.encoding = 'utf-8'
        joke = BeautifulSoup(request.text, 'lxml').find('p').text.replace('\n\n', '\n').strip().strip('\n')
        self.numbers.remove(random_number)
        return joke