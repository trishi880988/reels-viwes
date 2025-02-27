import requests
import sqlite3
from aiogram import Bot, Dispatcher, types
import asyncio

# Your Credentials
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
SMM_API_KEY = "f02c626df4cef843d48a2beecd121a66"
SMM_API_URL = "https://tntsmm.in/api/v2"
SERVICE_ID = "6680"  # Instagram Views Service ID

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Connect to database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
conn.commit()

# Start Command
@dp.message(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        await message.answer("⚠️ You have already claimed your free 1000 views!")
    else:
        await message.answer("👋 Welcome! Send your Instagram Reels link to get **1000 free views** 🎉")
    
    # Bot creator credit
    await message.answer("🤖 Bot created by @skillwithgaurav")

# Handle Instagram Reels Link
@dp.message()
async def process_order(message: types.Message):
    user_id = message.from_user.id
    user_link = message.text.strip()
    
    # Check if user already used free order
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        await message.answer("⚠️ You have already claimed your free 1000 views!")
        return
    
    if "instagram.com/reel/" not in user_link:
        await message.answer("❌ Invalid link! Please send a valid **Instagram Reels link**.")
        return
    
    # Place Order
    data = {
        "key": SMM_API_KEY,
        "action": "add",
        "service": SERVICE_ID,
        "link": user_link,
        "quantity": 1000
    }
    response = requests.post(SMM_API_URL, data=data).json()
    
    if "order" in response:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        await message.answer(f"✅ Your **1000 views** order has been placed successfully! 🚀\n📦 **Order ID:** {response['order']}\n⏳ You will receive the views in **10-20 minutes**.")
    else:
        await message.answer(f"⚠️ Failed to place order: {response}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
