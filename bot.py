import os
import asyncio
import random
import yt_dlp # Instaloader o'rniga
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN") or "TOKENINGIZNI_SHU_YERGA_YOZING"
ADMIN_ID = 8639222385
CHANNEL_ID = "@temuzikinsta"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- YORDAMCHI FUNKSIYALAR ---
def generate_large_nick_list():
    bases = ["Cyber", "Dark", "Neon", "Shadow", "Pro", "Ultra", "Mega", "Ghost", "Titan", "Elite"]
    suffixes = ["Warrior", "King", "Lord", "Sniper", "Gamer", "Soul", "Blade", "Force", "Hunter", "Ghost"]
    return [f"{b}_{s}{i}" for b in bases for s in suffixes for i in range(100, 999)]

NICKS = generate_large_nick_list()

async def check_sub(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status != ChatMemberStatus.LEFT
    except: return False

def get_main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📥 Video Silkasi orqali heshteg olish🥶")],
        [KeyboardButton(text="💳 Pulli sxema paneli"), KeyboardButton(text="📩 Admenga savol yulash")],
        [KeyboardButton(text="🏎 The Bugatti Chiron Heshteg"), KeyboardButton(text="𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")],
        [KeyboardButton(text="⏱ Vidiyo qõyish vaqti✅🫠"), KeyboardButton(text="✨ Niklar yaratish paneli")],
        [KeyboardButton(text="🎮 Oʻyinlar paneli"), KeyboardButton(text="💰 Valyuta kursi")],
        [KeyboardButton(text="🚀 Tekin nakrutka paneli")]
    ], resize_keyboard=True)

# --- INSTAGRAM QISMI (YANGILANGAN) ---
@dp.message(F.text.startswith("https://www.instagram.com/"))
async def get_instagram_hashtags(msg: Message):
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(msg.text, download=False)
            caption = info.get('description', 'Matn topilmadi.')
            await msg.answer(f"✅ **Video matni:**\n\n{caption[:1000]}")
    except Exception:
        await msg.answer("❌ Video matnini olishda xatolik. Havola ochiqmi?")

# --- CHEK VA SAVOL JAVOB TIZIMI ---
@dp.message(F.reply_to_message)
async def admin_replies(msg: Message):
    if msg.from_user.id == ADMIN_ID:
        # Chekka javoblar
        if msg.text == "/ok":
            try:
                user_id = msg.reply_to_message.caption.split("ID: ")[1].split("\n")[0]
                await bot.send_message(user_id, "✅ To'lovingiz tasdiqlandi! Sxema: [MAXFIY SXEMA]")
                await msg.answer("✅ Sxema foydalanuvchiga yuborildi.")
            except: await msg.answer("❌ Xatolik.")
        elif msg.text == "/no":
            try:
                user_id = msg.reply_to_message.caption.split("ID: ")[1].split("\n")[0]
                await bot.send_message(user_id, "❌ To'lovingiz rad etildi.")
                await msg.answer("✅ Rad etildi.")
            except: await msg.answer("❌ Xatolik.")
        else:
            # Oddiy javob
            try:
                user_id = msg.reply_to_message.caption.split("ID: ")[1].split("\n")[0]
                await bot.send_message(user_id, f"📩 Admindan javob:\n{msg.text}")
                await msg.answer("✅ Javob yuborildi!")
            except: await msg.answer("❌ Foydalanuvchi ID topilmadi.")

@dp.message(lambda msg: msg.text not in ["📥 Video Silkasi orqali heshteg olish🥶", "💳 Pulli sxema paneli", "📩 Admenga savol yulash", "🏎 The Bugatti Chiron Heshteg", "𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇", "⏱ Vidiyo qõyish vaqti✅🫠", "✨ Niklar yaratish paneli", "🎮 Oʻyinlar paneli", "💰 Valyuta kursi", "🚀 Tekin nakrutka paneli", "Tosh", "Qaychi", "Qogoz"] and not msg.text.startswith("https://"))
async def handle_user_question(msg: Message):
    await bot.send_message(ADMIN_ID, f"📩 Yangi savol:\nFoydalanuvchi: @{msg.from_user.username}\nID: {msg.from_user.id}\nMatn: {msg.text}")
    await msg.answer("✅ Savolingiz admenga yuborildi!")

@dp.message(F.photo)
async def handle_photo(msg: Message):
    await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=f"To'lov cheki:\nFoydalanuvchi: @{msg.from_user.username}\nID: {msg.from_user.id}")
    await msg.answer("✅ Chek qabul qilindi, admin tekshirmoqda!")

# --- BOSHQA FUNKSIYALAR ---
@dp.message(F.text == "🎮 Oʻyinlar paneli")
async def cmd_oyin(msg: Message):
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Tosh"), KeyboardButton(text="Qaychi"), KeyboardButton(text="Qogoz")]], resize_keyboard=True)
    await msg.answer("Tanlang:", reply_markup=markup)

@dp.message(F.text == "✨ Niklar yaratish paneli")
async def cmd_nik(msg: Message): await msg.answer("Ism va familiyangizni yuboring:")

@dp.message(F.text == "💰 Valyuta kursi")
async def cmd_valyuta(msg: Message): await msg.answer("USD: 13,120 UZS")

@dp.message(Command("start"))
async def start(msg: Message): await msg.answer("Xush kelibsiz!", reply_markup=get_main_menu())

async def main(): 
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__": asyncio.run(main())
