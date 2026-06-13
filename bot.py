import os
import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8639222385
CHANNEL_ID = "@temuzikinsta"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1000+ niklar generatori
def generate_large_nick_list():
    bases = ["Cyber", "Dark", "Neon", "Shadow", "Pro", "Ultra", "Mega", "Ghost", "Titan", "Elite"]
    suffixes = ["Warrior", "King", "Lord", "Sniper", "Gamer", "Soul", "Blade", "Force", "Hunter", "Ghost"]
    return [f"{b}_{s}{i}" for b in bases for s in suffixes for i in range(100, 999)]

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

# 1. INSTAGRAM VIDEO HAVOLASI UCHUN HESHTEGLAR
@dp.message(F.text.startswith("https://www.instagram.com/"))
async def get_instagram_hashtags(msg: Message):
    hashtags = "#reels #instagram #top #trend #videographer #views #follow #like #uzbekistan #tashkent #creative #algorithm #explore #fyp #video #tiktok #viral"
    await msg.answer(f"✅ Video havolasi qabul qilindi!\n\nTrenddagi heshteglar:\n{hashtags}\n\n*Bularni kopiyalab videongiz ostiga qo'shing!")

# 2. BOSHQA FUNKSIYALAR
@dp.message(F.text == "📥 Video Silkasi orqali heshteg olish🥶")
async def cmd_heshteg(msg: Message): await msg.answer("Iltimos, video havolasini yuboring.")

@dp.message(F.text == "💳 Pulli sxema paneli")
async def cmd_sxema(msg: Message): 
    await msg.answer("🚀 TOP SXEMA SOTILADI! 🚀\nNarx: 35ming so'm.\nTo'lov qilib chek rasmini yuboring, admin tekshiradi.\nAgar ishlamay qolsa: @roziyev2")

@dp.message(F.text == "📩 Admenga savol yulash")
async def cmd_admin(msg: Message): await msg.answer("Savolingizni yozib qoldiring, admin tez orada javob beradi.")

@dp.message(F.text == "🏎 The Bugatti Chiron Heshteg")
async def cmd_bugatti(msg: Message): await msg.answer("The Bugatti Chiron is a mid-engine two-seater sports car designed and developed in Germany by Bugatti Engineering GmbH...")

@dp.message(F.text == "𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” Heshtegi😇")
async def cmd_eslatma(msg: Message): await msg.answer("𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” 𝘇𝗲𝗿𝗼 𝗲𝘀𝗹𝗮𝘁𝗺𝗮 𝗺𝗼’𝗺𝗶𝗻𝗹𝗮𝗿𝗴𝗮 𝗺𝗮𝗻𝗳𝗮𝗮𝘁 𝘆𝗲𝘁𝗸𝗮𝘇𝘂𝗿... #islam #allah")

@dp.message(F.text == "⏱ Vidiyo qõyish vaqti✅🫠")
async def cmd_vaqt(msg: Message): await msg.answer("Rekga chiqish vaqtlari:\n6:00, 8:00, 11:00, 16:00, 20:00, 22:00, 00:00")

@dp.message(F.text == "💰 Valyuta kursi")
async def cmd_valyuta(msg: Message): await msg.answer("USD: 13,120 UZS")

@dp.message(F.text == "🎮 Oʻyinlar paneli")
async def cmd_oyin(msg: Message):
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Tosh"), KeyboardButton(text="Qaychi"), KeyboardButton(text="Qogoz")]], resize_keyboard=True)
    await msg.answer("Tanlang:", reply_markup=markup)

@dp.message(F.text.in_(["Tosh", "Qaychi", "Qogoz"]))
async def play_game(msg: Message):
    await msg.answer(f"Bot tanladi: {random.choice(['Tosh', 'Qaychi', 'Qogoz'])}")

@dp.message(F.text == "✨ Niklar yaratish paneli")
async def cmd_nik(msg: Message): await msg.answer("Ism va familiyangizni yuboring:")

@dp.message(lambda msg: msg.text and len(msg.text.split()) >= 2)
async def gen_nik(msg: Message):
    await msg.answer(f"Siz uchun nik: @{msg.text.replace(' ', '_')}_{random.choice(NICKS)}")

@dp.message(F.text == "🚀 Tekin nakrutka paneli")
async def cmd_nakrutka(msg: Message):
    if await check_sub(msg.from_user.id):
        await msg.answer("Siz obuna bo'lgansiz! Mana link: https://leofame.com")
    else:
        await msg.answer("Nakrutka uchun kanalga obuna bo'ling!", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Kanalga obuna bo'lish", url="https://t.me/temuzikinsta")], [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]]))

@dp.callback_query(F.data == "check_sub")
async def verify(call: CallbackQuery):
    if await check_sub(call.from_user.id): await call.message.edit_text("Rahmat! Link: https://leofame.com")
    else: await call.answer("Hali obuna bo'lmagansiz!", show_alert=True)

@dp.message(F.photo)
async def handle_photo(msg: Message):
    await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=f"To'lov cheki: @{msg.from_user.username}")
    await msg.answer("✅ Chek qabul qilindi!")

@dp.message(Command("start"))
async def start(msg: Message): await msg.answer("Xush kelibsiz!", reply_markup=get_main_menu())

async def main(): await dp.start_polling(bot)
if __name__ == "__main__": asyncio.run(main())
