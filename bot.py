from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random

API_TOKEN = "8514343100:AAG70S7e4qlS1B4j0FxRpgppVGMYFvhLYPY"
ADMIN_ID = 8639222385

storage = MemoryStorage()
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

# --- Ma'lumotlarni saqlash xotirasi ---
USED_NICKS = set()  # Ishlatilgan niklar takrorlanmasligi uchun
added_counts = {}   # Kim qancha odam qo'shganini hisoblash xotirasi

# --- FSM (Holatlar) ---
class BotStates(StatesGroup):
    waiting_for_video_link = State()
    waiting_for_chek = State()
    waiting_for_admin_question = State()
    waiting_for_nick_name = State()

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

# --- Super menyu tugmalari ---
super_menu = InlineKeyboardMarkup(row_width=2)
buttons = [
    ("🎥 Video Silkasi", "video"),
    ("⚡ Tekin Nakrutka", "nakrutka"),
    ("🚀 Pulli sxema paneli", "sxema"),
    ("📩 Admenga savol yuborish", "admin"),
    ("🆔 Nik yaratish", "nic"),
    ("🎮 O‘yinlar paneli", "oyin"),
    ("💱 Valyuta kursi", "valyuta"),
    ("🏎 Bugatti Chiron", "bugatti"),
    ("𖣔 Eslatmalar", "eslatma"),
    ("Vidiyo qõyish vaqti✅🫠", "vaqt"),
    ("🔥 Rek Sirlari (1M+)", "insta_secrets"),
    ("📊 Statistika", "stat"),
    ("🔥 Trend heshteglar", "trend"),
    ("📅 Kunlik maslahatlar", "maslahat"),
    ("🌤 Ob-havo paneli", "obhavo"),
    ("🧩 Mini-quiz", "quiz"),
    ("🎵 Musiqa tavsiyalari", "music"),
    ("📢 Reklama paneli", "reklama"),
    ("⭐ VIP reklama", "vip"),
    ("🎁 Sovg‘a o‘yini", "sovga"),
    ("📚 Kitob tavsiyalari", "kitob"),
    ("🧠 Bilim testi", "test"),
    ("🎬 Kino tavsiyalari", "kino"),
    ("🍔 Retsept paneli", "retsept"),
    ("🧮 Matematika o‘yini", "math"),
    ("🎲 Random generator", "random"),
    ("📖 Hadis paneli", "hadis"),
    ("🧘 Zikr paneli", "zikr"),
    ("🛠 Developer tools", "dev"),
    ("🕹 Mini-game Arcade", "arcade"),
    ("📜 Qur’on oyatlari", "quron"),
    ("🧾 Tarixiy faktlar", "tarix"),
    ("⚽ Sport yangiliklari", "sport"),
    ("🚀 Texnologiya yangiliklari", "tech"),
    ("🎨 Meme generator", "meme"),
    ("🧑‍🎓 Inglizcha so‘zlar", "english"),
    ("🎤 Sitata paneli", "sitata"),
    ("🧑‍🍳 Oshpazlik o‘yini", "oshpaz"),
    ("🎯 Maqsadlar paneli", "maqsad")
]

for text, data in buttons:
    super_menu.add(InlineKeyboardButton(text, callback_data=data))

# --- Kanalga kim odam qo'shsa avtomatik hisoblash ---
@dp.chat_member_handler()
async def track_channel_adds(chat_member: types.ChatMemberUpdated):
    if chat_member.chat.username == "temuzikinsta":
        inviter = chat_member.from_user.id
        if chat_member.new_chat_member.status == "member" and chat_member.old_chat_member.status in ["left", "kicked", None]:
            if inviter != chat_member.new_chat_member.user.id:
                added_counts[inviter] = added_counts.get(inviter, 0) + 1

# --- Start komandasi ---
@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton("📢 Obuna bo‘lish", url="https://t.me/temuzikinsta"))
        keyboard.add(InlineKeyboardButton("✅ Tekshirdim", callback_data="check_sub"))
        await message.answer("❗ Botdan foydalanish uchun avval kanalga obuna bo‘ling:", reply_markup=keyboard)
    else:
        await message.answer("Super menyu:", reply_markup=super_menu)

@dp.callback_query_handler(lambda c: c.data == "check_sub", state="*")
async def process_check_sub(callback_query: types.CallbackQuery):
    if await check_subscription(callback_query.from_user.id):
        await callback_query.message.answer("✅ Obuna tasdiqlandi!", reply_markup=super_menu)
    else:
        await callback_query.answer("❌ Hali obuna bo‘lmadingiz!", show_alert=True)

# --- Tugmalar funksiyalari ---
@dp.callback_query_handler(lambda c: True, state="*")
async def process_all(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data == "video":
        await BotStates.waiting_for_video_link.set()
        await callback_query.message.answer("🎥 Instagram video havolasini (linkini) yuboring, men sizga unga mos trend heshteglarni tayyorlab beraman:")
        await callback_query.answer()

    elif data == "sxema":
        await BotStates.waiting_for_chek.set()
        text = (
            "🚀 <b>TOP SXEMA SOTILADI!</b> 🚀\n"
            "Videolaringiz TOPga chiqishini xohlaysizmi? 🎥\n\n"
            "Bu maxsus sinovdan o‘tgan sxema orqali sizning videolaringiz algoritmda yuqoriga ko‘tariladi, "
            "ko‘rishlar va obunachilar soni esa keskin oshadi! 📈\n"
            "✅ 100% ishlaydigan va tekshirilgan usul\n"
            "✅ Har qanday kontent uchun mos\n"
            "✅ To‘liq yo‘riqnoma bilan birga beriladi\n"
            "✅ Tez va ishonchli natija kafolatlangan\n\n"
            "💼 Videolaringizni trendga chiqarish, ko‘rishlarni oshirish va auditoriya kengaytirish uchun eng samarali yo‘l!\n\n"
            "💰 Narx: (35ming so'm)\n"
            "💳 Karta raqam: <code>9860 1666 5489 5563</code>\n\n"
            "💥 Endi sizning navbatingiz — videolaringizni trendga chiqaring! ⚡ "
            "<b>toʻlov qilib chek rasimini shu yerga yuborin</b> admin tekshirb bot orqali tashlaydi.\n"
            "Agar ishlamay qolsa @roziyev2"
        )
        await callback_query.message.answer(text)
        await callback_query.answer()

    elif data == "admin":
        await BotStates.waiting_for_admin_question.set()
        await callback_query.message.answer("📩 Admenga yubormoqchi bo'lgan savolingizni yoki xabaringizni yozib yuboring:")
        await callback_query.answer()

    elif data == "nic":
        await BotStates.waiting_for_nick_name.set()
        await callback_query.message.answer("🆔 Nik yaratish uchun Ism va Familiyangizni kiriting:")
        await callback_query.answer()

    elif data == "bugatti":
        bugatti_text = (
            "Here's the information about the Bugatti Chiron:\n\n"
            "The Bugatti Chiron is a mid-engine two-seater sports car designed and developed in Germany by Bugatti Engineering GmbH\n\n"
            "CRISGIRLY\n\n"
            "The successor to the Bugatti Veyron, [9] the Chiron was first shown at the Geneva Motor Show on 1 March 2016.\n\n"
            "The car's design was initially previewed with the Bugatti Vision Gran Turismo concept car unveiled at the 2015 Frankfurt Auto Show.\n\n"
            "The engine in the most powerful variant of its predecessor, the Veyron Super Sport generates 221 kW (296 hp; 300 PS) less than the new Chiron, "
            "while the engine in the original Veyron generates 367 kW (492 hp; 499 PS) less power\n\n"
            "The Chiron was recreated in Lego as 2018's annual Technic sports car. It was released on 1 June 2018 as a 1:8 scale model with 3,600 individual parts."
        )
        await callback_query.message.answer(bugatti_text)
        await callback_query.answer()

    elif data == "eslatma":
        eslatma_text = (
            "𖣔”𝖤𝗌𝗅𝖺𝗍𝗂𝗇𝗀” 𝗓𝖾𝗋𝗈 𝖾𝗌𝗅𝖺tplari 𝗆𝗈’𝗆𝗂𝗇𝗅𝖺𝗋𝗀𝖺 𝗆𝖺𝗇𝖿𝖺𝖺𝗍 𝗒𝖾𝗍𝗄𝖺𝗓𝗎𝗋. (Zarriyot surasi, 55 ) ___\n"
            "Alhamdulillah - Barcha maqtov Allohga...\n"
            "Alloh Akbar - Alloh buyukdir...\n\n"
            "#namaz #islam #quran #subhanallah #alhamdulillah"
        )
        await callback_query.message.answer(eslatma_text)
        await callback_query.answer()

    elif data == "vaqt":
        vaqt_text = (
            "Rekgа chiqish vaqtlari😊❤️\n"
            "6:00✅ | 8:00🫵 | 11:00🫶\n"
            "16:00🤍 | 20:00💋 | 22:00 🖤\n"
            "00:00 ❤️\n\n"
            "Shu vaqtda qoysela aktiv norm bolа𝗱𝗶"
        )
        await callback_query.message.answer(vaqt_text)
        await callback_query.answer()

    elif data == "insta_secrets":
        secrets_text = (
            "🔥 <b>INSTAGRAMDA MILLIONLIK REKKA CHIQISH SIRLARI</b> 🔥\n\n"
            "1️⃣ <b>Sirlar va Nastroyka (Sozlamalar):</b>\n"
            "• Profilingizda Highest quality yuklashni yoqing.\n"
            "• Videoning dastlabki 3 soniyasida qiziqarli gap ishlating."
        )
        await callback_query.message.answer(secrets_text)
        await callback_query.answer()

    elif data == "oyin":
        game_menu = InlineKeyboardMarkup(row_width=3)
        game_menu.add(
            InlineKeyboardButton("✊ Tosh", callback_data="rps_tosh"),
            InlineKeyboardButton("✌️ Qaychi", callback_data="rps_qaychi"),
            InlineKeyboardButton("✋ Qog'oz", callback_data="rps_qogoz")
        )
        await callback_query.message.answer("🎮 Tosh-Qaychi-Qog'oz o'yini! Tanlang:", reply_markup=game_menu)
        await callback_query.answer()

    elif data == "valyuta":
        await callback_query.message.answer("💱 Joriy Valyuta Kurslari:\n\n💵 1 USD = 12,850 so'm\n💶 1 EUR = 13,950 so'm\n🪙 1 RUB = 145 so'm")
        await callback_query.answer()

    elif data == "nakrutka":
        current_adds = added_counts.get(user_id, 0)
        check_menu = InlineKeyboardMarkup()
        check_menu.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_nakrutka_shares"))
        
        await callback_query.message.answer(
            f"⚡ Tekin nakrutka paneli ⚡\n\n"
            f"<b>Shart:</b> @temuzikinsta kanaliga 5 ta do‘stni qo‘shishingiz kerak.\n"
            f"Siz hozirgacha qo'shgan odamlar soni: <b>{current_adds}/5</b>", 
            reply_markup=check_menu
        )
        await callback_query.answer()

    else:
        responses = {
            "stat": "📊 Statistika: Foydalanuvchilar soni va tugma bosishlar yuklanmoqda...",
            "trend": "🔥 Trend heshteglar:\n#viral #explore #fyp #instagood #reels",
            "maslahat": random.choice(["Bugun ko‘proq sabr qiling.", "Harakat qilgan odam albatta muvaffaqiyatga erishadi.", "Yaxshi niyat – yaxshi natija."]),
            "obhavo": "🌤 Ob-havo: Toshkent – 34°C, quyoshli.",
            "quiz": "🧩 Savol: O‘zbekiston poytaxti qaysi?\nA) Samarqand\nB) Toshkent\nC) Buxoro",
            "music": "🎵 Musiqa tavsiyasi: Sevara Nazarkhan – Yor-yor",
            "reklama": "📢 Reklama paneli: Reklama joylashtirish shartlari.",
            "vip": "⭐ VIP reklama xizmatlari ko'rsatkichi.",
            "sovga": "🎁 Sovg‘a o‘yini: Random tanlov yaqin kunlarda start oladi.",
            "kitob": "📚 Kitob tavsiyasi: Paulo Coelho – Alkimyogar",
            "test": "🧠 Bilim testi: Yaqin daqiqalarda ochiladi.",
            "kino": "🎬 Kino tavsiyasi: Inception (2010)",
            "retsept": "🍔 Retsept: Palov – guruch, sabzi, go‘sht, piyoz.",
            "math": f"🧮 Misolni yeching: {random.randint(1,10)} + {random.randint(1,10)}",
            "random": f"🎲 Tasodifiy son: {random.randint(1,100)}",
            "hadis": "📖 Hadis: “Eng yaxshi odam – odamlarga foydasi tegadiganidir.”",
            "zikr": "🧘 Zikr: Subhanallah 🌸 Alhamdulillah 🌸 Allohu Akbar 🌸",
            "dev": "🛠 Developer tools: Python va aiogram boyicha yordam.",
            "arcade": "🕹 Mini-game Arcade: Tez kunda yangi o'yinlar qo'shiladi.",
            "quron": "📜 Qur’on oyati: “Albatta, namoz mo‘minlarga vaqtida farz qilingan.” (Niso 103)",
            "tarix": "🧾 Tarixiy fakt: 1969-yilda odam birinchi marta Oyga chiqdi.",
            "sport": "⚽ Sport yangiliklari: O‘zbekiston terma jamoasi g‘alaba qozondi.",
            "tech": "🚀 Texno yangiliklar: O‘zbekiston 5G tarmog‘ini kengaytirmoqda.",
            "meme": "🎨 Meme generator: Tez kunda mem yaratish funksiyasi qo‘shiladi!",
            "english": "🧑‍🎓 Inglizcha so‘zlar: 'Perseverance' – Qat'iyat, matonat.",
            "sitata": "🎤 Sitata: 'Harakat qilgan odam albatta muvaffaqiyatga erishadi.'",
            "oshpaz": "🧑‍🍳 Oshpazlik o‘yini: Taom tayyorlash simulyatori.",
            "maqsad": "🎯 Maqsadlar paneli: Bugungi maqsadingizni yozib qoldiring!"
        }
        if data in responses:
            await callback_query.message.answer(responses[data])
        await callback_query.answer()

# --- Tekin Nakrutka Tekshirish ---
@dp.callback_query_handler(lambda c: c.data == "check_nakrutka_shares", state="*")
async def check_nakrutka_status(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    current_adds = added_counts.get(user_id, 0)
    
    if current_adds >= 5:
        link_text = (
            "Leofame\n"
            "https://leofame.com\n"
            "Free Instagram Views - Instant [%100 FREE & Safe]"
        )
        await callback_query.message.answer(f"✅ Shart bajarildi! Mana sizning havolaingiz:\n\n{link_text}")
    else:
        await callback_query.answer(f"❌ Shart bajarilmadi! Hali 5 ta odam qo'shmadingiz. (Hozir: {current_adds} ta)", show_alert=True)

# --- Tosh Qaychi Qog'oz O'yini Logikasi ---
@dp.callback_query_handler(lambda c: c.data.startswith("rps_"), state="*")
async def play_rps(callback_query: types.CallbackQuery):
    user_choice = callback_query.data.split("_")[1]
    bot_choices = ["tosh", "qaychi", "qogoz"]
    
    rand_val = random.random()
    if rand_val < 0.1:
        bot_choice = user_choice
    else:
        if user_choice == "tosh":
            bot_choice = "qaychi" if rand_val < 0.6 else "qogoz"
        elif user_choice == "qaychi":
            bot_choice = "qogoz" if rand_val < 0.6 else "tosh"
        else:
            bot_choice = "tosh" if rand_val < 0.6 else "qaychi"

    emojis = {"tosh": "✊ Tosh", "qaychi": "✌️ Qaychi", "qogoz": "✋ Qog'oz"}
    
    result = ""
    if user_choice == bot_choice:
        result = "🤝 Do'stlik g'alaba qozondi (Tenglik)!"
    elif (user_choice == "tosh" and bot_choice == "qaychi") or \
         (user_choice == "qaychi" and bot_choice == "qogoz") or \
         (user_choice == "qogoz" and bot_choice == "tosh"):
        result = "🎉 Siz yutdingiz! Tabriklaymiz!"
    else:
        result = "🤖 Bot yutdi! Keyingi safar omad keladi."

    await callback_query.message.answer(
        f"Sizning tanlovingiz: {emojis[user_choice]}\n"
        f"Botning tanlovingiz: {emojis[bot_choice]}\n\n"
        f"<b>{result}</b>"
    )
    await callback_query.answer()

# --- Video Silkasi Input Handler ---
@dp.message_handler(state=BotStates.waiting_for_video_link, content_types=types.ContentTypes.TEXT)
async def process_video_link(message: types.Message, state: FSMContext):
    link = message.text
    if "instagram.com" in link:
        viral_hashtags = "#viral #explore #fyp #instagram #reels #trend #uzb #top #rek #trending #reelsuz"
        await message.answer(f"✅ Havola qabul qilindi! Videongiz uchun trend heshteglar:\n\n<code>{viral_hashtags}</code>\n\nNusxa olib ishlating!")
    else:
        await message.answer("❌ Bu to'g'ri Instagram havolasi emas. Iltimos qaytadan urining yoki /start bosing.")
    await state.finish()

# --- Pulli Sxema Chek Yuborish ---
@dp.message_handler(state=BotStates.waiting_for_chek, content_types=types.ContentTypes.PHOTO)
async def process_chek_photo(message: types.Message, state: FSMContext):
    user_info = f"💰 Yangi To'lov!\nID: {message.from_user.id}\nUsername: @{message.from_user.username}"
    await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id, caption=user_info)
    
    await message.answer("✅ Rasm (chek) qabul qilindi va admenga yuborildi! Admin tez orada tekshirib sxemani bot orqali yuboradi.")
    await state.finish()

# --- Admenga Savol Yuborish ---
@dp.message_handler(state=BotStates.waiting_for_admin_question, content_types=types.ContentTypes.TEXT)
async def process_admin_question(message: types.Message, state: FSMContext):
    question_text = f"📩 <b>Yangi savol keldi!</b>\nFrom ID: {message.from_user.id}\nUsername: @{message.from_user.username}\n\nSavol: {message.text}"
    await bot.send_message(chat_id=ADMIN_ID, text=question_text)
    
    await message.answer("✅ Savolingiz muvaffaqiyatli yuborildi. Admin tez orada javob beradi!")
    await state.finish()

# --- 1 Millionlik Takrorlanmas Niklar Generator Logikasi ---
@dp.message_handler(state=BotStates.waiting_for_nick_name, content_types=types.ContentTypes.TEXT)
async def process_nick_generation(message: types.Message, state: FSMContext):
    name_parts = message.text.split()
    first_name = name_parts[0] if len(name_parts) > 0 else "User"
    
    prefixes = ["Top", "UzB", "Real", "The", "King", "Mega", "Star", "Cyber", "Shadow", "Alpha", "Pro", "Neo", "Leo", "Lux"]
    suffixes = ["_X", "_777", "_pro", "_off", "_boss", "_prime", "_king", "_uz", "_maker", "_v", "_one", "_mafia"]
    
    generated_nick = None
    for _ in range(100):
        pref = random.choice(prefixes)
        suff = random.choice(suffixes)
        rand_num = random.randint(1000, 9999)
        
        format_type = random.randint(1, 3)
        if format_type == 1:
            candidate = f"{pref}_{first_name}{suff}"
        elif format_type == 2:
            candidate = f"{first_name}_{rand_num}{suff}"
        else:
            candidate = f"{pref}_{first_name}_{rand_num}"
            
        if candidate not in USED_NICKS:
            generated_nick = candidate
            USED_NICKS.add(candidate)  # Mana shu qatordagi xato to'g'rilandi!
            break

    if generated_nick:
        await message.answer(f"🆔 Siz uchun maxsus takrorlanmas nik:\n\n<code>{generated_nick}</code>\n\nNusxa olish uchun ustiga bosing!")
    else:
        await message.answer("⚠️ Hozircha nik yaratib bo'lmadi, iltimos qaytadan urining.")
    await state.finish()

# --- Botni ishga tushirish (Doimiy Polling) ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
