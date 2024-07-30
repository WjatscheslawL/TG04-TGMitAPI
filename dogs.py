import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests

from config import TOKEN, THE_DOGS_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Вот в этом промежутке мы будем работать и писать новый код


def get_dogs_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_DOGS_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_dogs_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_DOGS_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']


def get_breed_info(breed_name):
    breeds = get_dogs_breeds()()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None

# messages


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши мне название породы, и я пришлю тебе её фото и описание.")


@dp.message()
async def send_dog_info(message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info:
        cat_image_url = get_dogs_image_by_breed(breed_info['id'])
        info = (
            f"Порода - {breed_info['name']}\\n"
            f"Описание - {breed_info['description']}\\n"
            f"Продолжительность жизни - {breed_info['life_span']} лет"
        )
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        await message.answer("Порода не найдена. Попробуйте еще раз.")

# eof messages


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
