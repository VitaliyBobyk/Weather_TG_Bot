import hashlib

import requests
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType, InputTextMessageContent, \
    InlineQueryResultArticle

# Main Buttons
markup_requests = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Отримати погоду по геолокації', request_location=True))

API_TOKEN = '1290171926:AAEHtIDYG0SZBnbF00gGGXzgTqOxPQfyA8Y'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['location'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await bot.send_message(message.from_user.id,
                           "Щоб отримати погоду за місцем розташування, необхідно надати дозві на отримання геолокації!",
                           reply_markup=markup_requests)


@dp.inline_handler()
async def handler(inline_query: types.InlineQuery):
    city = get_weather(str(inline_query.query))
    print(city)
    if city != None:
        formatet_text = f'Hello!\nWeather in {city["city"]}\nTemperature: {city["temprature"]} °С\nHumidity: {city["humidity"]} %'
        text = inline_query.query
        input_content = InputTextMessageContent(formatet_text)
        result_id: str = hashlib.md5(text.encode()).hexdigest()
        item = InlineQueryResultArticle(
            id=result_id,
            title=f'Result {city["city"]!r}',
            input_message_content=input_content,
        )
        await bot.answer_inline_query(inline_query.id, results=[item])


@dp.message_handler()
async def weather(message: types.Message):
    city = get_weather(str(message.text))
    if city != None:
        formatet_text = f'Hello!\nWeather in {city["city"]}\nTemperature: {city["temprature"]} °С\nHumidity: {city["humidity"]} %'
        await bot.send_message(message.from_user.id, str(formatet_text), reply_markup=markup_requests)


@dp.message_handler(content_types=ContentType.LOCATION)
async def location(message: types.Message):
    if message.location is not None:
        lon = message.location.longitude
        lat = message.location.latitude
        city = get_weather(lon=lon, lat=lat)
        if city != None:
            formatet_text = f'Hello!\nWeather in {city["city"]}\nTemperature: {city["temprature"]} °С\nHumidity: {city["humidity"]} %'
            await bot.send_message(message.from_user.id, str(formatet_text), reply_markup=markup_requests)


def get_weather(city='', lon=0, lat=0):
    appid = 'd4d6b0bfecbeb4c1467c499c6557acd1'
    if city:
        try:
            slug = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'
            res = requests.get(slug).json()
            context = {
                'city': res['name'],
                'temprature': int(res['main']['temp'] - 273),
                'humidity': int(res['main']['humidity'])
            }
            return context
        except:
            print('EROR')
    else:
        try:
            slug_geo = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}'
            res = requests.get(slug_geo).json()
            context = {
                'city': res['name'],
                'temprature': int(res['main']['temp'] - 273),
                'humidity': int(res['main']['humidity'])
            }
            return context
        except:
            print('EROR')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
