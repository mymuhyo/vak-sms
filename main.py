'''
Bu vak-sms.com site api idan foydalanib teegram orqali raqam olish va sms code ni qabul qilish uchun
'''

import logging
import requests
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = '6219627123:AAEVQ7uQCl7d33LGcauEUkYIen_rMbVZ9tA'

API_KEY = 'e2ac1e74152c4470927da98ad5a792c6'

bot = Bot(token=BOT_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a dispatcher
dp = Dispatcher(bot)



# Handler for the /start command


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    ''' Start buyrug'i uchun '''
    await message.reply("Hello! I'm your Telegram bot.")

# Handler for the "Get Balance" button


@dp.message_handler(commands=['getbalance'])
async def get_balance(message: types.Message):
    ''' Balansni olish'''
    url = f'https://vak-sms.com/stubs/handler_api.php?api_key={API_KEY}&action=getBalance'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.text.split(":")
        print("Response:", response.text)  # Print the response for debugging

        if len(data) == 2 and data[0] == "ACCESS_BALANCE":
            balance = float(data[1])
            await message.reply(f"Your balance is: {balance}")
        else:
            await message.reply("Invalid response format.")
    except requests.exceptions.RequestException as error:
        await message.reply(f"An error occurred: {error}")

# Handler for the /getprice command


@dp.message_handler(commands=['getprice'])
async def get_price(message: types.Message):
    '''Raqam narxini aniqlash uchun'''
    url = f'https://vak-sms.com/stubs/handler_api.php?api_key={API_KEY}&action=getPrices&service=tg&country=6'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if '6' in data:
            country_data = data['6']
            if 'tg' in country_data:
                tg_data = country_data['tg']
                cost = tg_data['cost']
                count = tg_data['count']
                await message.reply(f"Narxi: {cost} rubl\nSoni:  {count} ta")
            else:
                await message.reply("No data for 'tg' service")
        else:
            await message.reply("No data for country '6'")
    except requests.exceptions.RequestException as error:
        await message.reply(f"An error occurred: {error}")

# Handler for the /getnumber command


@dp.message_handler(commands=['getnumber'])
async def get_number(message: types.Message):
    '''Raqam olish uchun'''
    url = f'https://vak-sms.com/stubs/handler_api.php?api_key={API_KEY}&action=getNumber&service=tg&operator=telkomsel&country=6'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.text.split(":")
        print("Response:", response.text)  # Print the response for debugging

        if len(data) == 3 and data[0] == "ACCESS_NUMBER":
            number_id = data[1]
            number = data[2]
            await message.reply(f"ID: {number_id}\nNumber: {number}")
        else:
            await message.reply("Invalid response format.")
    except requests.exceptions.RequestException as error:
        await message.reply(f"An error occurred: {error}")

# Start the bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
