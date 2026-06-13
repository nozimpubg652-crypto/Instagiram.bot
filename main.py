import os
import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Konfiguratsiya
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8639222385
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Menyular
def get_main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📥 Video Silkasi orqali heshteg olish🥶")],
        [KeyboardButton(text="💳 Pulli sxema paneli"), KeyboardButton(text="📩 Admenga savol yulash")],
        [KeyboardButton(text="🏎 The Bugatti Chiron Heshteg"), KeyboardButton(text="𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")],
        [KeyboardButton(text="⏱ Vidiyo qõyish vaqti✅🫠"), KeyboardButton(text="✨ Niklar yaratish paneli")],
        [KeyboardButton(text="🎮 Oʻyinlar paneli"), KeyboardButton(text="💰 Valyuta kursi")],
        [KeyboardButton(text="🚀 Tekin nakrutka paneli"), KeyboardButton(text="📌 Rek heshteglar")]
    ], resize_keyboard=True)

# Handlerlar
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Salom! Men ishlayapman.", reply_markup=get_main_menu())

@dp.message(F.text == "📥 Video Silkasi orqali heshteg olish🥶")
async def ask_insta(message: Message):
    await message.answer("Video havolasini yuboring:")

@dp.message(F.text == "💳 Pulli sxema paneli")
async def pulli_sxema(message: Message):
    await message.answer("To'lov qilib chek rasmini yuboring!")

@dp.message(F.text == "🏎 The Bugatti Chiron Heshteg")
async def bugatti(message: Message):
    await message.answer("The Bugatti Chiron is a mid-engine two-seater sports car.")

@dp.message(F.text == "𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")
async def eslatma(message: Message):
    await message.answer("𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” 𝘇𝗲𝗿𝗼 𝗲𝘀𝗹𝗮𝘁𝗺𝗮 𝗺𝗼’𝗺𝗶𝗻𝗹𝗮𝗿𝗴𝗮 𝗺𝗮𝗻𝗳𝗮𝗮𝘁 𝘆𝗲𝘁𝗸𝗮𝘇𝘂𝗿.")

@dp.message(F.text == "🎮 Oʻyinlar paneli")
async def oyinlar(message: Message):
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Tosh"), KeyboardButton(text="Qaychi"), KeyboardButton(text="Qogoz")]], resize_keyboard=True)
    await message.answer("Tanlang:", reply_markup=markup)

@dp.message(F.text.in_(["Tosh", "Qaychi", "Qogoz"]))
async def play_game(message: Message):
    variants = ["Tosh", "Qaychi", "Qogoz"]
    bot_choice = random.choice(variants)
    await message.answer(f"Bot tanladi: {bot_choice}")

@dp.message(F.text == "💰 Valyuta kursi")
async def valyuta(message: Message):
    await message.answer("USD: 13,120 UZS")

@dp.message(F.text == "📩 Admenga savol yulash")
async def savol(message: Message):
    await message.answer("Savolingizni yozing:")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
