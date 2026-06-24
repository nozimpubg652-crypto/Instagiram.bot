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

class BotStates(StatesGroup):
    waiting_for_video_link = State()
    waiting_for_chek = State()
    waiting_for_admin_question = State()
    waiting_for_nick_name = State()

# Xatolarni oldini olish uchun yordamchi funksiya
async def safe_edit(message: types.Message, text: str, reply_markup=None):
    try:
        await message.edit_text(text, reply_markup=reply_markup)
    except Exception:
        pass

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

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Asosiy menyu:</b>", reply_markup=get_main_menu())

@dp.callback_query_handler(state="*")
async def all_callbacks(c: types.CallbackQuery, state: FSMContext):
    data = c.data
    back_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Ortga", callback_data="main_menu"))

    if data == "main_menu":
        await safe_edit(c.message, "<b>Asosiy menyu:</b>", reply_markup=get_main_menu())
    
    # Maxsus bo'limlar
    elif data == "video":
        await BotStates.waiting_for_video_link.set()
        await safe_edit(c.message, "🎥 Instagram video havolasini yuboring:", reply_markup=back_kb)
    elif data == "sxema":
        await BotStates.waiting_for_chek.set()
        await safe_edit(c.message, f"🚀 <b>Pulli Sxema</b>\nNarxi: 35,000 so'm\nKarta: <code>{KARTA_RAQAM}</code>\n\nChekni rasm ko'rinishida yuboring.", reply_markup=back_kb)
    elif data == "admin":
        await BotStates.waiting_for_admin_question.set()
        await safe_edit(c.message, "📩 Savolingizni yozing:", reply_markup=back_kb)
    elif data == "nic":
        await BotStates.waiting_for_nick_name.set()
        await safe_edit(c.message, "🆔 Ism/Familiyangizni yozing:", reply_markup=back_kb)
    elif data == "oyin":
        kb = InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton("✊", callback_data="rps_tosh"),
            InlineKeyboardButton("✌️", callback_data="rps_qaychi"),
            InlineKeyboardButton("✋", callback_data="rps_qogoz")
        ).add(InlineKeyboardButton("⬅️ Ortga", callback_data="main_menu"))
        await safe_edit(c.message, "Tanlang:", reply_markup=kb)
    
    # Boshqa barcha tugmalar (faqat matn chiqarish)
    else:
        text = f"Siz tanladingiz: <b>{data.upper()}</b>\n\nBu bo'lim ustida ishlamoqdamiz."
        await safe_edit(c.message, text, reply_markup=back_kb)

    await c.answer()

# --- Holatlar (States) ---
@dp.message_handler(state=BotStates.waiting_for_video_link)
async def get_link(msg: types.Message, state: FSMContext):
    await msg.answer("✅ Qabul qilindi!", reply_markup=get_main_menu())
    await state.finish()

@dp.message_handler(state=BotStates.waiting_for_chek, content_types=['photo'])
async def get_chek(msg: types.Message, state: FSMContext):
    await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=f"To'lov: {msg.from_user.id}")
    await msg.answer("✅ Chek qabul qilindi!", reply_markup=get_main_menu())
    await state.finish()

@dp.message_handler(state=BotStates.waiting_for_admin_question)
async def get_admin_q(msg: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"Savol: {msg.text}\nID: {msg.from_user.id}")
    await msg.answer("✅ Admin ga yuborildi.", reply_markup=get_main_menu())
    await state.finish()

@dp.message_handler(state=BotStates.waiting_for_nick_name)
async def gen_nick(msg: types.Message, state: FSMContext):
    nick = f"Top_{msg.text}_{random.randint(100,999)}"
    await msg.answer(f"🆔 Nik: <code>{nick}</code>", reply_markup=get_main_menu())
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
