import logging
import requests
import asyncio
import asyncpg

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from MessageTemplates import *
from bot_config import *

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class DialogStates(StatesGroup):
	dialog_start = State()

async def create_pool():
	return await asyncpg.create_pool(
		database = DATABASE_NAME,
		user = PG_USER,
		password= PG_USER_PASSWORD,
		host='localhost'
	)

def send_order(request):
	data = request.POST
	print(data)

def check_api_token(token):
	hostname = 'http://my.prom.ua/api/v1'
	headers = {'Authorization': 'Bearer {}'.format(token),
				'Content-type': 'application/json'}
	request = requests.get(hostname+'/orders/list', headers=headers, verify=False)
	if request.status_code == 200:
		return True
	else:
		return False

async def check_activation_code(activation_code):
	async with conn.acquire() as connection:
		result = await connection.fetch('''
					SELECT * from clients_profile
					''')
	logger.debug('Checking users for code : {}'.format(activation_code))
	for user in result:
		logger.debug("Checking user : {}".format(user))
		if user['activation_code'] == activation_code:
			return True, user['id']
	return False, None

async def is_user_activated(user_id):
	async with conn.acquire() as connection:
		result = await connection.fetchrow('''
					SELECT * from clients_profile
					WHERE telegram_token = $1;
					''', str(user_id))
		if result['telegram_active']:
			return result
	return False


async def is_user_in_db(user_id):
	async with conn.acquire() as connection:
		result = await connection.fetchrow('''
					SELECT * from clients_profile
					WHERE telegram_token = $1;
					''', str(user_id))
		if result:
			return result
	return False

@dp.message_handler(state=DialogStates.dialog_start, content_types=types.ContentTypes.TEXT)
async def dialog_start(message: types.Message, state: FSMContext):
	logger.debug("Checking user : {}".format(message.chat.id))
	user_id = message.chat.id
	user_reply = message.text
	activate, django_id = await check_activation_code(user_reply)
	if activate:
		async with conn.acquire() as connection:
			async with connection.transaction():
				result = await connection.fetchrow('''
							UPDATE clients_profile
							SET telegram_active = True, telegram_token = $1
							WHERE id = $2;
							''', str(user_id), django_id)
		await message.answer(VIBER_API_KEY_REQUEST)
	else:
		await message.answer(VIBER_WRONG_ACTIVATION_CODE_MESSAGE.format(user_reply))
	await state.finish()

@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
	user_name = message.from_user.username
	user_id = message.chat.id
	if not await is_user_in_db(user_id):
		await message.answer(TELEGRAM_GREETING_MESSAGE.format(name=user_name))
		await DialogStates.dialog_start.set()
	else:
		if await is_user_activated(user_id):
			await message.answer(FINISH_MESSAGE)
		else:
			await message.answer('Введите ключ активации')
			await DialogStates.dialog_start.set()
	#await message.answer(VIBER_ACTIVATION_CODE_MESSAGE)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	conn = loop.run_until_complete(create_pool())
	executor.start_polling(dp, loop=loop)