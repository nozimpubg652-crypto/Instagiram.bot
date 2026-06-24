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

@dp.callback_query_handler(lambda c: True, state="*")
async def all_callbacks(c: types.CallbackQuery, state: FSMContext):
    data = c.data
    
    # Orqaga qaytish uchun yordamchi tugma
    back_markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_menu"))

    if data == "back_to_menu":
        await c.message.edit_text("<b>Asosiy menyu:</b>", reply_markup=get_main_menu())
    
    elif data == "video":
        await BotStates.waiting_for_video_link.set()
        await c.message.edit_text("🎥 Instagram video havolasini yuboring:", reply_markup=back_markup)
    elif data == "sxema":
        await BotStates.waiting_for_chek.set()
        await c.message.edit_text(f"🚀 <b>Pulli Sxema</b>\nNarxi: 35,000 so'm\nKarta: <code>{KARTA_RAQAM}</code>\n\nChekni rasm ko'rinishida yuboring.", reply_markup=back_markup)
    elif data == "admin":
        await BotStates.waiting_for_admin_question.set()
        await c.message.edit_text("📩 Savolingizni yozing:", reply_markup=back_markup)
    elif data == "nic":
        await BotStates.waiting_for_nick_name.set()
        await c.message.edit_text("🆔 Ism/Familiyangizni yozing:", reply_markup=back_markup)
    else:
        # Barcha ma'lumot tugmalari
        responses = {
            "valyuta": "💱 1 USD = 12,850 so'm.", "bugatti": "🏎 Bugatti Chiron - 1,500 ot kuchi.",
            "stat": "📊 Bot statistikasi: 1,500+ obunachi.", "trend": "🔥 Trend heshteglar: #rek #top",
            "obhavo": "🌤 Toshkent: 34°C, Quyoshli.", "random": f"🎲 Tasodifiy son: {random.randint(1,100)}."
        }
        text = responses.get(data, "Tanlangan bo'lim: " + data)
        await c.message.edit_text(text, reply_markup=back_markup)
    
    await c.answer()

# --- Holatlar (States) ---
@dp.message_handler(state=BotStates.waiting_for_video_link)
async def get_link(msg: types.Message, state: FSMContext):
    await msg.answer("✅ Qabul qilindi! Trend heshteglar: #viral #rek", reply_markup=get_main_menu())
    await state.finish()

@dp.message_handler(state=BotStates.waiting_for_chek, content_types=['photo'])
async def get_chek(msg: types.Message, state: FSMContext):
    await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=f"To'lov keldi: {msg.from_user.id}")
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
