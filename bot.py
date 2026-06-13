import os
import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8639222385
CHANNEL_ID = "@temuzikinsta" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class BotStates(StatesGroup):
    savol_yuborish = State()
    ism_familiya = State()
    chek_kutish = State()
    instagram_link = State()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Salom! Men ishlayapman.", reply_markup=get_main_menu())

@dp.message(F.text == "📥 Video Silkasi orqali heshteg olish🥶")
async def ask_insta_link(message: types.Message, state: FSMContext):
    await message.answer("Video havolasini yuboring, men sizga mos heshteglarni tayyorlab beraman:")
    await state.set_state(BotStates.instagram_link)

@dp.message(BotStates.instagram_link)
async def process_insta_link(message: types.Message, state: FSMContext):
    await message.answer(f"✅ Tahlil qilindi!\n\n🚀 **Instagramda TOPga chiqish bo'yicha qo'llanma**\n• **Eng yaxshi vaqtlar:** 6:00, 11:00, 16:00, 20:00, 22:00.\n• **Algoritmni aldaydigan heshteglar:** #reels #top #uzb #trend #foryou #viral #instagram\n\nSizga mos heshteglar: #top #reels #trend #uzb")
    await state.clear()

def get_main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📥 Video Silkasi orqali heshteg olish🥶")],
        [KeyboardButton(text="💳 Pulli sxema paneli"), KeyboardButton(text="📩 Admenga savol yulash")],
        [KeyboardButton(text="🏎 The Bugatti Chiron Heshteg"), KeyboardButton(text="𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")],
        [KeyboardButton(text="⏱ Vidiyo qõyish vaqti✅🫠"), KeyboardButton(text="✨ Niklar yaratish paneli")],
        [KeyboardButton(text="🎮 Oʻyinlar paneli"), KeyboardButton(text="💰 Valyuta kursi")],
        [KeyboardButton(text="🚀 Tekin nakrutka paneli"), KeyboardButton(text="📌 Rek heshteglar")]
    ], resize_keyboard=True)

@dp.message(F.text == "💳 Pulli sxema paneli")
async def pulik_sxema(message: types.Message, state: FSMContext):
    text = ("🚀 **TOP SXEMA SOTILADI!** 🚀\n"
            "Videolaringizni trendga chiqarish uchun 100% ishlaydigan usul.\n"
            "💰 Narx: 35 000 so'm. \nKarta raqam: [Karta ma'lumotlari]\n\n"
            "To'lov qilib chek rasmini yuboring!")
    await message.answer(text)
    await state.set_state(BotStates.chek_kutish)

@dp.message(BotStates.chek_kutish, F.photo)
async def chek_qabul(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"accept_{message.from_user.id}")]])
    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"Yangi to'lov! ID: {message.from_user.id}", reply_markup=markup)
    await message.answer("Chek yuborildi, admin tekshirmoqda.")
    await state.clear()

@dp.message(F.text == "🏎 The Bugatti Chiron Heshteg")
async def bugatti_info(message: types.Message):
    await message.answer("The Bugatti Chiron is a mid-engine two-seater sports car... (The successor to the Bugatti Veyron)")

@dp.message(F.text == "𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")
async def eslatma(message: types.Message):
    await message.answer("𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” 𝘇𝗲𝗿𝗼 𝗲𝘀𝗹𝗮𝘁𝗺𝗮 𝗺𝗼’𝗺𝗶𝗻𝗹𝗮𝗿𝗴𝗮 𝗺𝗮𝗻𝗳𝗮𝗮𝘁 𝘆𝗲𝘁𝗸𝗮𝘇𝘂𝗿. #musulmon #islam")

@dp.message(F.text == "🎮 Oʻyinlar paneli")
async def game_start(message: types.Message):
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Tosh"), KeyboardButton(text="Qaychi"), KeyboardButton(text="Qog'oz")]], resize_keyboard=True)
    await message.answer("Tanlang:", reply_markup=markup)

@dp.message(F.text.in_(["Tosh", "Qaychi", "Qog'oz"]))
async def play_game(message: types.Message):
    bot_choice = random.choice(["Tosh", "Qaychi", "Qog'oz"])
    await message.answer(f"Bot: {bot_choice}")

@dp.message(F.text == "📩 Admenga savol yulash")
async def ask_admin(message: types.Message, state: FSMContext):
    await message.answer("Savolingizni yozing:")
    await state.set_state(BotStates.savol_yuborish)

@dp.message(BotStates.savol_yuborish)
async def forward_ask(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"Savol: {message.text}")
    await message.answer("Yuborildi!")
    await state.clear()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
