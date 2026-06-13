import os
import asyncio
import random
import instaloader
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN") or "TOKENINGIZNI_SHU_YERGA_YOZING"
ADMIN_ID = 8639222385
CHANNEL_ID = "@temuzikinsta"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

# INSTAGRAM VA SXEMA QISMI
@dp.message(F.text.startswith("https://www.instagram.com/"))
async def get_instagram_hashtags(msg: Message):
    url = msg.text
    try:
        L = instaloader.Instaloader()
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        caption = post.caption if post.caption else "Bu videoda matn yo'q."
        await msg.answer(f"✅ **Video matni va heshteglari:**\n\n{caption}")
    except Exception:
        await msg.answer("❌ Uzr, bu videodan matnni olib bo'lmadi.")

@dp.message(F.reply_to_message)
async def admin_replies(msg: Message):
    if msg.from_user.id == ADMIN_ID:
        # Chekka javoblar (/ok yoki /no)
        if msg.text == "/ok":
            user_id = msg.reply_to_message.caption.split("ID: ")[1].split("\n")[0]
            await bot.send_message(user_id, "✅ To'lovingiz tasdiqlandi! Mana sxema: [Sizning maxfiy sxemangiz shu yerda]")
            await msg.answer("✅ Sxema foydalanuvchiga yuborildi.")
        elif msg.text == "/no":
            user_id = msg.reply_to_message.caption.split("ID: ")[1].split("\n")[0]
            await bot.send_message(user_id, "❌ To'lovingiz qabul qilinmadi. Iltimos, admin bilan bog'laning.")
            await msg.answer("✅ Rad etildi.")
        else:
            # Oddiy matnli javob
            try:
                user_id = msg.reply_to_message.caption.split("ID: ")[1].split("\n")[0]
                await bot.send_message(user_id, f"📩 Admindan javob:\n{msg.text}")
                await msg.answer("✅ Javob yuborildi!")
            except:
                user_id = msg.reply_to_message.text.split("ID: ")[1].split("\n")[0]
                await bot.send_message(user_id, f"📩 Admindan javob:\n{msg.text}")
                await msg.answer("✅ Javob yuborildi!")

@dp.message(lambda msg: msg.text and not msg.text.startswith("/") and msg.reply_to_message is None)
async def handle_user_question(msg: Message):
    if msg.text in ["📥 Video Silkasi orqali heshteg olish🥶", "💳 Pulli sxema paneli", "🚀 Tekin nakrutka paneli", "✨ Niklar yaratish paneli"]: return
    await bot.send_message(ADMIN_ID, f"📩 Yangi savol:\nFoydalanuvchi: @{msg.from_user.username}\nID: {msg.from_user.id}\nMatn: {msg.text}")
    await msg.answer("✅ Savolingiz admenga yuborildi!")

@dp.message(F.photo)
async def handle_photo(msg: Message):
    await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=f"To'lov cheki:\nFoydalanuvchi: @{msg.from_user.username}\nID: {msg.from_user.id}")
    await msg.answer("✅ Chek qabul qilindi, admin tekshirmoqda!")

# QOLGAN FUNKSIYALAR
@dp.message(F.text == "📥 Video Silkasi orqali heshteg olish🥶")
async def cmd_heshteg(msg: Message): await msg.answer("Iltimos, video havolasini yuboring.")
@dp.message(F.text == "💳 Pulli sxema paneli")
async def cmd_sxema(msg: Message): await msg.answer("🚀 TOP SXEMA SOTILADI! 🚀\nNarx: 35ming so'm.\n@roziyev2 ga yozing.")
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
async def play_game(msg: Message): await msg.answer(f"Bot tanladi: {random.choice(['Tosh', 'Qaychi', 'Qogoz'])}")
@dp.message(F.text == "✨ Niklar yaratish paneli")
async def cmd_nik(msg: Message): await msg.answer("Ism va familiyangizni yuboring:")
@dp.message(lambda msg: msg.text and len(msg.text.split()) >= 2)
async def gen_nik(msg: Message): await msg.answer(f"Siz uchun nik: @{msg.text.replace(' ', '_')}_{random.choice(NICKS)}")
@dp.message(F.text == "🚀 Tekin nakrutka paneli")
async def cmd_nakrutka(msg: Message):
    if await check_sub(msg.from_user.id): await msg.answer("Siz obuna bo'lgansiz! Mana link: https://leofame.com")
    else: await msg.answer("Nakrutka uchun kanalga obuna bo'ling!", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Kanalga obuna bo'lish", url="https://t.me/temuzikinsta")], [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]]))
@dp.callback_query(F.data == "check_sub")
async def verify(call: CallbackQuery):
    if await check_sub(call.from_user.id): await call.message.edit_text("Rahmat! Link: https://leofame.com")
    else: await call.answer("Hali obuna bo'lmagansiz!", show_alert=True)
@dp.message(Command("start"))
async def start(msg: Message): await msg.answer("Xush kelibsiz!", reply_markup=get_main_menu())

async def main(): 
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__": asyncio.run(main())
