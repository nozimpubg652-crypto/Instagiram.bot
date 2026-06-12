import os
import sqlite3
import yt_dlp
import random
import requests
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# --- SOZLAMALAR ---
API_TOKEN = '8870187278:AAGWhBPnKCkK6MVpdMta7rGOapUAq0FvaTw'
CHANNEL_ID = '@temuzikinsta'
ADMIN_ID = 8639222385
SECURITY_ID = 8639222385
ADMIN_USERNAME = "@roziyev2"
KARTA_RAQAM = "uzur hozir karta bloklangan"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- BAZA (Foydalanuvchilar va Referral) ---
conn = sqlite3.connect('bot_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, invited_by INTEGER, referrals INTEGER DEFAULT 0)')
conn.commit()

class FSM(StatesGroup):
    waiting_for_link = State()
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_chek = State()

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

# --- ASOSIY FUNKSIYALAR ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📥 Media yukla", "✨ Niklar paneli", "🎮 O'yin", "💰 Valyuta kursi")
    markup.add("📊 Statistika", "🚀 Tekin nakrutka", "📢 Reklama", "💳 Pulli sxema")
    return markup

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Xavfsizlik: Boshqa id dan kirishga urinsa ogohlantirish
    if message.from_user.id != ADMIN_ID and message.from_user.id != SECURITY_ID:
        # Oddiy foydalanuvchi bazaga qo'shiladi
        cursor.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (message.from_user.id,))
        # Referral tekshiruvi
        args = message.get_args()
        if args and args.isdigit():
            referrer = int(args)
            cursor.execute('SELECT id FROM users WHERE id=?', (referrer,))
            if cursor.fetchone() and referrer != message.from_user.id:
                cursor.execute('UPDATE users SET referrals = referrals + 1 WHERE id=?', (referrer,))
                conn.commit()
    
    if not await is_subscribed(message.from_user.id):
        await message.answer("Botdan foydalanish uchun kanalimizga obuna bo'ling!", 
                             reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Obuna bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}")))
    else:
        await message.answer("Xush kelibsiz! Tanlang:", reply_markup=get_main_markup())

# --- MEDIA YUKLASH ---
@dp.message_handler(text="📥 Media yukla")
async def ask_link(message: types.Message):
    await message.answer("Havolani yuboring:")
    await FSM.waiting_for_link.set()

@dp.message_handler(state=FSM.waiting_for_link)
async def process_media(message: types.Message, state: FSMContext):
    await message.answer("🔍 Yuklanmoqda...")
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'media.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message.text, download=True)
            caption = info.get('description', '')
        # Matn va heshteglarni ajratib olamiz
    text_only = ' '.join([w for w in caption.split() if not w.startswith('#')])
    hashtags = ' '.join([w for w in caption.split() if w.startswith('#')])
    
    # 1. Videoni matn va heshteglar bilan bitta qilib yuboramiz
    await message.answer_video(open('media.mp4', 'rb'), caption=f"{text_only}\n\n{hashtags}")
    
    # 2. Musiqani alohida xabar sifatida yuboramiz
    os.system("ffmpeg -i media.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3 -y")
    await message.answer_audio(open('audio.mp3', 'rb'), caption="🎵 Musiqa")
        tags = [w for w in caption.split() if w.startswith('#')]
        if tags: await message.answer(f"🏷 Heshteglar: {' '.join(tags)}")
        os.remove('media.mp4'); os.remove('audio.mp3')
    except: await message.answer("❌ Xatolik.")
    await state.finish()

# --- NIKLAR PANELI (To'g'rilangan) ---
@dp.message_handler(text="✨ Niklar paneli")
async def nick_panel(message: types.Message):
    await message.answer("Ismingizni yozing:")
    await FSM.waiting_for_name.set()

@dp.message_handler(state=FSM.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Familiyangizni yozing:")
    await FSM.waiting_for_surname.set()

@dp.message_handler(state=FSM.waiting_for_surname)
async def gen_nick(message: types.Message, state: FSMContext):
    data = await state.get_data()
    symbols = ["꧁", "⚡", "🔥", "☠", "⚔", "💎"]
    res = f"{random.choice(symbols)}{data['name']}_{message.text}{random.choice(symbols)}"
    await message.answer(f"Sizning nik: {res}")
    await state.finish()

# --- O'YIN (Tosh, Qaychi, Qog'oz) ---
@dp.message_handler(text="🎮 O'yin")
async def play_game(message: types.Message):
    items = ["🪨 Tosh", "✂️ Qaychi", "📄 Qog'oz"]
    u, b = random.choice(items), random.choice(items)
    await message.answer(f"Siz: {u}\nBot: {b}\n\n{'Tenglik!' if u==b else 'Siz yutdingiz!' if (u=='🪨' and b=='✂️') or (u=='✂️' and b=='📄') or (u=='📄' and b=='🪨') else 'Bot yutdi!'}")

# --- TEKIN NAKRUTKA ---
@dp.message_handler(text="🚀 Tekin nakrutka")
async def nakrutka(message: types.Message):
    cursor.execute('SELECT referrals FROM users WHERE id=?', (message.from_user.id,))
    data = cursor.fetchone() # 1. Bazadan ma'lumotni olib, data nomli idishga solamiz
if data:                 # 2. Agar idishda ma'lumot bo'lsa
    ref = data[0]        # 3. Ma'lumotni o'qiymiz
else:                    # 4. Agar bazada hech narsa bo'lmasa
    ref = 0              # 5. ref ni 0 ga tenglaymiz (xato chiqmaydi)
    if ref < 10:
        # 130-qator atrofini shunday qiling:
    me = await bot.get_me() # Bot ma'lumotini alohida olamiz
    bot_username = me.username

    await message.answer(f"10 ta do'st taklif qiling (Hozir: {ref}/10).\nSilka: https://t.me/{bot_username}?start={message.from_user.id}")
else:
    await message.answer("Tabriklaymiz! Mana: https://leofame.com")
        await message.answer("Tabriklaymiz! Mana: https://leofame.com")

# --- PULLI SXEMA VA CHEK ---
@dp.message_handler(text="💳 Pulli sxema")
async def pay_sxema(message: types.Message):
    await message.answer(f"Karta: `{KARTA_RAQAM}`. Pul tashlang va chek rasmini yuboring.")
    await FSM.waiting_for_chek.set()

@dp.message_handler(content_types=['photo'], state=FSM.waiting_for_chek)
async def chek_yubor(message: types.Message, state: FSMContext):
    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"Foydalanuvchi: {message.from_user.id}\n/ok - sxema yuborish\n/cancel - soxta chek")
    await message.answer("Chek qabul qilindi.")
    await state.finish()

@dp.message_handler(commands=['ok'])
async def ok(message: types.Message):
    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        uid = message.reply_to_message.caption.split('\n')[0].split(': ')[1]
        await bot.send_message(uid, "Mana sxema: [Sizning faylingiz]")

@dp.message_handler(commands=['cancel'])
async def cancel(message: types.Message):
    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        uid = message.reply_to_message.caption.split('\n')[0].split(': ')[1]
        await bot.send_message(uid, "Soxta chek yubormang! 🤬")

# --- ADMIN / REKLAMA ---
@dp.message_handler(text="📢 Reklama")
async def rek(message: types.Message):
    await message.answer(f"Adminga murojaat qiling: {ADMIN_USERNAME}")

@dp.message_handler(text="📊 Statistika")
async def stat(message: types.Message):
    cursor.execute('SELECT COUNT(*) FROM users')
    await message.answer(f"Jami foydalanuvchilar: {cursor.fetchone()[0]}")

if __name__ == '__main__':
    # Ushbu qator botni qayta ishga tushirish uchun qo'shildi
    print("Restarting bot...")
    executor.start_polling(dp, skip_updates=True)
