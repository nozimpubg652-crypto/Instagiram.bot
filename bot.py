import asyncio, aiosqlite, logging, os, yt_dlp, random, re, subprocess
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ChatMemberStatus

# Loglarni yoqish
logging.basicConfig(level=logging.INFO)

TOKEN = "8514343100:AAGcJvEM-wOSMU7ZOdzzbqxZCnE3WMnxDpo"
ADMIN_ID = 8639222385
CHANNEL_ID = "@temuzikinsta"
CHANNEL_LINK = "https://t.me/temuzikinsta"
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
    bot_info = await bot.get_me()
    BOT_USERNAME = bot_info.username
    async with aiosqlite.connect(db_path) as db:
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute("PRAGMA busy_timeout = 3000")
        await db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, invited_count INTEGER DEFAULT 0)")
        await db.execute("CREATE TABLE IF NOT EXISTS referrals (inviter_id INTEGER, invited_id INTEGER UNIQUE)")
        await db.commit()

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
    except: return False

async def force_sub(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=CHANNEL_LINK)]])
    await msg.answer("❌ Botdan foydalanish uchun avval kanalga obuna bo‘ling.", reply_markup=kb)

@dp.message(Command("start"))
async def start(msg: Message, command: CommandObject):
    if not await check_sub(msg.from_user.id): return await force_sub(msg)
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
    if not await check_sub(msg.from_user.id): return await force_sub(msg)
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT invited_count FROM users WHERE user_id = ?", (msg.from_user.id,)) as cursor:
            row = await cursor.fetchone()
            count = row[0] if row else 0
    if count >= 5: await msg.answer("✅ Tabriklaymiz! Sayt: https://leofame.com")
    else: await msg.answer(f"Siz {count}/5 ta do'st taklif qildingiz.\nHavola: https://t.me/{BOT_USERNAME}?start={msg.from_user.id}")

@dp.message(F.text == "📥 Video Silkasi")
async def ask_link(msg: Message, state: FSMContext):
    if not await check_sub(msg.from_user.id): return await force_sub(msg)
    await state.set_state(States.waiting_for_insta_link)
    await msg.answer("Instagram linkini yuboring:")

@dp.message(States.waiting_for_insta_link)
async def dl_video(msg: Message, state: FSMContext):
    if "instagram.com/" not in msg.text: return await msg.answer("❌ Noto'g'ri link.")
    status = await msg.answer("⏳ Yuklanmoqda...")
    file_path = f"vid_{msg.from_user.id}_{random.randint(1000,9999)}.mp4"
    audio_path = file_path.replace(".mp4", ".mp3")
    
    try:
        def dl(): 
            ydl_opts = {
                "quiet": True, "outtmpl": file_path, "noplaylist": True, 
                "retries": 3, "socket_timeout": 20, "extract_flat": False, "writedescription": False
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: return ydl.extract_info(msg.text, download=True)
        
        info = await asyncio.to_thread(dl)
        title = info.get("title", "Video")
        description = (info.get("description") or info.get("caption") or info.get("title") or "")
        
        # Videoni yuborish
        await msg.answer_video(FSInputFile(file_path), caption=f"📌 Sarlavha: {title}")
        
        # Matnni yuborish
        if description:
            await msg.answer(f"📝 Matn:\n\n{description[:4000]}")
            # Hashtaglarni ajratish
            hashtags = re.findall(r"#[^\s#]+", description)
            if hashtags:
                await msg.answer("🏷 Hashtaglar:\n" + " ".join(hashtags[:20]))
        
        # ffmpeg tekshiruvi va audio yaratish
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
            subprocess.run(["ffmpeg", "-i", file_path, "-vn", "-ab", "192k", audio_path, "-y"], check=True)
            await msg.answer_audio(FSInputFile(audio_path), caption="🎵 Audio format")
        except Exception:
            logging.error("ffmpeg o'rnatilmagan yoki xatolik yuz berdi.")
        
        await status.delete()
    except Exception as e: await status.edit_text(f"❌ Xatolik yuz berdi: {e}")
    finally:
        for p in [file_path, audio_path]:
            if os.path.exists(p): 
                try: os.remove(p)
                except: pass
    await state.clear()

@dp.message(F.text == "✨ Niklar yaratish paneli")
async def ask_nick(msg: Message, state: FSMContext):
    if not await check_sub(msg.from_user.id): return await force_sub(msg)
    await state.set_state(States.waiting_for_nick)
    await msg.answer("Ismingizni yuboring:")

@dp.message(States.waiting_for_nick)
async def make_nick(msg: Message, state: FSMContext):
    await msg.answer(f"✅ Yangi nik: {msg.text.replace(' ', '_')}_{random.randint(100000, 999999)}")
    await state.clear()

@dp.message(F.text == "📩 Admenga savol yulash")
async def ask_admin(msg: Message, state: FSMContext):
    if not await check_sub(msg.from_user.id): return await force_sub(msg)
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
