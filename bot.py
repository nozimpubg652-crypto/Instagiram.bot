import os
import sqlite3
import yt_dlp
import random
import requests
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# --- SOZLAMALAR ---
API_TOKEN = '8870187278:AAGWhBPnKCkK6MVpdMta7rGOapUAq0FvaTw'
CHANNEL_ID = '@temuzikinsta'
ADMIN_ID = 8639222385
SECURITY_ID = 8639222385
ADMIN_USERNAME = "@roziyev2"
KARTA_RAQAM = "uzur hozir karta bloklangan"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- BAZA ---
conn = sqlite3.connect('bot_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, invited_by INTEGER, referrals INTEGER DEFAULT 0)')
conn.commit()

class FSM(StatesGroup):
    waiting_for_link = State()
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_chek = State()

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📥 Media yukla", "✨ Niklar paneli", "🎮 O'yin", "💰 Valyuta kursi")
    markup.add("📊 Statistika", "🚀 Tekin nakrutka", "📢 Reklama", "💳 Pulli sxema")
    return markup

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id != ADMIN_ID and message.from_user.id != SECURITY_ID:
        cursor.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (message.from_user.id,))
        args = message.get_args()
        if args and args.isdigit():
            referrer = int(args)
            cursor.execute('SELECT id FROM users WHERE id=?', (referrer,))
            if cursor.fetchone() and referrer != message.from_user.id:
                cursor.execute('UPDATE users SET referrals = referrals + 1 WHERE id=?', (referrer,))
                conn.commit()
    
    if not await is_subscribed(message.from_user.id):
        await message.answer("Botdan foydalanish uchun kanalimizga obuna bo'ling!", 
                             reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Obuna bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}")))
    else:
        await message.answer("Xush kelibsiz! Tanlang:", reply_markup=get_main_markup())

@dp.message_handler(text="📥 Media yukla")
async def ask_link(message: types.Message):
    await message.answer("Havolani yuboring:")
    await FSM.waiting_for_link.set()

@dp.message_handler(state=FSM.waiting_for_link)
async def process_media(message: types.Message, state: FSMContext):
    await message.answer("🔍 Yuklanmoqda...")
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'media.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message.text, download=True)
            caption = info.get('description', '')
        
        text_only = ' '.join([w for w in caption.split() if not w.startswith('#')])
        hashtags = ' '.join([w for w in caption.split() if w.startswith('#')])
        
        await message.answer_video(open('media.mp4', 'rb'), caption=f"{text_only}\n\n{hashtags}")
        
        os.system("ffmpeg -i media.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3 -y")
        await message.answer_audio(open('audio.mp3', 'rb'), caption="🎵 Musiqa")
        
        os.remove('media.mp4')
        os.remove('audio.mp3')
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")
    await state.finish()

@dp.message_handler(text="🚀 Tekin nakrutka")
async def nakrutka(message: types.Message):
    cursor.execute('SELECT referrals FROM users WHERE id=?', (message.from_user.id,))
    data = cursor.fetchone()
    ref = data[0] if data else 0
    
    if ref < 10:
        me = await bot.get_me()
        await message.answer(f"10 ta do'st taklif qiling (Hozir: {ref}/10).\nSilka: https://t.me/{me.username}?start={message.from_user.id}")
    else:
        await message.answer("Tabriklaymiz! Mana: https://leofame.com")

# ... (qolgan funksiyalaringizni xuddi shu tarzda saqlab qoling)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
