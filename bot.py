import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import link
from aiogram.utils import executor

from joke_parser import get_joke

from config import TOKEN


bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    print(f'ИД чата: {message.chat.id}')
    joke_number, joke = await get_joke(list(range(1, 1143)))
    await message.answer(f'*Внимание, анекдот!*\n\n{joke}', parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dispatcher)