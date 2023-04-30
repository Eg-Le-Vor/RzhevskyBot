import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from joke_parser import Joke

from config import TOKEN


bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    print(f'ИД чата: {message.chat.id}')
    joke = Joke()
    joke.get_joke()
    await message.answer(f'*Внимание, анекдот!*\n\n{joke.get_joke()}', parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dispatcher)