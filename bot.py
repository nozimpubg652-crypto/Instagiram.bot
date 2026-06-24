from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random

API_TOKEN = "8514343100:AAG70S7e4qlS1B4j0FxRpgppVGMYFvhLYPY"
ADMIN_ID = 8639222385
KARTA_RAQAM = "9860 1666 5489 5563"

storage = MemoryStorage()
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

# Xotira
USED_NICKS = set()
added_counts = {}
video_data = {}

class BotStates(StatesGroup):
    waiting_for_video_link = State()
    waiting_for_chek = State()
    waiting_for_admin_question = State()
    waiting_for_nick_name = State()

REQUIRED_CHANNELS = ["@temuzikinsta"]

async def check_subscription(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]: return False
        except: return False
    return True

# --- Menyuni yaratish ---
def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        ("🎥 Video Silkasi", "video"), ("⚡ Tekin Nakrutka", "nakrutka"),
        ("🚀 Pulli sxema", "sxema"), ("📩 Admenga savol", "admin"),
        ("🆔 Nik yaratish", "nic"), ("🎮 O‘yinlar", "oyin"),
        ("💱 Valyuta kursi", "valyuta"), ("🏎 Bugatti Chiron", "bugatti"),
        ("𖣔 Eslatmalar", "eslatma"), ("⏰ Video vaqti", "vaqt"),
        ("📊 Statistika", "stat"), ("🔥 Trend heshteglar", "trend"),
        ("📅 Kunlik maslahat", "maslahat"), ("🌤 Ob-havo", "obhavo"),
        ("📰 Yangiliklar", "yangilik"), ("🧩 Mini-quiz", "quiz"),
        ("🎵 Musiqa", "music"), ("📢 Reklama", "reklama"),
        ("⭐ VIP reklama", "vip"), ("🎁 Sovg‘a o‘yini", "sovga"),
        ("📚 Kitoblar", "kitob"), ("🧠 Bilim testi", "test"),
        ("🎬 Kinolar", "kino"), ("🍔 Retseptlar", "retsept"),
        ("🧮 Matematika", "math"), ("🎲 Random", "random"),
        ("📖 Hadislar", "hadis"), ("🧘 Zikrlar", "zikr"),
        ("🛠 Developer", "dev"), ("🕹 Arcade", "arcade"),
        ("📜 Qur’on", "quron"), ("🧾 Tarix", "tarix"),
        ("⚽ Sport", "sport"), ("🚀 Texnologiya", "tech"),
        ("🎨 Meme", "meme"), ("🧑‍🎓 Inglizcha", "english"),
        ("🎤 Sitatalar", "sitata"), ("🧑‍🍳 Oshpazlik", "oshpaz"),
        ("🎯 Maqsadlar", "maqsad")
    ]
    for text, callback in buttons:
        markup.insert(InlineKeyboardButton(text=text, callback_data=callback))
    return markup

# --- Start ---
@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    if not await check_subscription(message.from_user.id):
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("📢 Obuna bo‘lish", url="https://t.me/temuzikinsta"),
                                      InlineKeyboardButton("✅ Tekshirdim", callback_data="check_sub"))
        await message.answer("❗ Botdan foydalanish uchun obuna bo‘ling:", reply_markup=kb)
    else:
        await message.answer("<b>Super menyu:</b>", reply_markup=get_main_menu())

# --- Callbacklar ---
@dp.callback_query_handler(lambda c: c.data == "check_sub", state="*")
async def check_sub(c: types.CallbackQuery):
    if await check_subscription(c.from_user.id):
        await c.message.edit_text("✅ Obuna tasdiqlandi!", reply_markup=get_main_menu())
    else:
        await c.answer("❌ Hali obuna bo‘lmadingiz!", show_alert=True)

@dp.callback_query_handler(lambda c: True, state="*")
async def all_callbacks(c: types.CallbackQuery, state: FSMContext):
    data = c.data
    
    # Maxsus holatlar
    if data == "video":
        await BotStates.waiting_for_video_link.set()
        await c.message.answer("🎥 Instagram video havolasini yuboring:")
    elif data == "sxema":
        await c.message.answer(f"🚀 <b>Pulli Sxema</b>\nNarxi: 35,000 so'm\nKarta: <code>{KARTA_RAQAM}</code>\n\nChekni yuboring.")
        await BotStates.waiting_for_chek.set()
    elif data == "admin":
        await BotStates.waiting_for_admin_question.set()
        await c.message.answer("📩 Savolingizni yozing:")
    elif data == "nic":
        await BotStates.waiting_for_nick_name.set()
        await c.message.answer("🆔 Ism/Familiyangizni yozing:")
    elif data == "nakrutka":
        await c.message.answer("⚡ Shart: @temuzikinsta ga 5 ta odam qo'shing.")
    elif data == "oyin":
        kb = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton("✊", callback_data="rps_tosh"),
                                                   InlineKeyboardButton("✌️", callback_data="rps_qaychi"),
                                                   InlineKeyboardButton("✋", callback_data="rps_qogoz"))
        await c.message.answer("Tanlang:", reply_markup=kb)
    elif data.startswith("rps_"):
        user_choice = data.split("_")[1]
        bot_choice = random.choice(["tosh", "qaychi", "qogoz"])
        await c.message.answer(f"Siz: {user_choice}\nBot: {bot_choice}\nResult: {'Teng' if user_choice == bot_choice else 'Yutdingiz'}")
    elif data == "random":
        await c.message.answer(f"🎲 Tasodifiy son: {random.randint(1, 100)}")
    
    # Barcha qolgan tugmalar
    else:
        responses = {
            "valyuta": "💱 1 USD = 12,850 so'm.",
            "bugatti": "🏎 Bugatti Chiron - 1,500 ot kuchi.",
            "eslatma": "𖣔 Bismillahir rohmanir rohiym.",
            "vaqt": "⏰ Eng yaxshi vaqtlar: 11:00, 16:00, 20:00.",
            "stat": "📊 Bot statistikasi: 1,500+ obunachi.",
            "trend": "🔥 Trend heshteglar: #rek #top #uzb #instagram",
            "maslahat": "📅 Bugungi maslahat: Harakatdan to‘xtamang!",
            "obhavo": "🌤 Toshkent: 34°C, Quyoshli.",
            "yangilik": "📰 Yangiliklar: Botimiz yangilandi!",
            "quiz": "🧩 Savol: O'zbekiston poytaxti qaysi?",
            "music": "🎵 Musiqa: Sevara - Yor-yor.",
            "reklama": "📢 Reklama uchun admin: @roziyev2.",
            "vip": "⭐ VIP reklama: 50,000 so'm.",
            "sovga": "🎁 Sovg'a o'yini: Tez orada boshlanadi.",
            "kitob": "📚 Paulo Coelho - Alkimyogar.",
            "test": "🧠 Bilim testi yuklanmoqda...",
            "kino": "🎬 Kino: Inception (2010).",
            "retsept": "🍔 Palov retsepti: Guruch, go'sht, sabzi.",
            "math": "🧮 Matematika: 2+2=4.",
            "hadis": "📖 Hadis: “Eng yaxshi odam – foydali bo'lganidir.”",
            "zikr": "🧘 Subhanallah, Alhamdulillah, Allohu Akbar.",
            "dev": "🛠 Developer: @roziyev2.",
            "arcade": "🕹 Arcade o'yinlar bo'limi.",
            "quron": "📜 Qur'on: Niso surasi.",
            "tarix": "🧾 1969-yil: Inson oyga chiqdi.",
            "sport": "⚽ Sport: O'zbekiston terma jamoasi - G'alaba!",
            "tech": "🚀 Texnologiya: 5G tarmog'i.",
            "meme": "🎨 Memlar bo'limi tez kunda!",
            "english": "🧑‍🎓 Inglizcha: 'Believe in yourself'.",
            "sitata": "🎤 Harakatda barakat.",
            "oshpaz": "🧑‍🍳 Oshpazlik sirlari.",
            "maqsad": "🎯 Maqsadingizni yozing va erishing!"
        }
        await c.message.answer(responses.get(data, "Bo'lim ishga tushirilmoqda..."))
    
    await c.answer()

# --- Holatlar (States) ---
@dp.message_handler(state=BotStates.waiting_for_video_link)
async def get_link(msg: types.Message, state: FSMContext):
    await msg.answer("✅ Qabul qilindi! Trend heshteglar: #viral #rek")
    await state.finish()

@dp.message_handler(state=BotStates.waiting_for_chek, content_types=['photo'])
async def get_chek(msg: types.Message, state: FSMContext):
    await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=f"To'lov: {msg.from_user.id}")
    await msg.answer("✅ Chek qabul qilindi!")
    await state.finish()

@dp.message_handler(state=BotStates.waiting_for_admin_question)
async def get_admin_q(msg: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"Savol: {msg.text}\nID: {msg.from_user.id}")
    await msg.answer("✅ Admin ga yuborildi.")
    await state.finish()

@dp.message_handler(state=BotStates.waiting_for_nick_name)
async def gen_nick(msg: types.Message, state: FSMContext):
    nick = f"Top_{msg.text}_{random.randint(100,999)}"
    await msg.answer(f"🆔 Nik: <code>{nick}</code>")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
