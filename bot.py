import os
import yt_dlp
import random
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '8870187278:AAEQM8m8c7G1m4qVpyAnWiWqMdD9QvzXKGQ'
CHANNEL_ID = '@temuzikinsta' # KANALINGIZNI SHU YERGA YOZING

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class FSM(StatesGroup):
    waiting_for_link = State()

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def get_sub_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}"))
    markup.add(types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub"))
    return markup

def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📥 Link heshteg yukla", "✨ Niklar paneli", "🎮 O'yin", "💰 Valyuta kursi")
    markup.add("📊 Statistika", "🚀 Tekin nakrutka", "📢 Reklama", "💳 Pulli sxema", "📌 Rek heshteglar")
    return markup

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    if await check_sub(message.from_user.id):
        await message.answer("Xush kelibsiz!", reply_markup=get_main_markup())
    else:
        await message.answer("Botdan foydalanish uchun kanalimizga obuna bo'ling:", reply_markup=get_sub_markup())

@dp.callback_query_handler(text="check_sub")
async def verify_sub(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.delete()
        await call.message.answer("Rahmat! Obuna tasdiqlandi. Asosiy menyu:", reply_markup=get_main_markup())
    else:
        await call.answer("Siz hali obuna bo'lmadingiz! Iltimos, kanalga kiring.", show_alert=True)

# MEDIA YUKLASH QISMI (To'ldirildi)
@dp.message_handler(text="📥 Link heshteg yukla", state="*")
async def ask_link(message: types.Message):
    if await check_sub(message.from_user.id):
        await message.answer("Havolani yuboring:")
        await FSM.waiting_for_link.set()
    else:
        await message.answer("Avval obuna bo'ling!", reply_markup=get_sub_markup())

@dp.message_handler(state=FSM.waiting_for_link, content_types=['text'])
async def process_media(message: types.Message, state: FSMContext):
    if not message.text.startswith("http"):
        await message.answer("Bu havola emas! Iltimos, to'g'ri havola yuboring.")
        return
    
    await message.answer("🔍 Yuklanmoqda... Iltimos kuting.")
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'media.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message.text, download=True)
            caption = info.get('description', 'Matn topilmadi')
        
        await message.answer_video(open('media.mp4', 'rb'), caption=caption[:1000])
        
        os.system("ffmpeg -i media.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3 -y")
        if os.path.exists('audio.mp3'):
            await message.answer_audio(open('audio.mp3', 'rb'))
            os.remove('audio.mp3')
        
        os.remove('media.mp4')
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")
    finally:
        await state.finish()

# O'yinlar va boshqalar
@dp.message_handler(text="🎮 O'yin", state="*")
async def game_menu(message: types.Message):
    if await check_sub(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("✂️ Tosh-Qog'oz-Qaychi", "🔤 So'z o'yini", "🔢 Raqamli o'yin", "🔙 Orqaga")
        await message.answer("O'yin turini tanlang:", reply_markup=markup)
    else:
        await message.answer("Avval obuna bo'ling!", reply_markup=get_sub_markup())

@dp.message_handler(text="🔙 Orqaga", state="*")
async def back(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Asosiy menyu:", reply_markup=get_main_markup())

async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
