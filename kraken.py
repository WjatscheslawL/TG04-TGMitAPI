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

from config import TOKEN, KRAKEN_API_KEY,KRAKEN_API_SIGN
from datetime import datetime, timedelta

bot = Bot(token=TOKEN)
dp = Dispatcher()
# end of INIT
#url = "https://api.kraken.com/0/private/AddOrder"
url = "https://demo-futures.kraken.com/"

payload = json.dumps({
  "nonce": 163245617,
  "ordertype": "limit",
  "type": "buy",
  "volume": "1.25",
  "pair": "XBTUSD",
  "price": "27500",
  "cl_ord_id": "6d1b345e-2821-40e2-ad83-4ecb18a06876"
})

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'API-Key': KRAKEN_API_KEY,
  'API-Sign': KRAKEN_API_SIGN
}

data = {
    "nonce": "1616492376594",
    "ordertype": "limit",
    "pair": "XBTUSD",
    "price": 37500,
    "type": "buy",
    "volume": 1.25
}
api_sec = "kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg=="


def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


#signature = get_kraken_signature("/0/private/AddOrder", data, api_sec)

#print("API-Sign: {}".format(signature))

    # sends an HTTP request and read response body
def make_request(requestType, endpoint, postUrl="", postBody=""):
    return make_request_raw(requestType, endpoint, postUrl, postBody).read().decode("utf-8")
 # returns historical data for futures and indices
def get_history(self, symbol, lastTime=""):
    endpoint = "/derivatives/api/v3/history"
    if lastTime != "":
        postUrl = "symbol=%s&lastTime=%s" % (symbol, lastTime)
    else:
        postUrl = "symbol=%s" % symbol
    return make_request("GET", endpoint, postUrl=postUrl)

# get history
symbol = "PI_XBTUSD"  # "PI_XBTUSD", "cf-bpi", "cf-hbpi"
lastTime = datetime.datetime.strptime(
        "2016-01-20", "%Y-%m-%d").isoformat() + ".000Z"
result = get_history(symbol, lastTime=lastTime)
print("get_history:\n", result)

def get_kraken_info():
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response


@dp.message(Command("kraken"))
async def kraken(message: Message):
    apod = get_kraken_info()
    #pair = apod['pair']
    #price = apod['price']

    await message.answer(f"{apod.text}, Попробуйте еще раз.")
# eof messages


# start main
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
