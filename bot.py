import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from joke_parser import get_joke

from db import Database

from config import TOKEN


bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)

db = Database()


@dispatcher.message_handler(commands=['start_joking'])
async def start_command(message: types.Message):
    chat_id = message.chat.id
    if not await db.is_chat_registered(chat_id):
        await db.register_new_chat(chat_id)
        await message.answer('Бот добавлен.')
    else:
        print(f'Чат уже зарегистрирован.\nИД чата: {chat_id}')


@dispatcher.message_handler(commands=['joke'])
async def joke(message: types.Message):
    chat_id = message.chat.id
    if not await db.is_chat_registered(chat_id):
        await message.answer('Пожалуйста, зарегистрируйте данный чат командой /start_joking.')
    else:
        available_jokes = await db.get_available_jokes(chat_id)
        joke, joke_number = await get_joke(available_jokes)
        await db.update_available_jokes(chat_id, joke_number)
        await message.answer(f'*Внимание, анекдот!*\n\n{joke}', parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dispatcher)