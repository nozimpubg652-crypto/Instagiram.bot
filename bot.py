import asyncio, aiosqlite, logging, os, yt_dlp, random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Loglarni yoqish (xatolarni ko'rib turish uchun)
logging.basicConfig(level=logging.INFO)

TOKEN = "8514343100:AAGcJvEM-wOSMU7ZOdzzbqxZCnE3WMnxDpo"
ADMIN_ID = 8639222385
BOT_USERNAME = None
db_path = "bot_data.db"
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class States(StatesGroup):
    waiting_for_insta_link = State()
    waiting_for_nick = State()
    waiting_for_question = State()

async def init_db():
    global BOT_USERNAME
    # Bot username ni olish
    bot_info = await bot.get_me()
    BOT_USERNAME = bot_info.username
    
    async with aiosqlite.connect(db_path) as db:
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute("PRAGMA busy_timeout = 3000")
        await db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, invited_count INTEGER DEFAULT 0)")
        await db.execute("CREATE TABLE IF NOT EXISTS referrals (inviter_id INTEGER, invited_id INTEGER UNIQUE)")
        await db.commit()

@dp.message(Command("start"))
async def start(msg: Message, command: CommandObject):
    user_id = msg.from_user.id
    args = command.args
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)) as cursor:
            if cursor.rowcount > 0 and args and args.isdigit() and len(args) < 15:
                inviter = int(args)
                if inviter != user_id:
                    try:
                        await db.execute("INSERT OR IGNORE INTO referrals (inviter_id, invited_id) VALUES (?, ?)", (inviter, user_id))
                        await db.execute("UPDATE users SET invited_count = invited_count + 1 WHERE user_id = ?", (inviter,))
                        await db.commit()
                    except: pass
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📥 Video Silkasi"), KeyboardButton(text="🚀 Tekin Nakrutka")], [KeyboardButton(text="💳 Pulli sxema paneli"), KeyboardButton(text="📩 Admenga savol yulash")], [KeyboardButton(text="✨ Niklar yaratish paneli"), KeyboardButton(text="🎮 Oʻyinlar paneli")], [KeyboardButton(text="💰 Valyuta kursi"), KeyboardButton(text="🏎 The Bugatti Chiron Heshteg")], [KeyboardButton(text="𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇"), KeyboardButton(text="⏱ Vidiyo qõyish vaqti✅🫠")]], resize_keyboard=True)
    await msg.answer("Xush kelibsiz!", reply_markup=kb)

@dp.message(F.text == "🚀 Tekin Nakrutka")
async def nakrutka(msg: Message):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT invited_count FROM users WHERE user_id = ?", (msg.from_user.id,)) as cursor:
            row = await cursor.fetchone()
            count = row[0] if row else 0
    if count >= 5: await msg.answer("✅ Tabriklaymiz! Sayt: https://leofame.com")
    else: await msg.answer(f"Siz {count}/5 ta do'st taklif qildingiz.\nHavola: https://t.me/{BOT_USERNAME}?start={msg.from_user.id}")

@dp.message(F.text == "📥 Video Silkasi")
async def ask_link(msg: Message, state: FSMContext):
    await state.set_state(States.waiting_for_insta_link)
    await msg.answer("Instagram linkini yuboring:")

@dp.message(States.waiting_for_insta_link)
async def dl_video(msg: Message, state: FSMContext):
    if "instagram.com/" not in msg.text: return await msg.answer("❌ Noto'g'ri link.")
    status = await msg.answer("⏳ Yuklanmoqda...")
    file_path = f"vid_{msg.from_user.id}_{random.randint(1000,9999)}.mp4"
    try:
        def dl(): 
            ydl_opts = {"quiet": True, "outtmpl": file_path, "noplaylist": True, "retries": 3, "socket_timeout": 20}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([msg.text])
        await asyncio.to_thread(dl)
        await msg.answer_video(FSInputFile(file_path))
        await status.delete()
    except Exception as e: await status.edit_text(f"❌ Xatolik yuz berdi: {e}")
    finally:
        if os.path.exists(file_path): 
            try: os.remove(file_path)
            except: pass
    await state.clear()

@dp.message(F.text == "✨ Niklar yaratish paneli")
async def ask_nick(msg: Message, state: FSMContext):
    await state.set_state(States.waiting_for_nick)
    await msg.answer("Ismingizni yuboring:")

@dp.message(States.waiting_for_nick)
async def make_nick(msg: Message, state: FSMContext):
    await msg.answer(f"✅ Yangi nik: {msg.text.replace(' ', '_')}_{random.randint(100000, 999999)}")
    await state.clear()

@dp.message(F.text == "📩 Admenga savol yulash")
async def ask_admin(msg: Message, state: FSMContext):
    await state.set_state(States.waiting_for_question)
    await msg.answer("Savolingizni yozing:")

@dp.message(States.waiting_for_question)
async def send_q(msg: Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📩 Savol (ID {msg.from_user.id}): {msg.text}")
    await msg.answer("✅ Yuborildi.")
    await state.clear()

@dp.message(F.photo)
async def photo_handler(msg: Message):
    if msg.from_user.id == ADMIN_ID: return
    await bot.send_message(ADMIN_ID, f"📸 Yangi chek! ID: {msg.from_user.id}")
    await msg.answer("✅ Chek admin tekshiruvi uchun yuborildi.")

@dp.message(F.text == "🎮 Oʻyinlar paneli")
async def game(msg: Message): await msg.answer(f"Bot tanladi: {random.choice(['Tosh', 'Qaychi', 'Qogoz'])}.")
@dp.message(F.text == "💰 Valyuta kursi")
async def valyuta(msg: Message): await msg.answer("USD: 12,800 UZS")
@dp.message(F.text == "🏎 The Bugatti Chiron Heshteg")
async def bugatti(msg: Message): await msg.answer("The Bugatti Chiron is a mid-engine two-seater...")
@dp.message(F.text == "𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")
async def eslatma(msg: Message): await msg.answer("𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” zero eslatma...")
@dp.message(F.text == "⏱ Vidiyo qõyish vaqti✅🫠")
async def vaqt(msg: Message): await msg.answer("Rekga chiqish vaqtlari: 6:00, 8:00, 11:00, 16:00, 20:00, 22:00, 00:00")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__": 
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
