import os
import sqlite3
import yt_dlp
import random
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# --- SOZLAMALAR ---
API_TOKEN = '8870187278:AAGWhBPnKCkK6MVpdMta7rGOapUAq0FvaTw'
CHANNEL_ID = '@temuzikinsta'
ADMIN_ID = 8639222385
KARTA_RAQAM = "9860XXXXXXXXXXXX"
SXEMA_NARXI = "15 000 so'm"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- BAZA ---
conn = sqlite3.connect('bot_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, referrals INTEGER DEFAULT 0)')
conn.commit()

class FSM(StatesGroup):
    waiting_for_link = State()
    waiting_for_lang = State()
    waiting_for_chek = State()

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📥 Link heshteg yukla", "✨ Niklar paneli", "🎮 O'yin", "💰 Valyuta kursi")
    markup.add("📊 Statistika", "🚀 Tekin nakrutka", "📢 Reklama", "💳 Pulli sxema")
    return markup

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    if not await is_subscribed(message.from_user.id):
        await message.answer("Obuna bo'ling!", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Obuna bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}")))
    else:
        await message.answer("Xush kelibsiz!", reply_markup=get_main_markup())

# --- 1. LINK HESHTEG YUKLA ---
@dp.message_handler(text="📥 Link heshteg yukla", state="*")
async def lang_menu(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🇯🇵 Yapon", "🇦🇪 Arab", "🇺🇿 O'zbek", "🇷🇺 Rus")
    await message.answer("Tilni tanlang:", reply_markup=markup)
    await FSM.waiting_for_lang.set()

@dp.message_handler(state=FSM.waiting_for_lang)
async def choose_lang(message: types.Message, state: FSMContext):
    lang_data = {
        "🇯🇵 Yapon": ("🇯🇵\n最高にかっこいい車！(Eng zo'r mashina!)", "#reka #top #japan #car"),
        "🇦🇪 Arab": ("🇦🇪\nسيارة قوية جداً! (Juda kuchli mashina!)", "#reka #top #arab #car"),
        "🇺🇿 O'zbek": ("🇺🇿\nEng zo'r va tezkor mashina!", "#reka #top #uzb #car"),
        "🇷🇺 Rus": ("🇷🇺\nСамая быстрая машина! (Eng tezkor mashina!)", "#reka #top #rus #car")
    }
    if message.text in lang_data:
        await state.update_data(text=lang_data[message.text][0], tags=lang_data[message.text][1])
        await message.answer("Endi havolani yuboring:", reply_markup=types.ReplyKeyboardRemove())
        await FSM.waiting_for_link.set()
    else: await message.answer("Iltimos, tugmalardan birini bosing.")

@dp.message_handler(state=FSM.waiting_for_link)
async def process_media(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("🔍 Yuklanmoqda...")
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'media.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.extract_info(message.text, download=True)
        caption = f"{data['text']}\n\n{data['tags']}"
        await message.answer_video(open('media.mp4', 'rb'), caption=caption)
        os.system("ffmpeg -i media.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3 -y")
        await message.answer_audio(open('audio.mp3', 'rb'), caption=f"🎵 Musiqa\n\n{data['tags']}")
        os.remove('media.mp4'); os.remove('audio.mp3')
    except Exception as e: await message.answer(f"❌ Xatolik: {e}")
    await state.finish()
    await message.answer("Tanlang:", reply_markup=get_main_markup())

# --- 2. QOLGAN TUGMALAR ---
@dp.message_handler(text="✨ Niklar paneli", state="*")
async def niklar(message: types.Message, state: FSMContext): await message.answer("✨ Niklar paneli: Bu yerda siz chiroyli niklar topishingiz mumkin.")

@dp.message_handler(text="🎮 O'yin", state="*")
async def oyin(message: types.Message, state: FSMContext): await message.answer("🎮 O'yinlar: Tasodifiy raqam yoki so'z o'yinlari tez orada qo'shiladi!")

@dp.message_handler(text="💰 Valyuta kursi", state="*")
async def valyuta(message: types.Message, state: FSMContext): await message.answer("💰 Hozirgi dollar kursi: 12,850 so'm.")

@dp.message_handler(text="📊 Statistika", state="*")
async def statistika(message: types.Message, state: FSMContext): 
    cursor.execute('SELECT count(*) FROM users')
    count = cursor.fetchone()[0]
    await message.answer(f"📊 Bot foydalanuvchilari soni: {count} ta.")

@dp.message_handler(text="📢 Reklama", state="*")
async def reklama(message: types.Message, state: FSMContext): await message.answer("📢 Reklama joylashtirish uchun admin: @roziyev2")

@dp.message_handler(text="🚀 Tekin nakrutka", state="*")
async def nakrutka(message: types.Message, state: FSMContext): await message.answer("10 ta do'st taklif qiling va bepul xizmatdan foydalaning.")

# --- 3. PULLI SXEMA ---
@dp.message_handler(text="💳 Pulli sxema", state="*")
async def sxema_start(message: types.Message):
    await message.answer(f"💳 Narxi: {SXEMA_NARXI}\nKarta: {KARTA_RAQAM}\nAdmin: @roziyev2\nChekni rasm ko'rinishida yuboring!")
    await FSM.waiting_for_chek.set()

@dp.message_handler(content_types=['photo'], state=FSM.waiting_for_chek)
async def get_chek(message: types.Message, state: FSMContext):
    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"Foydalanuvchi: {message.from_user.id}",
                         reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"ok_{message.from_user.id}")))
    await message.answer("⏳ Admin tasdiqlashini kuting.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('ok_'))
async def approve_chek(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    reka_info = "🚀 REKA SIRLARI: Vaqt (18:00-21:00), Kun (Juma-Yakshanba), Sifat (3 soniya)."
    await bot.send_message(user_id, f"✅ To'lov tasdiqlandi!\n\n{reka_info}")
    await call.message.edit_caption("✅ Tasdiqlandi!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, reset_webhook=True)
