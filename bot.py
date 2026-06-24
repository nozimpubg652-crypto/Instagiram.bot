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

# Ma'lumotlarni saqlash
video_data = {}
added_counts = {}

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

# --- Yagona Menyuni Chiroyli Yaratish ---
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

# --- Barcha Tugmalarni Boshqarish (Dispatcher) ---
@dp.callback_query_handler(lambda c: True, state="*")
async def process_all_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    user_id = callback_query.from_user.id

    # 1. Maxsus amallar (Video, Sxema, Admin, etc)
    if data == "video":
        await BotStates.waiting_for_video_link.set()
        await callback_query.message.answer("🎥 Instagram video havolasini yuboring:")
    
    elif data == "sxema":
        await callback_query.message.answer(
            f"🚀 <b>Pulli Sxema</b>\nNarxi: 35,000 so'm\nKarta: <code>{KARTA_RAQAM}</code>\n\nTo'lov qilib chekni yuboring, admin tekshiradi."
        )
    
    elif data == "admin":
        await BotStates.waiting_for_admin_question.set()
        await callback_query.message.answer("📩 Savolingizni yozing:")

    elif data == "nic":
        await BotStates.waiting_for_nick_name.set()
        await callback_query.message.answer("🆔 Ismingizni yozing:")

    # 2. Oddiy ma'lumot beruvchi tugmalar (Dictionary orqali)
    else:
        responses = {
            "stat": "📊 Bot statistikasi: 1,500+ obunachi.",
            "trend": "🔥 Trend heshteglar: #rek #top #uzb #instagram",
            "maslahat": "📅 Bugungi maslahat: Harakatdan to‘xtamang!",
            "obhavo": "🌤 Toshkent: 34°C, Quyoshli.",
            "valyuta": "💱 1 USD = 12,850 so'm.",
            "bugatti": "🏎 Bugatti Chiron - 1,500 ot kuchi.",
            "eslatma": "𖣔 Alhamdulillah - Barcha maqtov Allohga.",
            "vaqt": "⏰ Rekka chiqish uchun eng yaxshi vaqtlar: 11:00, 16:00, 20:00.",
            "yangiliklar": "📰 Hozircha yangiliklar yo'q.",
            "quiz": "🧩 Savol: O'zbekiston poytaxti?",
            "music": "🎵 Musiqa: Sevara - Yor-yor.",
            "reklama": "📢 Reklama uchun admin bilan bog'laning.",
            "vip": "⭐ VIP reklama xizmati.",
            "sovga": "🎁 Sovg'a o'yini yaqinda boshlanadi.",
            "kitob": "📚 Paulo Coelho - Alkimyogar.",
            "test": "🧠 Bilim testi yuklanmoqda...",
            "kino": "🎬 Kino: Inception.",
            "retsept": "🍔 Palov retsepti...",
            "math": "🧮 2+2 = 4.",
            "random": f"🎲 Tasodifiy son: {random.randint(1,100)}.",
            "hadis": "📖 Hadis: Eng yaxshi odam foydasi tegadiganidir.",
            "zikr": "🧘 Subhanallah, Alhamdulillah, Allohu Akbar.",
            "dev": "🛠 Developer: @roziyev2.",
            "arcade": "🕹 O'yinlar bo'limi.",
            "quron": "📜 Qur'on oyati: Niso surasi.",
            "tarix": "🧾 1969-yil: Oyga inson chiqdi.",
            "sport": "⚽ O'zbekiston terma jamoasi - G'alaba!",
            "tech": "🚀 5G texnologiyasi rivojlanmoqda.",
            "meme": "🎨 Meme generator: Tez orada...",
            "english": "🧑‍🎓 Perseverance - Matonat.",
            "sitata": "🎤 Harakatda barakat.",
            "oshpaz": "🧑‍🍳 Oshpazlik bo'limi.",
            "maqsad": "🎯 Maqsadingizni yozing."
        }
        await callback_query.message.answer(responses.get(data, "Bo'lim ishga tushirilmoqda..."))

    await callback_query.answer()

# --- START VA QOLGAN QISMLAR ---
@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton("📢 Obuna bo‘lish", url="https://t.me/temuzikinsta"))
        keyboard.add(InlineKeyboardButton("✅ Tekshirdim", callback_data="check_sub"))
        await message.answer("❗ Botdan foydalanish uchun obuna bo‘ling:", reply_markup=keyboard)
    else:
        # Har safar yangi toza menyu chiqarish
        await message.answer("<b>Super menyu:</b>", reply_markup=get_main_menu())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
