import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- SOZLAMALAR ---
BOT_TOKEN = "8870187278:AAFgc0NaXYe6pasN2CKqDf3hD36CQxFb4Jg"
ADMIN_ID = 8639222385
KARTA_RAQAM = "karta tez kunda (Roziyev)"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ishlatilgan_niklar = set()

class BotStates(StatesGroup):
    reklama_tasdiqlash = State()
    savol_yuborish = State()
    ism_familiya = State()
    chek_kutish = State()

# --- KLAVIATURALAR ---
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Video Silkasi orqali heshteg olish🥶")],
            [KeyboardButton(text="Koyin pulik sxema paneli"), KeyboardButton(text="Admenga savol yulash📩")],
            [KeyboardButton(text="The Bugatti Chiron Heshteg"), KeyboardButton(text="𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” 𝘇𝗲𝗿𝗼 𝗲𝘀𝗹𝗮𝘁𝗺𝗮 𝗺𝗼’𝗺𝗶𝗻𝗹𝗮𝗿𝗴𝗮 Heshtegi😇")],
            [KeyboardButton(text="Vidiyo qõyish vaqti✅🫠"), KeyboardButton(text="Niclar yaratish paneli")],
            [KeyboardButton(text="Oʻyinlar paneli"), KeyboardButton(text="Valyuta kursi")],
            [KeyboardButton(text="Tekin nakurutka paneli"), KeyboardButton(text="📌 Rek heshteglar")]
        ],
        resize_keyboard=True
    )

def get_games_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Tosh"), KeyboardButton(text="Qaychi"), KeyboardButton(text="Qog'oz")],
            [KeyboardButton(text="Orqaga")]
        ],
        resize_keyboard=True
    )

def get_cancel_menu():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Bekor qilish")]], resize_keyboard=True)

# --- 4 TILDAGI HESHTEGLAR PANEL ---
@dp.message(F.text == "📌 Rek heshteglar")
async def hashtag_menu(message: types.Message):
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🇺🇿 O'zbekcha"), KeyboardButton(text="🇷🇺 Ruscha")],
        [KeyboardButton(text="🇬🇧 Inglizcha"), KeyboardButton(text="🇹🇷 Turkcha")],
        [KeyboardButton(text="Orqaga")]
    ], resize_keyboard=True)
    await message.answer("Qaysi tildagi heshteglar kerak?", reply_markup=markup)

@dp.message(F.text == "🇺🇿 O'zbekcha")
async def hash_uz(message: types.Message):
    await message.answer("#reka #trend #uzb #top #foryou #fyp #video")

@dp.message(F.text == "🇷🇺 Ruscha")
async def hash_ru(message: types.Message):
    await message.answer("#рекомендации #рек #тренды #популярное #video #россия")

@dp.message(F.text == "🇬🇧 Inglizcha")
async def hash_en(message: types.Message):
    await message.answer("#explore #viral #trending #reels #foryoupage #instadaily")

@dp.message(F.text == "🇹🇷 Turkcha")
async def hash_tr(message: types.Message):
    await message.answer("#kesfet #öneçıkar #takipet #video #trendler #turkey")

# --- ASOSIY FUNKSIYALAR (Sizning kodingiz) ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}! Instagram TOP botiga xush kelibsiz.", reply_markup=get_main_menu())

@dp.message(F.text == "Video Silkasi orqali heshteg olish🥶")
async def hashtag_request(message: types.Message):
    await message.answer("Instagram havolasini yuboring:")

@dp.message(F.text.contains("instagram.com/"))
async def instagram_link_handler(message: types.Message):
    await message.answer("Yuklanmoqda...")
    await asyncio.sleep(1)
    await message.answer_photo(photo="https://picsum.photos/600/800", caption="Tayyor! Heshteglar avtomatik qo'shildi.")

@dp.message(F.text == "Koyin pulik sxema paneli")
async def pulik_sxema(message: types.Message, state: FSMContext):
    await message.answer(f"Narx: 35 000 so'm. Karta: {KARTA_RAQAM}. Chek yuboring!", reply_markup=get_cancel_menu())
    await state.set_state(BotStates.chek_kutish)

@dp.message(BotStates.chek_kutish, F.photo)
async def chek_qabul_qilish(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"accept_{message.from_user.id}"),
        InlineKeyboardButton(text="❌ Rad etish", callback_data=f"deny_{message.from_user.id}")]])
    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"Yangi chek! ID: {message.from_user.id}", reply_markup=keyboard)
    await message.answer("Chek qabul qilindi, kuting.")
    await state.clear()

@dp.callback_query(F.data.startswith("accept_"))
async def admin_accept(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, "✅ To'lov tasdiqlandi!")
    await callback.message.edit_caption(caption="Tasdiqlandi ✅")

@dp.callback_query(F.data.startswith("deny_"))
async def admin_deny(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, "❌ Rad etildi.")
    await callback.message.edit_caption(caption="Rad etildi ❌")

@dp.message(F.text == "Admenga savol yulash📩")
async def ask_admin_start(message: types.Message, state: FSMContext):
    await message.answer("Savolingizni yozing:", reply_markup=get_cancel_menu())
    await state.set_state(BotStates.savol_yuborish)

@dp.message(BotStates.savol_yuborish)
async def ask_admin_forward(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📩 Yangi Savol: {message.text}")
    await message.answer("Yuborildi!", reply_markup=get_main_menu())
    await state.clear()

@dp.message(F.text == "The Bugatti Chiron Heshteg")
async def bugatti_chiron(message: types.Message):
    await message.answer("Bugatti Chiron - bu o'rtadagi dvigatelli sport avtomobili.")

@dp.message(F.text == "𖣔”𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴” 𝘇𝗲𝗿𝗼 𝗲𝘀𝗹𝗮𝘁𝗺𝗮 𝗺𝗼’𝗺𝗶𝗻𝗹𝗮𝗿𝗴𝗮 Heshtegi😇")
async def islamic_hashtag(message: types.Message):
    await message.answer("𖣔 𝗘𝘀𝗹𝗮𝘁𝗶𝗻𝗴... \n#islam #namaz #allahuakbar")

@dp.message(F.text == "Vidiyo qõyish vaqti✅🫠")
async def video_time(message: types.Message):
    await message.answer("6:00, 11:00, 16:00, 20:00, 22:00, 00:00")

@dp.message(F.text == "Niclar yaratish paneli")
async def nick_panel_start(message: types.Message, state: FSMContext):
    await message.answer("Ism kiriting:", reply_markup=get_cancel_menu())
    await state.set_state(BotStates.ism_familiya)

@dp.message(BotStates.ism_familiya)
async def nick_generator(message: types.Message, state: FSMContext):
    await message.answer(f"@{message.text}_top_777")
    await state.clear()

@dp.message(F.text == "Oʻyinlar paneli")
async def games_panel(message: types.Message):
    await message.answer("Tanlang:", reply_markup=get_games_menu())

@dp.message(F.text.in_(["Tosh", "Qaychi", "Qog'oz"]))
async def play_game(message: types.Message):
    bot_choice = random.choice(["Tosh", "Qaychi", "Qog'oz"])
    await message.answer(f"Bot: {bot_choice}")

@dp.message(F.text == "Valyuta kursi")
async def currency_rate(message: types.Message):
    await message.answer("USD: 13,120 UZS")

@dp.message(F.text == "Tekin nakrutka paneli")
async def free_nakrutka(message: types.Message):
    await message.answer("5 ta do'st taklif qiling!")

@dp.message(F.text == "Orqaga")
async def back_to_main(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu())

@dp.message(F.text == "Bekor qilish")
async def cancel_action(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
