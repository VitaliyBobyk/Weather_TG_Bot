from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# Main Buttons
markup_requests = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Отримати погоду по геолокації', request_location=True)).add(
    KeyboardButton('Отримати погоду по пошуку'))


