import os
import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8639222385  # Sizning Telegram ID
CHANNEL_ID = "@temuzikinsta"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1000+ niklar generatori
def generate_large_nick_list():
    bases = ["Cyber", "Dark", "Neon", "Shadow", "Pro", "Ultra", "Mega", "Ghost", "Titan", "Elite"]
    suffixes = ["Warrior", "King", "Lord", "Sniper", "Gamer", "Soul", "Blade", "Force", "Hunter", "Ghost"]
    return [f"{b}_{s}{i}" for b in bases for s in suffixes for i in range(100, 200)]

NICKS = generate_large_nick_list()

async def check_sub(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status != ChatMemberStatus.LEFT
    except:
        return False

def get_main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📥 Video Silkasi orqali heshteg olish🥶")],
        [KeyboardButton(text="💳 Pulli sxema paneli"), KeyboardButton(text="📩 Admenga savol yulash")],
        [KeyboardButton(text="🏎 The Bugatti Chiron Heshteg"), KeyboardButton(text="𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")],
        [KeyboardButton(text="⏱ Vidiyo qõyish vaqti✅🫠"), KeyboardButton(text="✨ Niklar yaratish paneli")],
        [KeyboardButton(text="🎮 Oʻyinlar paneli"), KeyboardButton(text="💰 Valyuta kursi")],
        [KeyboardButton(text="🚀 Tekin nakrutka paneli")]
    ], resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Salom! Xush kelibsiz. Kerakli bo'limni tanlang:", reply_markup=get_main_menu())

# CHEK QABUL QILISH FUNKSIYASI
@dp.message(F.photo)
async def handle_payment_check(message: Message):
    photo_id = message.photo[-1].file_id
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=f"💳 Yangi to'lov cheki keldi!\nFoydalanuvchi: @{message.from_user.username}\nID: {message.from_user.id}"
    )
    await message.answer("✅ Chek qabul qilindi! Admin tekshirib, sizga javob beradi.")

# Qolgan panellar (nakrutka, niklar, o'yinlar) avvalgidek ishlaydi...
@dp.message(F.text == "🚀 Tekin nakrutka paneli")
async def nakrutka(message: Message):
    if await check_sub(message.from_user.id):
        await message.answer("Siz obuna bo'lgansiz! Mana link: https://leofame.com")
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Kanalga obuna bo'lish", url="https://t.me/temuzikinsta")], [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]])
        await message.answer("Nakrutka uchun kanalga obuna bo'ling!", reply_markup=markup)

@dp.callback_query(F.data == "check_sub")
async def verify_sub(callback: CallbackQuery):
    if await check_sub(callback.from_user.id):
        await callback.message.edit_text("Rahmat! Link: https://leofame.com")
    else:
        await callback.answer("Hali obuna bo'lmagansiz!", show_alert=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
