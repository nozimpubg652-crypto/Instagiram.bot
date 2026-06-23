import random
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- SOZLAMALAR ---
API_TOKEN = "8514343100:AAG70S7e4qlS1B4j0FxRpgppVGMYFvhLYPY"
ADMIN_ID = 8639222385
REQUIRED_CHANNELS = ["@temuzikinsta"]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

USERS_DB = set()

class BotStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_admin_msg = State()
    waiting_for_math_ans = State()

async def check_subscription(user_id: int) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]: return False
        except: return False
    return True

# --- MENYU KONSTRUKTORI ---
def get_super_menu():
    buttons_data = [
        ("🎥 Video Silkasi", "video"), ("⚡ Tekin Nakrutka", "nakrutka"),
        ("🚀 Pulli sxema", "sxema"), ("📩 Admenga xabar", "admin"),
        ("🆔 Nik yaratish", "nic"), ("🎮 O‘yinlar", "oyin"),
        ("💱 Valyuta kursi", "valyuta"), ("🏎 Bugatti Chiron", "bugatti"),
        ("𖣔 Eslatmalar", "eslatma"), ("⏰ Video vaqti", "vaqt"),
        ("📊 Statistika", "stat"), ("🔥 Trend heshteglar", "trend"),
        ("📅 Kunlik maslahat", "maslahat"), ("🌤 Ob-havo", "obhavo"),
        ("📰 Yangiliklar", "yangilik"), ("🧩 Mini-quiz", "quiz"),
        ("🎵 Musiqa tavsiyasi", "music"), ("📢 Reklama", "reklama"),
        ("⭐ VIP reklama", "vip"), ("🎁 Sovg‘a o‘yini", "sovga"),
        ("📚 Kitob tavsiyasi", "kitob"), ("🧠 Bilim testi", "test"),
        ("🎬 Kino tavsiyalari", "kino"), ("🍔 Retsept paneli", "retsept"),
        ("🧮 Matematika o‘yini", "math"), ("🎲 Random generator", "random"),
        ("📖 Hadis paneli", "hadis"), ("🧘 Zikr paneli", "zikr"),
        ("🛠 Dev tools", "dev"), ("🕹 Arcade o‘yin", "arcade"),
        ("📜 Qur’on oyatlari", "quron"), ("🧾 Tarixiy faktlar", "tarix"),
        ("⚽ Sport yangiliklari", "sport"), ("🚀 Texno yangiliklar", "tech"),
        ("🎨 Meme generator", "meme"), ("🧑‍🎓 Inglizcha so‘zlar", "english"),
        ("🎤 Sitata paneli", "sitata"), ("🧑‍🍳 Oshpazlik", "oshpaz"),
        ("🎯 Maqsadlar", "maqsad")
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    row = []
    for text, data in buttons_data:
        row.append(InlineKeyboardButton(text=text, callback_data=data))
        if len(row) == 2:
            keyboard.inline_keyboard.append(row)
            row = []
    if row:
        keyboard.inline_keyboard.append(row)
    return keyboard

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    USERS_DB.add(message.from_user.id)
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Obuna bo‘lish", url="https://t.me/temuzikinsta")],
            [InlineKeyboardButton(text="✅ Tekshirdim", callback_data="check_sub")]
        ])
        await message.answer("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=keyboard)
    else:
        await message.answer("🤖 **Super Menyuga xush kelibsiz!**", reply_markup=get_super_menu(), parse_mode="Markdown")

@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback_query: types.CallbackQuery):
    if await check_subscription(callback_query.from_user.id):
        await callback_query.message.answer("✅ Obuna tasdiqlandi!", reply_markup=get_super_menu())
    else:
        await callback_query.answer("❌ Hali obuna bo‘lmadingiz!", show_alert=True)

# 1. NIK YARATISH
@dp.callback_query(F.data == "nic")
async def start_nickname(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("🆔 Ismingizni yuboring:")
    await state.set_state(BotStates.waiting_for_name)

@dp.message(BotStates.waiting_for_name)
async def generate_nickname(message: types.Message, state: FSMContext):
    name = message.text.strip()
    styles = [f"✨ {name} ✨", f"🔥 『{name}』 🔥", f"⚡ {name}_King ⚡"]
    await message.answer("🎭 **Siz uchun niklar:**\n\n" + "\n".join(styles), reply_markup=get_super_menu(), parse_mode="Markdown")
    await state.clear()

# 2. ADMENGA XABAR
@dp.callback_query(F.data == "admin")
async def admin_message_start(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("📩 Xabaringizni yozing:")
    await state.set_state(BotStates.waiting_for_admin_msg)

@dp.message(BotStates.waiting_for_admin_msg)
async def admin_message_send(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📬 **Xabar:**\n👤 @{message.from_user.username}\n📝 {message.text}")
    await message.answer("✅ Yuborildi!", reply_markup=get_super_menu())
    await state.clear()

# 3. STATIK TUGMALAR
@dp.callback_query()
async def process_all_buttons(callback_query: types.CallbackQuery):
    responses = {
        "video": "🎥 Havolani yuboring...",
        "nakrutka": "⚡ 5 ta do‘stingizni taklif qiling.",
        "sxema": "🚀 Pulli sxema: 35 000 so‘m.",
        "oyin": "🎮 Emojilardan (✊, ✌️, ✋) birini yuboring.",
        "valyuta": "💱 1 USD = 12 800 so‘m.",
        "bugatti": "🏎 Bugatti Chiron tezligi 420 km/s.",
        "eslatma": "𖣔 Subhanalloh, Alhamdulillah, Allohu Akbar.",
        "vaqt": "⏰ 08:00, 11:00, 20:00, 22:00.",
        "stat": f"📊 Foydalanuvchilar: {len(USERS_DB)} ta.",
        "trend": "#viral #explore #fyp",
        "maslahat": "📅 Harakat qiling!",
        "obhavo": "🌤 Toshkent: +28°C.",
        "yangilik": "📰 AI rivojlanmoqda.",
        "quiz": "🧩 P: Toshkent.",
        "music": "🎵 Sevara Nazarkhan — 'Yor-yor'.",
        "reklama": "📢 Reklama uchun @roziyev2.",
        "vip": "⭐ VIP Reklama mavjud.",
        "sovga": "🎁 O‘yinlarimizda qatnashing!",
        "kitob": "📚 'O‘tkan kunlar'.",
        "test": "🧠 Yupiter eng katta sayyora.",
        "kino": "🎬 'Inception' filmini ko‘ring.",
        "retsept": "🍔 Tovuqli sendvich retsepti.",
        "random": "🎲 Omadli raqam: 77.",
        "hadis": "📖 'Amallar niyatlarga ko‘ra...'",
        "zikr": "🧘 100 marta 'Subhanalloh'.",
        "dev": "🛠 Python Aiogram.",
        "arcade": "🕹 Tosh-Qaychi-Qog‘oz.",
        "quron": "📜 'Har qiyinchilik bilan...'",
        "tarix": "🧾 Amir Temur - buyuk sarkarda.",
        "sport": "⚽ Sport yangiliklari mavjud.",
        "tech": "🚀 iPhone 17 mish-mishlari.",
        "meme": "🎨 Meme-world.com.",
        "english": "🧑‍🎓 Success - Muvaffaqiyat.",
        "sitata": "🎤 Hayot — bu harakat.",
        "oshpaz": "🧑‍🍳 Palov retsepti.",
        "maqsad": "🎯 Maqsadingizni yozing."
    }
    
    if callback_query.data in responses:
        await callback_query.message.answer(responses[callback_query.data], reply_markup=get_super_menu(), parse_mode="Markdown")
    await callback_query.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) shu 
