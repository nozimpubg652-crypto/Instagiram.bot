import asyncio
import time
import os
import aiosqlite
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import uvicorn

# ================= CONFIG =================
TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))
DB = "app.db"

bot = Bot(TOKEN)
dp = Dispatcher()
app = FastAPI()

user_spam = {}

# ================= DB =================
async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            premium INTEGER DEFAULT 0,
            invites INTEGER DEFAULT 0
        )
        """)
        await db.commit()

# ================= START =================
@dp.message(Command("start"))
async def start(msg: Message):
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (msg.from_user.id,))
        await db.commit()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Tekin Nakrutka", callback_data="free")],
        [InlineKeyboardButton(text="💳 Premium olish", callback_data="buy")],
        [InlineKeyboardButton(text="🌐 Panel", url="http://127.0.0.1:8000")]
    ])

    await msg.answer("👋 Xush kelibsiz!", reply_markup=kb)

# ================= CALLBACK =================
@dp.callback_query(F.data == "buy")
async def buy(call):
    link = f"https://my.click.uz/pay?user={call.from_user.id}&amount=35000"
    await call.message.answer(f"💳 To‘lov link:\n{link}")

@dp.callback_query(F.data == "free")
async def free(call):
    await call.message.answer("📢 5 ta do‘st taklif qiling va premium oling!")

# ================= SIMPLE REF SYSTEM =================
@dp.message(F.text.startswith("/invite"))
async def invite(msg: Message):
    link = f"https://t.me/{(await bot.get_me()).username}?start={msg.from_user.id}"
    await msg.answer(f"🔗 Sizning link:\n{link}")

# ================= ANTI SPAM =================
@dp.message()
async def anti_spam(msg: Message):
    uid = msg.from_user.id
    now = time.time()

    if uid in user_spam and now - user_spam[uid] < 1.2:
        return

    user_spam[uid] = now

# ================= FASTAPI PANEL =================
@app.get("/")
async def home():
    return {"status": "bot running"}

@app.get("/users")
async def users():
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT * FROM users")
        rows = await cur.fetchall()
    return {"users": [dict(zip([c[0] for c in cur.description], r)) for r in rows]}

@app.post("/premium/{user_id}")
async def premium(user_id: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE users SET premium=1 WHERE user_id=?", (user_id,))
        await db.commit()
    return {"status": "ok"}

# ================= RUN BOT =================
async def run_bot():
    await dp.start_polling(bot)

# ================= RUN PANEL =================
async def run_panel():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

# ================= MAIN =================
async def main():
    await init_db()
    await asyncio.gather(
        run_bot(),
        run_panel()
    )

if __name__ == "__main__":
    asyncio.run(main())
