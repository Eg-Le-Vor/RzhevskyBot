import requests
import random


BASE_URL = "https://baneks.ru/"
JOKE_COUNT = 1143


class Joke:

    def __init__(self):
        self.numbers = list(range(1, JOKE_COUNT))

    def get_random_joke(self):
        temp = random.SystemRandom().choice(self.numbers)
        result = requests.get(BASE_URL + str(temp))
        result.encoding = "utf-8"
        print(result)
        # print(temp)
        self.numbers.remove(temp)


joke = Joke()
joke.get_random_joke() 