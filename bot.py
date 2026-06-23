from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

API_TOKEN = "8514343100:AAG70S7e4qlS1B4j0FxRpgppVGMYFvhLYPY"
ADMIN_ID = 8639222385

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Majburiy obuna kanali ---
REQUIRED_CHANNELS = ["@temuzikinsta"]

async def check_subscription(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

# --- Tugmalar paneli ---
main_menu = InlineKeyboardMarkup(row_width=2)
main_menu.add(
    InlineKeyboardButton("🎥 Video Silkasi", callback_data="video"),
    InlineKeyboardButton("⚡ Tekin Nakrutka", callback_data="nakrutka"),
    InlineKeyboardButton("🚀 Pulli sxema paneli", callback_data="sxema"),
    InlineKeyboardButton("📩 Admenga savol yuborish", callback_data="admin"),
    InlineKeyboardButton("🆔 Niklar yaratish paneli", callback_data="nic"),
    InlineKeyboardButton("🎮 O‘yinlar paneli", callback_data="oyin"),
    InlineKeyboardButton("💱 Valyuta kursi", callback_data="valyuta"),
    InlineKeyboardButton("🏎 Bugatti Chiron Heshteg", callback_data="bugatti"),
    InlineKeyboardButton("𖣔 Eslating Heshtegi", callback_data="eslatma"),
    InlineKeyboardButton("⏰ Vidiyo qo‘yish vaqti", callback_data="vaqt"),
    InlineKeyboardButton("📊 Statistika paneli", callback_data="stat"),
    InlineKeyboardButton("🔥 Trend heshteglar", callback_data="trend")
)

# --- Start komandasi ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton("📢 Obuna bo‘lish", url="https://t.me/temuzikinsta"))
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
@dp.callback_query_handler(lambda c: c.data == "video")
async def process_video(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Instagram havolasini yuboring:")

@dp.callback_query_handler(lambda c: c.data == "nakrutka")
async def process_nakrutka(callback_query: types.CallbackQuery):
    await callback_query.message.answer("⚡ Tezkor nakrutka paneli ⚡\nShart: 5 ta do‘stni @temuzikinsta kanaliga qo‘shing.\n✅ Tekshirish tugmasini bosib tasdiqlang.")

@dp.callback_query_handler(lambda c: c.data == "sxema")
async def process_sxema(callback_query: types.CallbackQuery):
    await callback_query.message.answer("🚀 Pulli sxema paneli\nNarx: 35 ming so‘m\nTo‘lov qilib chek yuboring.")

@dp.callback_query_handler(lambda c: c.data == "admin")
async def process_admin(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Savolingizni yozing, men uni admenga yuboraman:")

@dp.message_handler(lambda message: "savol" in message.text.lower())
async def get_question(message: types.Message):
    await bot.send_message(ADMIN_ID, f"📩 Yangi savol:\nFoydalanuvchi: @{message.from_user.username}\nID: {message.from_user.id}\nXabar: {message.text}")
    await message.answer("✅ Savolingiz admenga yuborildi.")

@dp.callback_query_handler(lambda c: c.data == "bugatti")
async def process_bugatti(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Bugatti Chiron haqida: Mid-engine sport car, 2016-yilda Geneva Motor Show’da taqdim etilgan. Lego modeli 2018-yilda chiqarilgan (3600 detal).")

@dp.callback_query_handler(lambda c: c.data == "eslatma")
async def process_eslatma(callback_query: types.CallbackQuery):
    await callback_query.message.answer("𖣔 “Eslating” mo‘minlarga foyda yetkazur (Zarriyot 55)\nSubhanallah 🌸\nAlhamdulillah 🌸\nAllohu Akbar 🌸")

@dp.callback_query_handler(lambda c: c.data == "vaqt")
async def process_vaqt(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Rekka chiqish vaqtlari: 6:00, 8:00, 11:00, 16:00, 20:00, 22:00, 00:00")

@dp.callback_query_handler(lambda c: c.data == "nic")
async def process_nic(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Ism va familiyangizni yuboring:")

@dp.message_handler(lambda message: len(message.text.split()) == 2)
async def create_nic(message: types.Message):
    ism, familiya = message.text.split()
    nic = f"{ism[:3]}{familiya[:3]}{random.randint(1000,9999)}"
    await message.answer(f"Siz uchun yaratilgan unikal nickname: {nic}")

@dp.callback_query_handler(lambda c: c.data == "oyin")
async def process_oyin(callback_query: types.CallbackQuery):
    oyin_menu = InlineKeyboardMarkup(row_width=3)
    oyin_menu.add(
        InlineKeyboardButton("🪨 Tosh", callback_data="tosh"),
        InlineKeyboardButton("✂️ Qaychi", callback_data="qaychi"),
        InlineKeyboardButton("📄 Qog‘oz", callback_data="qogoz")
    )
    await bot.send_message(callback_query.from_user.id, "O‘yin boshladik! Tanlang:", reply_markup=oyin_menu)

@dp.callback_query_handler(lambda c: c.data in ["tosh","qaychi","qogoz"])
async def play_game(callback_query: types.CallbackQuery):
    user_choice = callback_query.data
    bot_choice = random.choice(["tosh","qaychi","qogoz"])
    if user_choice == bot_choice:
        result = "🤝 Tenglik!"
    elif (user_choice == "tosh" and bot_choice == "qaychi") or \
         (user_choice == "qaychi" and bot_choice == "qogoz") or \
         (user_choice == "qogoz" and bot_choice == "tosh"):
        result = "🎉 Siz yutdingiz!"
    else:
        result = "😅 Bot yutdi!"
    await bot.send_message(callback_query.from_user.id, f"Siz: {user_choice}, Bot: {bot_choice}\nNatija: {result}")

@dp.callback_query_handler(lambda c: c.data == "valyuta")
async def process_valyuta(callback_query: types.CallbackQuery):
    kurslar = {"USD": 12600, "EUR": 13800, "RUB": 140}
    text = "💱 Valyuta kurslari:\n"
    for k, v in kurslar.items():
        text += f"{k}: {v} so‘m\n"
    await callback_query.message.answer(text)

@dp.callback_query_handler(lambda c: c.data == "stat")
async def process_stat(callback_query: types.CallbackQuery):
    await callback_query.message.answer("📊 Statistika paneli:\n- Foydalanuvchilar soni: 120\n- Bugungi kirishlar: 35\n- Aktiv tugma bosishlar: 80")

@dp.callback_query_handler(lambda c: c.data == "trend")
async def process_trend(callback_query: types.CallbackQuery):
    await callback_query.message.answer("🔥 Trend heshteglar:\n#viral #explore #fyp #instagood #love #fashion #motivation")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
