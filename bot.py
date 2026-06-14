import asyncio, aiosqlite, logging, os, yt_dlp, random, re, subprocess
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ChatMemberStatus

logging.basicConfig(level=logging.INFO)

TOKEN = "8514343100:AAGcJvEM-wOSMU7ZOdzzbqxZCnE3WMnxDpo"
ADMIN_ID = 8639222385
CHANNEL_ID = "@temuzikinsta"
CHANNEL_LINK = "https://t.me/temuzikinsta"
BOT_USERNAME = Insa_aqili_bot
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
        await db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, invited_count INTEGER DEFAULT 0)")
        await db.execute("CREATE TABLE IF NOT EXISTS referrals (inviter_id INTEGER, invited_id INTEGER UNIQUE)")
        await db.commit()

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
    except: return False

@dp.message(Command("start"))
async def start(msg: Message, command: CommandObject):
    if not await check_sub(msg.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=CHANNEL_LINK)]])
        return await msg.answer("❌ Botdan foydalanish uchun avval kanalga obuna bo‘ling.", reply_markup=kb)
    
    user_id = msg.from_user.id
    args = command.args
    async with aiosqlite.connect(db_path) as db:
        if args and args.isdigit():
            await db.execute("INSERT OR IGNORE INTO referrals (inviter_id, invited_id) VALUES (?, ?)", (int(args), user_id))
            await db.execute("UPDATE users SET invited_count = invited_count + 1 WHERE user_id = ?", (int(args),))
            await db.commit()
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()
        
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📥 Video Silkasi"), KeyboardButton(text="🚀 Tekin Nakrutka")],
        [KeyboardButton(text="💳 Pulli sxema paneli"), KeyboardButton(text="📩 Admenga savol yulash")],
        [KeyboardButton(text="✨ Niklar yaratish paneli"), KeyboardButton(text="🎮 Oʻyinlar paneli")],
        [KeyboardButton(text="💰 Valyuta kursi"), KeyboardButton(text="🏎 The Bugatti Chiron Heshteg")],
        [KeyboardButton(text="𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇"), KeyboardButton(text="⏱ Vidiyo qõyish vaqti✅🫠")]
    ], resize_keyboard=True)
    await msg.answer("Xush kelibsiz!", reply_markup=kb)

@dp.message(F.text == "💳 Pulli sxema paneli")
async def pulli_sxema(msg: Message):
    txt = ("🚀 TOP SXEMA SOTILADI! 🚀\n"
           "Videolaringiz TOPga chiqishini xohlaysizmi? 🎥\n\n"
           "Bu maxsus sinovdan o‘tgan sxema orqali videolaringiz algoritmda yuqoriga ko‘tariladi, ko‘rishlar va obunachilar keskin oshadi! 📈\n"
           "✅ 100% ishlaydigan va tekshirilgan usul\n"
           "✅ Har qanday kontent uchun mos\n"
           "✅ To‘liq yo‘riqnoma bilan birga beriladi\n"
           "✅ Tez va ishonchli natija kafolatlangan\n\n"
           "💰 Narx: 35ming so'm\n"
           "Karta raqam: [KARTA_RAQAM_BU_YERGA]\n\n"
           "💥 To‘lov qilib chek rasmini yuboring, admin tekshirib tashlaydi. Agar ishlamay qolsa @roziyev2")
    await msg.answer(txt)

@dp.message(F.text == "🚀 Tekin Nakrutka")
async def nakrutka(msg: Message):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT invited_count FROM users WHERE user_id = ?", (msg.from_user.id,)) as cursor:
            row = await cursor.fetchone()
            count = row[0] if row else 0
    if count >= 5:
        await msg.answer("✅ Tabriklaymiz! Sayt: https://leofame.com")
    else:
        await msg.answer(f"Siz {count}/5 ta do'st taklif qildingiz. @{BOT_USERNAME} ga 5 ta do'st qo'shing!")

@dp.message(F.text == "📥 Video Silkasi")
async def ask_link(msg: Message, state: FSMContext):
    await state.set_state(States.waiting_for_insta_link)
    await msg.answer("Instagram linkini yuboring:")

@dp.message(States.waiting_for_insta_link)
async def dl_video(msg: Message, state: FSMContext):
    status = await msg.answer("⏳ Yuklanmoqda...")
    file_path = f"vid_{msg.from_user.id}.mp4"
    audio_path = f"aud_{msg.from_user.id}.mp3"
    try:
        ydl_opts = {"quiet": True, "outtmpl": file_path, "noplaylist": True}
        def dl():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: return ydl.extract_info(msg.text, download=True)
        info = await asyncio.to_thread(dl)
        await msg.answer_video(FSInputFile(file_path), caption=f"📌 Sarlavha: {info.get('title')}")
        if info.get('description'):
            await msg.answer(f"📝 Matn: {info.get('description')[:4000]}")
            hashtags = re.findall(r"#[^\s#]+", info.get('description'))
            if hashtags: await msg.answer("🏷 Hashtaglar: " + " ".join(hashtags[:20]))
        subprocess.run(["ffmpeg", "-i", file_path, "-vn", "-ab", "192k", audio_path, "-y"], check=True)
        await msg.answer_audio(FSInputFile(audio_path), caption="🎵 Audio format")
        await status.delete()
    except Exception as e: await status.edit_text(f"❌ Xatolik: {e}")
    finally:
        for p in [file_path, audio_path]:
            if os.path.exists(p): os.remove(p)
    await state.clear()

@dp.message(F.text == "✨ Niklar yaratish paneli")
async def ask_nick(msg: Message, state: FSMContext):
    await state.set_state(States.waiting_for_nick)
    await msg.answer("Ism va familiyangizni yuboring:")

@dp.message(States.waiting_for_nick)
async def make_nick(msg: Message, state: FSMContext):
    nicks = ["Alpha", "Beta", "Gamma", "Delta", "Omega", "Cyber", "Ghost", "Neon", "Shadow", "Titan"]
    res = f"{msg.text.replace(' ', '_')}_{random.choice(nicks)}_{random.randint(100, 999999)}"
    await msg.answer(f"✅ Yangi nik: {res}")
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

@dp.message(F.text == "🎮 Oʻyinlar paneli")
async def game(msg: Message):
    choices = ["Tosh", "Qaychi", "Qogoz"]
    bot_choice = random.choice(choices)
    await msg.answer(f"Bot tanladi: {bot_choice}")

@dp.message(F.text == "💰 Valyuta kursi")
async def valyuta(msg: Message):
    await msg.answer("USD: 12,800 UZS\nEUR: 13,900 UZS\nRUB: 140 UZS")

@dp.message(F.text == "🏎 The Bugatti Chiron Heshteg")
async def bugatti(msg: Message):
    txt = ("Here's the information about the Bugatti Chiron:\n\nThe Bugatti Chiron is a mid-engine two-seater sports car designed and developed in Germany by Bugatti Engineering GmbH.\n"
           "CRISGIRLY\n\nThe successor to the Bugatti Veyron, the Chiron was first shown at the Geneva Motor Show on 1 March 2016.\n"
           "The car's design was initially previewed with the Bugatti Vision Gran Turismo concept car unveiled at the 2015 Frankfurt Auto Show.\n"
           "The Chiron was recreated in Lego as 2018's annual Technic sports car. It was released on 1 June 2018 as a 1:8 scale model with 3,600 individual parts.")
    await msg.answer(txt)

@dp.message(F.text == "𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")
async def eslatma(msg: Message):
    txt = ("𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” 𝘇𝗲𝗿𝗼 𝗲𝘀𝗹𝗮𝘁𝗺𝗮 𝗺𝗼’𝗺𝗶𝗻𝗹𝗮𝗿𝗴𝗮 𝗺𝗮𝗻𝗳𝗮𝗮𝘁 𝘆𝗲𝘁𝗸𝗮𝘇𝘂𝗿. (Zarriyot surasi, 55 ) ___\n"
           "𝗦𝘂𝗯𝗵𝗮𝗻𝗮𝗹𝗹𝗼𝗵 - 𝐴𝑙𝑙𝑜ℎ 𝑏𝑎𝑟𝑐ℎ𝑎 𝑛𝑢𝑞𝑠𝑜𝑛𝑙𝑎𝑟𝑑𝑎𝑛 ℎ𝑜𝑙𝑖 𝑣𝑎 𝑝𝑜𝑘𝑑𝑖𝑟...\n"
           "𝗔𝗹𝗵𝗮𝗺𝗱𝘂𝗹𝗶𝗹𝗹𝗮𝗵 - 𝐵𝑎𝑟𝑐ℎ𝑎 𝑚𝑎𝑞𝑡𝑜𝑣 𝐴𝑙𝑙𝑜ℎ𝑔𝑎...\n"
           "𝗔𝗹𝗹𝗼𝗵 𝗔𝗸𝗯𝗮𝗿 - 𝐴𝑙𝑙𝑜ℎ 𝑏𝑢𝑦𝑢𝑘𝑑𝑖𝑟...\n"
           "♻️ 𝗩𝗶𝗱𝗲𝗼𝗻𝗶 𝘂𝗹𝗮𝘀𝗵𝗶𝗻𝗴. 𝗜𝗻𝘀𝗵𝗮 𝗮𝗹𝗹𝗼𝗵 𝗯𝘂𝗻𝗶𝗻𝗴 𝗮𝗷𝗿𝘂 𝘀𝗮𝘃𝗼𝗯𝗶 𝗯𝗼𝗿...\n"
           "#muhammad #allah #islam #namaz #quran")
    await msg.answer(txt)

@dp.message(F.text == "⏱ Vidiyo qõyish vaqti✅🫠")
async def vaqt(msg: Message):
    await msg.answer("Rekga chiqish vaqtlari😊❤️\n6:00✅ 8:00🫵🏻 11:00🫶🏻 16:00🤍 20:00💋 22:00🖤 00:00❤️\n\nManzil: Видео в топ")

@dp.message(F.photo)
async def photo_handler(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"📸 Yangi chek! ID: {msg.from_user.id}")
        await msg.answer("✅ Chek admin tekshiruvi uchun yuborildi.")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
