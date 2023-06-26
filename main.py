# bot = Bot(token='6219627123:AAEVQ7uQCl7d33LGcauEUkYIen_rMbVZ9tA')

import logging
import requests
from aiogram import Bot, Dispatcher, types

# Set up logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token='6219627123:AAEVQ7uQCl7d33LGcauEUkYIen_rMbVZ9tA')
# Create a dispatcher
dp = Dispatcher(bot)

# Handler for the /start command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hello! I'm your Telegram bot.")

# Handler for the "Get Balance" button
@dp.message_handler(text='Get Balance')
async def get_balance(message: types.Message):
    api_key = 'e2ac1e74152c4470927da98ad5a792c6'  # Replace with your actual VAKSMS API key
    url = f'https://vak-sms.com/stubs/handler_api.php?api_key={api_key}&action=getBalance'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text.split(":")
        print("Response:", response.text)  # Print the response for debugging

        if len(data) == 2 and data[0] == "ACCESS_BALANCE":
            balance = float(data[1])
            await message.reply(f"Your balance is: {balance}")
        else:
            await message.reply("Invalid response format.")
    except requests.exceptions.RequestException as e:
        await message.reply(f"An error occurred: {e}")


# Start the bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
