import requests
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Your Credentials
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
SMM_API_KEY = "f02c626df4cef843d48a2beecd121a66"
SMM_API_URL = "https://tntsmm.in/api/v2"
SERVICE_ID = "6680"  # Instagram Views Service ID

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Connect to database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
conn.commit()

# Start Command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        await message.reply("⚠️ You have already claimed your free 1000 views!")
    else:
        await message.reply("👋 Welcome! Send your Instagram Reels link to get **1000 free views** 🎉")

# Handle Instagram Reels Link
@dp.message_handler()
async def process_order(message: types.Message):
    user_id = message.from_user.id
    user_link = message.text.strip()
    
    # Check if user already used free order
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        await message.reply("⚠️ You have already claimed your free 1000 views!")
        return
    
    if "instagram.com/reel/" not in user_link:
        await message.reply("❌ Invalid link! Please send a valid **Instagram Reels link**.")
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
        await message.reply(f"✅ Your **1000 views** order has been placed successfully! 🚀\n📦 **Order ID:** {response['order']}\n⏳ You will receive the views in **10-20 minutes**.")
    else:
        await message.reply(f"⚠️ Failed to place order: {response}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
