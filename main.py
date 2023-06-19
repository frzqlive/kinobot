import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = 'TOKEN'
API_URL = 'https://api.kinopoisk.dev/v1.3/movie/random'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Получить рекомендацию')
    keyboard.add(button)
    await message.answer('Добро пожаловать! Нажмите кнопку "Получить рекомендацию", чтобы получить случайный фильм.', reply_markup=keyboard)


@dp.message_handler(text='Получить рекомендацию')
async def get_recommendation(message: types.Message):
    headers = {'accept': 'application/json', 'X-API-KEY': 'X-API-KEY'}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        film = response.json()
        title = film.get('name')
        poster = film.get('poster').get('url')
        description = film.get('description')
        rating = round(film.get('rating').get('kp'), 1)

        if description is None:
            description = '🖤'

        truncated_description = truncate(description, 1024)

        text = f'<b>{title}</b>\n\n' \
               f'{truncated_description}\n\n' \
               f'Рейтинг: {rating}'

        await bot.send_photo(message.chat.id, poster, caption=text, parse_mode='HTML')
    else:
        await message.answer('Произошла ошибка при получении данных. Попробуйте позже.')


@dp.message_handler()
async def unknown_command(message: types.Message):
    await message.answer("Извините, я не понимаю эту команду. Введите /start для начала работы.")


def truncate(text, max_length):
    if len(text) > max_length:
        return text[:max_length-3] + '...'
    return text


if __name__ == '__main__':
    async def main():
        await dp.start_polling()

    asyncio.run(main())