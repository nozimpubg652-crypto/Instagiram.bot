import logging
import asyncio
import os
import random
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

# --- SOZLAMALAR ---
API_TOKEN = "8514343100:AAG70S7e4qlS1B4j0FxRpgppVGMYFvhLYPY"
ADMIN_ID = 8639222385
CARD_NUMBER = "9860 1666 5489 5563"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class BotStates(StatesGroup):
    waiting_for_payment_proof = State()

# --- MENYU (Barcha tugmalar) ---
def get_super_menu():
    buttons = [
        "🎥 Video Silkasi", "⚡ Tekin Nakrutka", "🚀 Pulli sxema", "📩 Admenga xabar",
        "🆔 Nik yaratish", "🎮 O‘yinlar", "💱 Valyuta kursi", "🏎 Bugatti Chiron",
        "𖣔 Eslatmalar", "⏰ Video vaqti", "📊 Statistika", "🔥 Trend heshteglar",
        "📅 Kunlik maslahat", "🌤 Ob-havo", "📰 Yangiliklar", "🧩 Mini-quiz",
        "🎵 Musiqa tavsiyasi", "📢 Reklama", "⭐ VIP reklama", "🎁 Sovg‘a o‘yini",
        "📚 Kitob tavsiyasi", "🧠 Bilim testi", "🎬 Kino tavsiyalari", "🍔 Retsept paneli",
        "🧮 Matematika o‘yini", "🎲 Random generator", "📖 Hadis paneli", "🧘 Zikr paneli",
        "🛠 Dev tools", "🕹 Arcade o‘yin", "📜 Qur’on oyatlari", "🧾 Tarixiy faktlar",
        "⚽ Sport yangiliklari", "🚀 Texno yangiliklar", "🎨 Meme generator", "🧑‍🎓 Inglizcha so‘zlar",
        "🎤 Sitata paneli", "🧑‍🍳 Oshpazlik", "🎯 Maqsadlar"
    ]
    keyboard = [[KeyboardButton(text=text) for text in buttons[i:i+2]] for i in range(0, len(buttons), 2)]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- INSTAGRAM YUKLAGICH (Video + Matn + Heshteg) ---
@dp.message(F.text.contains("instagram.com/"))
async def download_instagram_video(message: types.Message):
    msg = await message.answer("⏳ Video va ma'lumotlar yuklanmoqda, kuting...")
    url = message.text
    video_path = f"video_{message.from_user.id}.mp4"
    
    try:
        ydl_opts = {'outtmpl': video_path, 'format': 'best', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Video matni va heshteglar
            caption = info.get('description', 'Matn topilmadi')
            if len(caption) > 1000: caption = caption[:1000] + "..."
            
        await message.answer_video(
            video=FSInputFile(video_path), 
            caption=f"📝 **Matn va Heshteglar:**\n\n{caption}\n\n🤖 @Insa_aqili_bot",
            parse_mode="Markdown"
        )
        await bot.delete_message(message.chat.id, msg.message_id)
        if os.path.exists(video_path): os.remove(video_path)
    except Exception as e:
        await msg.edit_text(f"❌ Xatolik yuz berdi. Iltimos, boshqa havola yuboring.\n{e}")

# --- PULLI SXEMA ---
@dp.message(F.text == "🚀 Pulli sxema")
async def pay_scheme(message: types.Message, state: FSMContext):
    await message.answer(f"🚀 **Pulli sxemani olish uchun:**\n\nTo‘lov qilinadigan karta:\n`{CARD_NUMBER}`\n\nPulni o‘tkazgach, chek rasmini shu yerga yuboring.", parse_mode="Markdown")
    await state.set_state(BotStates.waiting_for_payment_proof)

@dp.message(BotStates.waiting_for_payment_proof, F.photo)
async def get_payment_proof(message: types.Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{message.from_user.id}")]])
    await bot.send_photo(ADMIN_ID, photo=message.photo[-1].file_id, caption=f"📬 **Yangi to‘lov!**\nFoydalanuvchi: @{message.from_user.username}", reply_markup=kb)
    await message.answer("✅ Chek qabul qilindi. Admin tasdiqlashini kuting...")
    await state.clear()

@dp.callback_query(F.data.startswith("approve_"))
async def approve_payment(call: types.CallbackQuery):
    user_id = int(call.data.split("_")[1])
    await bot.send_message(user_id, "🎉 **To‘lovingiz tasdiqlandi!**\n\nMana sizga va'da qilingan sxema.")
    await call.message.edit_caption(caption="✅ Tasdiqlandi!")

# --- BARCHA TUGMALARNI QAYTA ISHLASH ---
@dp.message()
async def all_other_buttons(message: types.Message):
    txt = message.text
    if txt == "🍔 Retsept paneli":
        await message.answer("🥗 **Retsept:**\nPalov uchun: guruch, go‘sht, sabzi, piyoz va ziravorlar kerak.")
    elif txt == "🧮 Matematika o‘yini":
        await message.answer("Misol: 125 * 5 = ? (Javobni yozing)")
    elif txt == "📖 Hadis paneli":
        await message.answer("«Iymonning afzali sabr va bag‘rikenglikdir.»")
    elif txt == "🔥 Trend heshteglar":
        await message.answer("#reels #uzbekistan #top #trending #life")
    elif txt == "🆔 Nik yaratish":
        await message.answer(f"Sizning yangi nikingiz: Pro_User_{random.randint(100, 999)}")
    else:
        await message.answer(f"Siz '{txt}' tugmasini bosdingiz. Bu bo'lim tez orada ishga tushadi!", reply_markup=get_super_menu())

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("🤖 **Super Menyuga xush kelibsiz!**", reply_markup=get_super_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
