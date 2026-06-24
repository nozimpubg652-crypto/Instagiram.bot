import asyncio
import logging
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus

# ================= XAVFSIZ SOZLAMALAR =================
# Token server sozlamalaridan (Environment Variables) avtomatik olinadi
API_TOKEN = os.getenv("8250196324:AAEb807EbczLnTcat3X_wJjd996zGXAx2h8")
ADMIN_ID = 8639222385
KARTA_RAQAM = "9860 1666 5489 5563"
CHANNEL_ID = "@temuzikinsta" 

if not API_TOKEN:
    logging.error("XATOLIK: BOT_TOKEN server sozlamalarida topilmadi!")
    exit(1)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

class BotStates(StatesGroup):
    waiting_for_link = State()
    waiting_for_payment = State()
    waiting_for_broadcast = State()

# ================= MAJBURIY OBUNA LOGIKASI =================
async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except Exception as e:
        logging.error(f"Kanal tekshirishda xato: {e}")
        return False

def sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")],
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="check_sub")]
    ])

# ================= MENYU =================
def get_main_menu(is_admin=False):
    kb = [
        [InlineKeyboardButton(text="🎥 Insta Video Yuklash", callback_data="download")],
        [InlineKeyboardButton(text="💳 Pulli Sxema (To'lov)", callback_data="pay")]
    ]
    if is_admin:
        kb.append([InlineKeyboardButton(text="⚙️ Admin Panel", callback_data="admin_panel")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

# ================= START VA TEKSHIRUV =================
@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    if not await is_subscribed(message.from_user.id):
        await message.answer(f"👋 <b>Xush kelibsiz!</b>\n\nBotdan foydalanish uchun avval kanalimizga obuna bo'ling:", 
                             reply_markup=sub_keyboard(), parse_mode="HTML")
        return

    is_admin = (message.from_user.id == ADMIN_ID)
    await message.answer("<b>Asosiy menyu:</b>\nQuyidagilardan birini tanlang 👇", 
                         reply_markup=get_main_menu(is_admin), parse_mode="HTML")

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        is_admin = (callback.from_user.id == ADMIN_ID)
        await callback.message.edit_text("✅ <b>Obuna tasdiqlandi!</b>\nAsosiy menyu:", 
                                         reply_markup=get_main_menu(is_admin), parse_mode="HTML")
    else:
        await callback.answer("❌ Hali kanalga a'zo bo'lmadingiz!", show_alert=True)

# ================= INSTA YUKLAGICH =================
def download_video(url: str):
    ydl_opts = {'format': 'best', 'outtmpl': 'video_%(id)s.mp4', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

@dp.callback_query(F.data == "download")
async def request_insta_link(callback: types.CallbackQuery, state: FSMContext):
    if not await is_subscribed(callback.from_user.id):
        await callback.message.answer("❌ Avval kanalga a'zo bo'ling!", reply_markup=sub_keyboard())
        return

    await callback.message.edit_text("🎥 <b>Instagram video havolasini yuboring:</b>", parse_mode="HTML")
    await state.set_state(BotStates.waiting_for_link)

@dp.message(BotStates.waiting_for_link)
async def process_insta_link(message: types.Message, state: FSMContext):
    msg = await message.answer("⏳ <i>Video yuklanmoqda, kuting...</i>", parse_mode="HTML")
    try:
        video_path = await asyncio.to_thread(download_video, message.text)
        await bot.send_video(chat_id=message.chat.id, video=types.FSInputFile(video_path), caption="✅ @instapub_bot orqali yuklandi")
        os.remove(video_path) 
    except Exception as e:
        await message.answer("❌ Havolada xatolik bor yoki yopiq (private) akkaunt.")
    
    await msg.delete()
    await state.clear()

# ================= TO'LOV TIZIMI =================
@dp.callback_query(F.data == "pay")
async def request_payment(callback: types.CallbackQuery, state: FSMContext):
    text = f"🚀 <b>Pulli sxema uchun to'lov</b>\n\nKarta raqam: <code>{KARTA_RAQAM}</code>\n\n📸 <i>Iltimos, to'lov qilinganidan so'ng chekni shu yerga rasm qilib yuboring.</i>"
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(BotStates.waiting_for_payment)

@dp.message(BotStates.waiting_for_payment, F.photo)
async def receive_receipt(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    caption = f"🚨 <b>YANGI TO'LOV!</b>\n\nFoydalanuvchi: @{message.from_user.username}\nID: <code>{message.from_user.id}</code>"
    
    await bot.send_photo(chat_id=ADMIN_ID, photo=photo_id, caption=caption, parse_mode="HTML")
    await message.answer("✅ <b>Chek qabul qilindi!</b>\nAdmin tez orada xizmatingizni faollashtiradi.", parse_mode="HTML")
    await state.clear()

# ================= ADMIN PANEL =================
@dp.callback_query(F.data == "admin_panel")
async def open_admin(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Xabar tarqatish (Broadcast)", callback_data="broadcast")]
    ])
    await callback.message.edit_text("⚙️ <b>Admin Panelga xush kelibsiz!</b>\n\nNima qilamiz?", reply_markup=kb, parse_mode="HTML")

@dp.callback_query(F.data == "broadcast")
async def ask_broadcast(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📢 Barcha foydalanuvchilarga yuboriladigan xabarni yozing:")
    await state.set_state(BotStates.waiting_for_broadcast)

@dp.message(BotStates.waiting_for_broadcast)
async def send_broadcast(message: types.Message, state: FSMContext):
    await message.answer("✅ Xabar tarqatish muvaffaqiyatli yakunlandi! (Test rejimi)")
    await state.clear()

# ================= BOTNI ISHGA TUSHIRISH =================
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
