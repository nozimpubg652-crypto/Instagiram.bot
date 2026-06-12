import os
import sqlite3
import yt_dlp
import random
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '8870187278:AAGWhBPnKCkK6MVpdMta7rGOapUAq0FvaTw'
CHANNEL_ID = '@temuzikinsta'
ADMIN_ID = 8639222385
KARTA_RAQAM = "8600 1234 5678 9012 (Roziyev)" # Karta raqamingizni kiriting

logging.basicConfig(level=logging.INFO)
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
    waiting_for_chek = State()

# --- FUNKSIYALAR ---
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

# --- PULLI SXEMA (To'lov tizimi) ---
@dp.message_handler(text="💳 Pulli sxema")
async def pulli_sxema(message: types.Message):
    await message.answer(f"💳 To'lov uchun karta: `{KARTA_RAQAM}`\n\nTo'lov qilganingizdan so'ng chek rasmini yuboring!", parse_mode="Markdown")
    await FSM.waiting_for_chek.set()

@dp.message_handler(state=FSM.waiting_for_chek, content_types=['photo'])
async def get_chek(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await bot.send_photo(ADMIN_ID, photo_id, caption=f"Yangi chek! Foydalanuvchi: @{message.from_user.username} ({message.from_user.id})",
                         reply_markup=types.InlineKeyboardMarkup().add(
                             types.InlineKeyboardButton("✅ /ok", callback_data=f"ok_{message.from_user.id}"),
                             types.InlineKeyboardButton("❌ /cancel", callback_data=f"cancel_{message.from_user.id}")
                         ))
    await message.answer("Chek qabul qilindi, admin tasdiqlashini kuting.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('ok_'))
async def approve_pay(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    await bot.send_message(user_id, "To'lovingiz tasdiqlandi! Mana sxema: [BU YERGA SXEMA YOZASIZ: Soat 14:00 da 5 daqiqa kuting...]")
    await call.message.edit_caption("Tasdiqlandi ✅")

@dp.callback_query_handler(lambda c: c.data.startswith('cancel_'))
async def reject_pay(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    await bot.send_message(user_id, "Soxta chek! To'lov tasdiqlanmadi.")
    await call.message.edit_caption("Rad etildi ❌")

# --- QOLGAN BO'LIMLAR ---
@dp.message_handler(text="✨ Niklar paneli")
async def niklar(message: types.Message):
    await message.answer("🔥 *Chiroyli niklar:* \n`『ʟᴏʀᴅ』`\n`⚡️ ᴋɪɴɢ ⚡️`\n`꧁ঔৣ☬✞ ᴋɪɴɢ ✞☬ঔৣ꧂`", parse_mode="Markdown")

@dp.message_handler(text="💰 Valyuta kursi")
async def valyuta(message: types.Message):
    await message.answer("🇺🇸 1 USD = 12,800 UZS\n🇷🇺 1 RUB = 135 UZS")

@dp.message_handler(text="📊 Statistika")
async def stat(message: types.Message):
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    await message.answer(f"👥 Botdagi foydalanuvchilar soni: {count}")

@dp.message_handler(text="📢 Reklama")
async def reklama(message: types.Message):
    await message.answer(f"Reklama va hamkorlik uchun: @roziyev2")

@dp.message_handler(text="🎮 O'yin")
async def game(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add("✂️ Tosh-Qog'oz-Qaychi", "🔢 Raqamli o'yin", "🔙 Asosiy menyu")
    await message.answer("O'yinni tanlang:", reply_markup=markup)

@dp.message_handler(text="✂️ Tosh-Qog'oz-Qaychi")
async def tqg(message: types.Message):
    await message.answer(f"Bot tanladi: {random.choice(['Tosh', 'Qog\'oz', 'Qaychi'])}")

@dp.message_handler(text="🔢 Raqamli o'yin")
async def raqam(message: types.Message):
    await message.answer(f"Bot 1-10 gacha raqam o'yladi: {random.randint(1, 10)}")

@dp.message_handler(text="🔙 Asosiy menyu")
async def back(message: types.Message):
    await message.answer("Menyu:", reply_markup=get_main_markup())

# --- START, MEDIA VA NAKRUTKA (Avvalgi kodingizdagi kabi qoladi) ---
# [Start, Media Yuklash va Nakrutka funksiyalarini shu joyga qo'shib qo'ying]

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
