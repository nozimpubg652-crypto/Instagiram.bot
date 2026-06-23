import random
import logging
import asyncio
import os
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
REQUIRED_CHANNELS = ["@temuzikinsta"]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

USERS_DB = set()

class BotStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_admin_msg = State()
    waiting_for_math_ans = State()

async def check_subscription(user_id: int) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]: return False
        except: return False
    return True

# --- PASTKI KLAVIATURA (REPLY MENU) KONSTRUKTORI ---
def get_super_menu():
    buttons_text = [
        "🎥 Video Silkasi", "⚡ Tekin Nakrutka",
        "🚀 Pulli sxema", "📩 Admenga xabar",
        "🆔 Nik yaratish", "🎮 O‘yinlar",
        "💱 Valyuta kursi", "🏎 Bugatti Chiron",
        "𖣔 Eslatmalar", "⏰ Video vaqti",
        "📊 Statistika", "🔥 Trend heshteglar",
        "📅 Kunlik maslahat", "🌤 Ob-havo",
        "📰 Yangiliklar", "🧩 Mini-quiz",
        "🎵 Musiqa tavsiyasi", "📢 Reklama",
        "⭐ VIP reklama", "🎁 Sovg‘a o‘yini",
        "📚 Kitob tavsiyasi", "🧠 Bilim testi",
        "🎬 Kino tavsiyalari", "🍔 Retsept paneli",
        "🧮 Matematika o‘yini", "🎲 Random generator",
        "📖 Hadis paneli", "🧘 Zikr paneli",
        "🛠 Dev tools", "🕹 Arcade o‘yin",
        "📜 Qur’on oyatlari", "🧾 Tarixiy faktlar",
        "⚽ Sport yangiliklari", "🚀 Texno yangiliklar",
        "🎨 Meme generator", "🧑‍🎓 Inglizcha so‘zlar",
        "🎤 Sitata paneli", "🧑‍🍳 Oshpazlik",
        "🎯 Maqsadlar"
    ]
    
    keyboard = []
    row = []
    for text in buttons_text:
        row.append(KeyboardButton(text=text))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- START VA MAJBURIY OBUNA ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    USERS_DB.add(message.from_user.id)
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Obuna bo‘lish", url="https://t.me/temuzikinsta")],
            [InlineKeyboardButton(text="✅ Tekshirdim", callback_data="check_sub")]
        ])
        await message.answer("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=keyboard)
    else:
        await message.answer("🤖 **Super Menyuga xush kelibsiz!** Quyidagi tugmalardan birini tanlang:", reply_markup=get_super_menu(), parse_mode="Markdown")

@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback_query: types.CallbackQuery):
    if await check_subscription(callback_query.from_user.id):
        await callback_query.message.answer("✅ Obuna tasdiqlandi! Asosiy menyu ochildi.", reply_markup=get_super_menu())
    else:
        await callback_query.answer("❌ Hali obuna bo‘lmadingiz!", show_alert=True)

# --- INSTAGRAM VIDEO YUKLASH QISMI (MATN VA HESHTEGLARI BILAN) ---
@dp.message(F.text.contains("instagram.com/"))
async def download_instagram_video(message: types.Message):
    status_msg = await message.answer("⏳ Instagram videosi yuklanmoqda, iltimos kuting...")
    url = message.text
    video_path = f"video_{message.from_user.id}.mp4"
    
    ydl_opts = {
        'outtmpl': video_path,
        'format': 'best',
        'quiet': True,
    }
    
    try:
        # Videoni va ma'lumotlarni serverga tortish
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Instagramdagi asil matn va heshteglarni ajratib olish
            original_caption = info_dict.get('description', '')
            
        # Telegram videoga qo'shiladigan matn uzunligi 1024 belgidan oshmasligi kerak.
        if original_caption:
            caption_text = f"{original_caption[:900]}\n\n🤖 @temuzikinsta"
        else:
            caption_text = "📥 Botingiz orqali yuklab olindi!\n\n🤖 @temuzikinsta"
            
        # Foydalanuvchiga yuborish
        video_file = FSInputFile(video_path)
        await message.answer_video(video=video_file, caption=caption_text, reply_markup=get_super_menu())
        
        # "Kuting..." xabarini o'chirib tashlaymiz
        await bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
        
        # Serverni to'ldirib yubormaslik uchun videoni o'chirib tashlaymiz
        if os.path.exists(video_path):
            os.remove(video_path)
            
    except Exception as e:
        await status_msg.edit_text("❌ Videoni yuklab olishda xatolik yuz berdi. Yopiq (private) profil yoki noto'g'ri havola bo'lishi mumkin.")
        if os.path.exists(video_path):
            os.remove(video_path)

# --- NIK YARATISH ---
@dp.message(F.text == "🆔 Nik yaratish")
async def start_nickname(message: types.Message, state: FSMContext):
    await message.answer("🆔 Ismingizni yuboring:")
    await state.set_state(BotStates.waiting_for_name)

@dp.message(BotStates.waiting_for_name)
async def generate_nickname(message: types.Message, state: FSMContext):
    name = message.text.strip()
    styles = [f"✨ {name} ✨", f"🔥 『{name}』 🔥", f"⚡ {name}_King ⚡"]
    await message.answer("🎭 **Siz uchun niklar:**\n\n" + "\n".join(styles), reply_markup=get_super_menu(), parse_mode="Markdown")
    await state.clear()

# --- ADMENGA XABAR ---
@dp.message(F.text == "📩 Admenga xabar")
async def admin_message_start(message: types.Message, state: FSMContext):
    await message.answer("📩 Xabaringizni yozing:")
    await state.set_state(BotStates.waiting_for_admin_msg)

@dp.message(BotStates.waiting_for_admin_msg)
async def admin_message_send(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📬 **Xabar:**\n👤 @{message.from_user.username}\n📝 {message.text}")
    await message.answer("✅ Yuborildi!", reply_markup=get_super_menu())
    await state.clear()

# --- MATEMATIKA ---
@dp.message(F.text == "🧮 Matematika o‘yini")
async def math_game_start(message: types.Message, state: FSMContext):
    num1 = random.randint(5, 20)
    num2 = random.randint(5, 20)
    correct_ans = num1 + num2
    await state.update_data(correct_ans=correct_ans)
    await message.answer(f"🧮 **Misolni yeching:**\n\n{num1} + {num2} = ?\n\nJavobingizni raqam bilan yozing:")
    await state.set_state(BotStates.waiting_for_math_ans)

@dp.message(BotStates.waiting_for_math_ans)
async def math_game_check(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        user_ans = int(message.text.strip())
        if user_ans == data['correct_ans']:
            await message.answer("🎉 To‘g‘ri javob! Barakalla! 🏅", reply_markup=get_super_menu())
        else:
            await message.answer(f"❌ Noto‘g‘ri! To‘g‘ri javob {data['correct_ans']} edi.", reply_markup=get_super_menu())
    except ValueError:
        await message.answer("⚠️ Iltimos faqat raqam bilan javob bering!", reply_markup=get_super_menu())
    await state.clear()

# --- QOLGAN BARCHA TUGMALAR ---
@dp.message()
async def process_all_texts(message: types.Message):
    responses = {
        "🎥 Video Silkasi": "🎥 Instagram Reals yoki Video havolasini shunchaki botga yuboring, men yuklab beraman!",
        "⚡ Tekin Nakrutka": "⚡ 5 ta do‘stingizni taklif qiling.",
        "🚀 Pulli sxema": "🚀 Pulli sxema: 35 000 so‘m.",
        "🎮 O‘yinlar": "🎮 Emojilardan (✊, ✌️, ✋) birini yuboring.",
        "💱 Valyuta kursi": "💱 1 USD = 12 800 so‘m.",
        "🏎 Bugatti Chiron": "🏎 Bugatti Chiron tezligi 420 km/s.",
        "𖣔 Eslatmalar": "𖣔 Subhanalloh, Alhamdulillah, Allohu Akbar.",
        "⏰ Video vaqti": "⏰ 08:00, 11:00, 20:00, 22:00.",
        "📊 Statistika": f"📊 Foydalanuvchilar: {len(USERS_DB)} ta.",
        "🔥 Trend heshteglar": "`#viral #explore #fyp #instagood #love`",
        "📅 Kunlik maslahat": "📅 Harakat qilgan odam doim maqsadiga yetadi.",
        "🌤 Ob-havo": "🌤 Toshkent: +28°C, Quyoshli.",
        "📰 Yangiliklar": "📰 IT sohasi kundan kunga rivojlanmoqda.",
        "🧩 Mini-quiz": "🧩 Savol: O‘zbekiston poytaxti qaysi? (Toshkent)",
        "🎵 Musiqa tavsiyasi": "🎵 Sevara Nazarkhan — 'Yor-yor'.",
        "📢 Reklama": "📢 Reklama uchun admin bilan bog'laning.",
        "⭐ VIP reklama": "⭐ VIP xizmatlarimiz orqali axvatni ko'taring!",
        "🎁 Sovg‘a o‘yini": "🎁 Eng aktiv foydalanuvchilarga sovg'alar bor!",
        "📚 Kitob tavsiyasi": "📚 O‘qishni tavsiya qilamiz: 'O‘tkan kunlar'.",
        "🧠 Bilim testi": "🧠 Quyosh tizimidagi eng katta sayyora: Yupiter.",
        "🎬 Kino tavsiyalari": "🎬 'Inception' filmini ko‘ring.",
        "🍔 Retsept paneli": "🍔 Tovuqli sendvich tayyorlash sirlari.",
        "🎲 Random generator": f"🎲 Sizning omadli raqamingiz: {random.randint(1, 100)}",
        "📖 Hadis paneli": "📖 'Amallar niyatlarga ko‘ra bo‘ladi.'",
        "🧘 Zikr paneli": "🧘 'Subhanallohi va bihamdihi'.",
        "🛠 Dev tools": "🛠 Bot Python (aiogram) orqali yaratilgan.",
        "🕹 Arcade o‘yin": "🕹 Keling, biror o'yin o'ynaymiz!",
        "📜 Qur’on oyatlari": "📜 'Albatta, har bir qiyinchilik bilan yengillik bordir.'",
        "🧾 Tarixiy faktlar": "🧾 Amir Temur yengilmas sarkarda bo'lgan.",
        "⚽ Sport yangiliklari": "⚽ Chempionlar ligasi o'yinlari qizg'in pallada!",
        "🚀 Texno yangiliklar": "🚀 Yangi texnologiyalar premyerasi kutilyapti.",
        "🎨 Meme generator": "🎨 Ajoyib memelar tez orada qo'shiladi.",
        "🧑‍🎓 Inglizcha so‘zlar": "🧑‍🎓 'Success' — Muvaffaqiyat.",
        "🎤 Sitata paneli": "🎤 'Hayot — bu harakat.'",
        "🧑‍🍳 Oshpazlik": "🧑‍🍳 Mazali taomlar siri olovni to'g'ri sozlashda.",
        "🎯 Maqsadlar": "🎯 Maqsadingiz sari qadam tashlashdan to'xtamang!"
    }
    if message.text in responses:
        await message.answer(responses[message.text], reply_markup=get_super_menu(), parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
