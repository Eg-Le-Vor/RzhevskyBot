import motor.motor_asyncio


MONGO_URI = 'mongodb://localhost:27017/'
JOKE_NUMBERS = list(range(1, 1143))


class Database:
    def __init__(self):
        cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        self.chats_collection = cluster.rzhevsky.chats
    
    async def register_new_chat(self, chat_id: str):
        await self.chats_collection.insert_one({'chat_id': chat_id, 'available_jokes': JOKE_NUMBERS})
        print(f'Чат добавлен.\nИД чата: {chat_id}')
    
    async def is_chat_registered(self, chat_id: str):
        return bool(await self.chats_collection.find_one({'chat_id': chat_id}))
    
    async def get_available_jokes(self, chat_id: str):
        return (await self.chats_collection.find_one({'chat_id': chat_id}))['available_jokes']
    
    async def update_available_jokes(self, chat_id: str, joke_number: int):
        new_available_jokes = (await self.chats_collection.find_one({'chat_id': chat_id}))['available_jokes']
        new_available_jokes.remove(joke_number)
        await self.chats_collection.update_one({'chat_id': chat_id}, {'$set': {'available_jokes': new_available_jokes}})
        print(f'Список доступных анекдотов обновлён: удалён анекдот №{joke_number}.\nИД чата: {chat_id}')