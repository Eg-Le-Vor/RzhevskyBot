import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from datetime import datetime

from joke_parser import get_joke

from db import Database

from utils.bot_token import BOT_TOKEN
from utils.answers import ANSWERS


bot = Bot(BOT_TOKEN)
dispatcher = Dispatcher(bot)

db = Database()


@dispatcher.message_handler(commands=['start_joking'])
async def start_command(message: types.Message):
    chat_id = message.chat.id
    if not await db.is_chat_registered(chat_id):
        await db.register_new_chat(chat_id)
        text = '*Дисклеймер*\n\n'
        text += 'Данный бот создан исключительно в развлекательных целях.\n\n'
        text += 'Если в чате есть лица младше 18 лет – удалите бота из чата (возможно присутствие ненормативной лексики в присылаемых им сообщениях).\n\n'
        text += 'Создатель ничего не пропагандирует и ни к чему не призывает пользователей данного бота.\n\n'
        text += 'Все права и вся ответственность за присылаемые анекдоты закреплены за создателями сайта https://baneks.ru, с которого они и берутся.\n\n'
        text += '*Приятного использования!*'
        await message.answer(text=text, parse_mode='Markdown', disable_web_page_preview=True)
        text = '*Рекомендация*\n\n'
        text += 'Также добавьте к себе в чат *Чювак Бота*, который умеет присылать жабу каждую среду и много других интересных вещей!\n\n'
        text += '*Ссылка: https://t.me/WednesdayDudes_bot*'
        await message.answer(text=text, parse_mode='Markdown', disable_web_page_preview=True)
        text = 'Позвольте представиться, поручик Ржевский!\n'
        text += 'Теперь каждую среду я буду присылать вам самые лучшие из наихудших анекдотов, а также реагировать на некоторые ваши сообщения своими коронными фразами.\n'
        text += 'А сейчас, в качестве приветствия...'
        await message.answer(text=text, parse_mode='Markdown')
        await send_joke(chat_id)


@dispatcher.message_handler(commands=['random_joke'])
async def random_joke_command(message: types.Message):
    chat_id = message.chat.id
    if chat_id in (-935528281, -941653252, -883981301):
        if not await db.is_chat_registered(chat_id):
            await message.answer('Пожалуйста, зарегистрируйте бота командой /start_joking.')
        else:
            await send_joke(message.chat.id)


@dispatcher.message_handler()
async def various_answers(message: types.Message):
    if await db.is_chat_registered(message.chat.id):
        for key, value in ANSWERS.items():
            if key in message.text.lower():
                await message.answer(text=value, parse_mode='Markdown')
                return


async def send_joke(chat_id: str):
    available_jokes = await db.get_available_jokes(chat_id)
    joke, joke_number = await get_joke(available_jokes)
    await db.update_available_jokes(chat_id, joke_number)
    message = f'*Внимание, анекдот!*\n\n{joke}'
    await bot.send_message(text=message, chat_id=chat_id, parse_mode='Markdown')


async def send_jokes_to_all_chats():
    chats_ids = await db.get_all_chats_ids()

    for chat_id in chats_ids:
        try:
            await send_joke(chat_id)
        except Exception as ex:
            print(f'Отправка сообщения провалена.\nОшибка: {ex}')
            continue


async def scheduler():
    while True:
        now = datetime.now()
        if now.weekday() == 2 and now.hour == 10 and now.minute == 0:
            await send_jokes_to_all_chats()
        await asyncio.sleep(60 - now.second)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dispatcher)