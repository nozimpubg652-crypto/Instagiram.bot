from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

API_TOKEN = "8514343100:AAGnKDxm66i8zTdzBx5FSWEFMtDBIAYbr4s"
ADMIN_ID = 8639222385

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Majburiy obuna kanali ---
REQUIRED_CHANNELS = ["@temuzikinsta"]

async def check_subscription(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]: return False
        except: return False
    return True

# --- Tugmalar paneli ---
main_menu = InlineKeyboardMarkup(row_width=2)
main_menu.add(
    InlineKeyboardButton("🎥 Video heshteg olish", callback_data="video_heshteg"),
    InlineKeyboardButton("🚀 TOP sxema sotiladi", callback_data="top_sxema"),
    InlineKeyboardButton("📩 Admin bilan aloqa", callback_data="admin"),
    InlineKeyboardButton("🏎 Bugatti Chiron heshteg", callback_data="bugatti"),
    InlineKeyboardButton("𖣔 Eslatmalar", callback_data="eslatma"),
    InlineKeyboardButton("⏰ Video qo‘yish vaqti", callback_data="vaqt"),
    InlineKeyboardButton("🆔 Nic yaratish", callback_data="nic"),
    InlineKeyboardButton("🎮 O‘yinlar", callback_data="oyin"),
    InlineKeyboardButton("💱 Valyuta kursi", callback_data="valyuta"),
    InlineKeyboardButton("⚡ Tezkor nakrutka", callback_data="nakrutka")
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    if not is_subscribed:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(f"📢 Obuna bo‘lish", url=f"https://t.me/temuzikinsta"))
        keyboard.add(InlineKeyboardButton("✅ Tekshirdim", callback_data="check_sub"))
        await message.answer("❗ Botdan foydalanish uchun avval kanalga obuna bo‘ling:", reply_markup=keyboard)
    else:
        await message.answer("Asosiy menyu:", reply_markup=main_menu)

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def process_check_sub(callback_query: types.CallbackQuery):
    if await check_subscription(callback_query.from_user.id):
        await callback_query.message.answer("✅ Obuna tasdiqlandi!", reply_markup=main_menu)
    else:
        await callback_query.answer("❌ Hali obuna bo‘lmadingiz!", show_alert=True)

# --- Funksiyalar ---
@dp.callback_query_handler(lambda c: c.data == "top_sxema")
async def process_top_sxema(callback_query: types.CallbackQuery):
    text = """🚀 TOP SXEMA SOTILADI! 🚀
Videolaringiz TOPga chiqishini xohlaysizmi? 🎥

Bu maxsus sinovdan o‘tgan sxema orqali videolaringiz algoritmda yuqoriga ko‘tariladi, ko‘rishlar keskin oshadi! 📈
✅ 100% ishlaydigan va tekshirilgan usul
✅ Har qanday kontent uchun mos
💰 Narx: 35ming so'm
To‘lov qilib chek rasmini yuboring, admin tekshirib bot orqali tashlaydi. Agar ishlamay qolsa @roziyev2"""
    await callback_query.message.answer(text)

@dp.callback_query_handler(lambda c: c.data == "admin")
async def process_admin(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Savolingizni yozing, men uni admenga yuboraman:")
    # Bu yerda admin uchun savol qabul qilish mantig'i qo'shiladi

@dp.message_handler(lambda message: message.reply_to_message is None and "savol" in message.text.lower())
async def get_question(message: types.Message):
    await bot.send_message(ADMIN_ID, f"📩 Yangi savol:\nFoydalanuvchi: @{message.from_user.username}\nID: {message.from_user.id}\nXabar: {message.text}")
    await message.answer("✅ Savolingiz admenga yuborildi.")

@dp.callback_query_handler(lambda c: c.data == "bugatti")
async def process_bugatti(callback_query: types.CallbackQuery):
    text = """Here's the information about the Bugatti Chiron:
The Bugatti Chiron is a mid-engine two-seater sports car designed and developed in Germany by Bugatti Engineering GmbH.
CRISGIRLY
The successor to the Bugatti Veyron, the Chiron was first shown at the Geneva Motor Show on 1 March 2016.
The car's design was initially previewed with the Bugatti Vision Gran Turismo concept car unveiled at the 2015 Frankfurt Auto Show.
The Chiron was recreated in Lego as 2018's annual Technic sports car. It was released on 1 June 2018 as a 1:8 scale model with 3,600 individual parts."""
    await callback_query.message.answer(text)

@dp.callback_query_handler(lambda c: c.data == "eslatma")
async def process_eslatma(callback_query: types.CallbackQuery):
    text = """𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” 𝘇𝗲𝗿𝗼 𝗲𝘀𝗹𝗮𝘁𝗺𝗮 𝗺𝗼’𝗺𝗶𝗻𝗹𝗮𝗿𝗴𝗮 𝗺𝗮𝗻𝗳𝗮𝗮𝘁 𝘆𝗲𝘁𝗸𝗮𝘇𝘂𝗿. (Zarriyot surasi, 55 ) ___
𝗦𝘂𝗯𝗵𝗮𝗻𝗮𝗹𝗹𝗼𝗵 - 𝐴𝑙𝑙𝑜ℎ 𝑏𝑎𝑟𝑐ℎ𝑎 𝑛𝑢𝑞𝑠𝑜𝑛𝑙𝑎𝑟𝑑𝑎𝑛 ℎ𝑜𝑙𝑖 𝑣𝑎 𝑝𝑜𝑘𝑑𝑖𝑟...
𝗔𝗹𝗵𝗮𝗺𝗱𝘂𝗹𝗶𝗹𝗹𝗮𝗵 - 𝐵𝑎𝑟𝑐ℎ𝑎 𝑚𝑎𝑞𝑡𝑜𝑣 𝐴𝑙𝑙𝑜ℎ𝑔𝑎...
𝗔𝗹𝗹𝗼𝗵 𝗔𝗸𝗯𝗮𝗿 - 𝐴𝑙𝑙𝑜ℎ 𝑏𝑢𝑦𝑢𝑘𝑑𝑖𝑟... ♻️ 𝗩𝗶𝗱𝗲𝗼𝗻𝗶 𝘂𝗹𝗮𝘀𝗵𝗶𝗻𝗴. 𝗜𝗻𝘀𝗵𝗮 𝗮𝗹𝗹𝗼𝗵 𝗯𝘂𝗻𝗶𝗻𝗴 𝗮𝗷𝗿𝘂 𝘀𝗮𝘃𝗼𝗯𝗶 𝗯𝗼𝗿... 𖣔

#muhammad #allah #islam #namaz #quran #inshaallah #shukurullohdomla #muslim #tushuncha_ol"""
    await callback_query.message.answer(text)

@dp.callback_query_handler(lambda c: c.data == "vaqt")
async def process_vaqt(callback_query: types.CallbackQuery):
    text = """Rekga chiqish vaqtlari😊❤️
6:00✅ 8:00🫵🏻 11:00🫶🏻 16:00🤍 20:00💋 22:00 🖤 00:00 ❤️
Manzil Видео в топ"""
    await callback_query.message.answer(text)

@dp.callback_query_handler(lambda c: c.data == "tekshir")
async def process_tekshir(callback_query: types.CallbackQuery):
    await callback_query.message.answer("✅ Shart bajarildi!\nLeofame linki: https://leofame.com")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
