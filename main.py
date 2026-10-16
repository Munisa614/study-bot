import telebot
from telebot import types

# === SOZLAMALAR ===
BOT_TOKEN = "8932775296:AAGp9ZyYtPvq29iSf71EfEMnVgqBSEPHmxM"  # Tokeningiz
ADMINS = [7372128318, 1309449553]  # Admin ID raqamlari

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# Foydalanuvchi bosqichlarini saqlash uchun vaqtinchalik xotira
user_data = {}


class UserState:
  FULLNAME = 1
  PHONE = 2
  GRADE = 3
  COURSE = 4


# /start buyrug'i
@bot.message_handler(commands=["start"])
def send_welcome(message):
  caption = (
      "🌟 O'QUV MARKAZIGA XUSH KELIBSIZ!\n\n"
      "👨‍🏫 Ilhom Ahmadov — Fizika-matematika fanlari bo'yicha falsafa doktori"
      " (PhD)\n"
      "📖 Matematika fanidan darslarni olib boradi.\n\n"
      "🎁 BIRINCHI DARS BEPUL!\n"
      "👥 Do'stingizni olib keling — 30% BONUS!\n\n"
      "📍 Manzil: Navoiy shahar, 10-mikrorayon, Vatan mahallasi yonida,"
      " Zarafshon uylari, A. Navoiy ko'chasi, 38-A uy.\n"
      "📞 Aloqa: +998 93 571 65 05\n\n"
      "───────────────\n"
      "Ro'yxatdan o'tish uchun, iltimos, Ism va Familiyangizni kiriting:"
  )
  bot.send_message(message.chat.id, caption)
  user_data[message.chat.id] = {"step": UserState.FULLNAME}


# Ism-familiyani qabul qilish
@bot.message_handler(
    func=lambda msg: user_data.get(msg.chat.id, {}).get("step")
    == UserState.FULLNAME
)
def get_fullname(message):
  user_data[message.chat.id]["fullname"] = message.text
  user_data[message.chat.id]["step"] = UserState.PHONE

  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
  markup.add(
      types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
  )

  bot.send_message(
      message.chat.id,
      "Rahmat! Endi telefon raqamingizni yuboring (pastdagi tugmani bosing"
      " yoki yozib yuboring):",
      reply_markup=markup,
  )


# Telefon raqamni qabul qilish
@bot.message_handler(
    func=lambda msg: user_data.get(msg.chat.id, {}).get("step")
    == UserState.PHONE,
    content_types=["text", "contact"],
)
def get_phone(message):
  phone_number = (
      message.contact.phone_number if message.contact else message.text
  )
  user_data[message.chat.id]["phone"] = phone_number
  user_data[message.chat.id]["step"] = UserState.GRADE

  bot.send_message(
      message.chat.id,
      "Nechinchi sinfda o'qiysiz? (masalan: 7-sinf, Abituriyent):",
      reply_markup=types.ReplyKeyboardRemove(),
  )


# Sinfni qabul qilish
@bot.message_handler(
    func=lambda msg: user_data.get(msg.chat.id, {}).get("step")
    == UserState.GRADE
)
def get_grade(message):
  user_data[message.chat.id]["grade"] = message.text
  user_data[message.chat.id]["step"] = UserState.COURSE

  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
  markup.add(
      types.KeyboardButton(
          "📐 Matematika, ingliz tili, rus tili (chuqurlashtirilgan)"
      )
  )
  markup.add(types.KeyboardButton("🏫 Prezident maktabiga tayyorlash"))
  markup.add(types.KeyboardButton("📚 4-11-sinflar uchun qo'shimcha darslar"))
  markup.add(types.KeyboardButton("🎓 Abituriyentlarni tayyorlash"))
  markup.add(
      types.KeyboardButton(
          "📜 Matematika va ingliz tilidan sertifikatga tayyorlash"
      )
  )

  bot.send_message(
      message.chat.id,
      "Qaysi yo'nalish/kurs bo'yicha ta'lim olmoqchisiz? Quyidagi"
      " ro'yxatdan tanlang:",
      reply_markup=markup,
  )


# Kursni tanlash va adminga yuborish
@bot.message_handler(
    func=lambda msg: user_data.get(msg.chat.id, {}).get("step")
    == UserState.COURSE
)
def get_course(message):
  user_data[message.chat.id]["course"] = message.text
  data = user_data[message.chat.id]

  bot.send_message(
      message.chat.id,
      "✅ Rahmat! Arizangiz qabul qilindi.\nTez orada administratorimiz"
      " siz bilan bog'lanadi.",
      reply_markup=types.ReplyKeyboardRemove(),
  )
  username = (
      f"@{message.from_user.username}"
      if message.from_user.username
      else "Mavjud emas"
  )
  admin_text = (
      "📥 Yangi ariza kelib tushdi!\n\n"
      f"👤 Ism-Familiya: {data['fullname']}\n"
      f"📞 Tel: {data['phone']}\n"
      f"🏫 Sinfi/Bosqichi: {data['grade']}\n"
      f"📚 Tanlangan kurs: {data['course']}\n"
      f"🔗 Telegram: {username}"
  )

  for admin_id in ADMINS:
    try:
      bot.send_message(admin_id, admin_text)
    except Exception as e:
      print(f"Admin {admin_id} ga xatolik: {e}")

  # Xotirani tozalash
  user_data.pop(message.chat.id, None)


# Botni ishga tushirish
if __name__ == "__main__":
  print("Bot ishga tushdi...")
  bot.infinity_polling()
