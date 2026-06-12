import os
import sqlite3
import yt_dlp
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '8870187278:AAEQM8m8c7G1m4qVpyAnWiWqMdD9QvzXKGQ'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class FSM(StatesGroup):
    waiting_for_link = State()
    waiting_for_chek = State()

# --- ASOSIY MENYU ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📥 Link heshteg yukla", "✨ Niklar paneli", "🎮 O'yin", "💰 Valyuta kursi")
    markup.add("📊 Statistika", "🚀 Tekin nakrutka", "📢 Reklama", "💳 Pulli sxema", "📌 Rek heshteglar")
    return markup

# --- O'YINLAR PANEL ---
def get_game_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("✂️ Tosh-Qog'oz-Qaychi", "🔤 So'z o'yini", "🔢 Raqamli o'yin", "🔙 Orqaga")
    return markup

@dp.message_handler(text="🎮 O'yin", state="*")
async def game_menu(message: types.Message):
    await message.answer("O'yin turini tanlang:", reply_markup=get_game_markup())

@dp.message_handler(text="✂️ Tosh-Qog'oz-Qaychi", state="*")
async def game_tosh(message: types.Message):
    choice = random.choice(["Tosh", "Qog'oz", "Qaychi"])
    await message.answer(f"Bot tanladi: {choice}")

@dp.message_handler(text="🔤 So'z o'yini", state="*")
async def game_soz(message: types.Message):
    await message.answer("Bot o'ylagan so'zni toping (Tez orada...)")

@dp.message_handler(text="🔢 Raqamli o'yin", state="*")
async def game_raqam(message: types.Message):
    await message.answer(f"Bot 1 dan 10 gacha raqam o'yladi: {random.randint(1, 10)}")

# --- REK HESHTEGLAR ---
@dp.message_handler(text="📌 Rek heshteglar", state="*")
async def rek_heshteglar(message: types.Message):
    await message.answer("Eng mashhur rek heshteglar:\n#reka #top #trend #video #foryou #fyp")

# --- MEDIA YUKLASH (Aniqlik bilan) ---
@dp.message_handler(text="📥 Link heshteg yukla", state="*")
async def ask_link(message: types.Message):
    await message.answer("Havolani yuboring (Bot matn va heshtegni videodan avtomatik ajratadi):")
    await FSM.waiting_for_link.set()

@dp.message_handler(state=FSM.waiting_for_link)
async def process_media(message: types.Message, state: FSMContext):
    await message.answer("🔍 Yuklanmoqda...")
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'media.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message.text, download=True)
            caption = info.get('description', 'Matn yo\'q')
        
        # Videoni yuborish
        await message.answer_video(open('media.mp4', 'rb'), caption=caption)
        
        # Musiqani yuborish
        os.system("ffmpeg -i media.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3 -y")
        if os.path.exists('audio.mp3'):
            await message.answer_audio(open('audio.mp3', 'rb'))
            os.remove('audio.mp3')
        
        os.remove('media.mp4')
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")
    await state.finish()

# --- BOSHQA FUNKSIYALAR ---
@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await message.answer("Xush kelibsiz!", reply_markup=get_main_markup())

@dp.message_handler(text="🔙 Orqaga", state="*")
async def back(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=get_main_markup())

if __name__ == '__main__':
    # reset_webhook=True - eng muhimi shu!
    executor.start_polling(dp, skip_updates=True, reset_webhook=True)
