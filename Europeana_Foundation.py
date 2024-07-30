import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
import json
import urllib.parse
import hashlib
import hmac
import base64

from config import TOKEN, EUFO_API_KEY, KEY_API_SPORT
from datetime import datetime, timedelta

bot = Bot(token=TOKEN)
dp = Dispatcher()
# end of INIT

url = f"https://api.sportmonks.com/v3/football/fixtures?api_token={KEY_API_SPORT}&include=statistics;events"


def get_info():
    # response = requests.request("POST", url, data=search)
    response = requests.request("GET", url)
    return response.json()


@dp.message(Command("sport"))
async def sport(message: Message):
    data = get_info()
    matches = data['data']
    names = []
    for breed in matches:
        print(breed['name'])
        names.append(breed['name'])
    await message.answer(f"{names}")
# eof messages


# start main
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
