import telebot

TOKEN = '8604260086:AAGvY_Y6MALYk8T72zN8cMF7tu2TRdcNCVU'
bot = telebot.TeleBot(TOKEN)

# لیست آیدی‌های عددی ادمین‌ها (خودت و اکانت پشتیبانی)
ADMIN_IDS = [
    6202317657,     # آیدی عددی اول (خودت)
    8304730388       # ⚠️ آیدی عددی اکانت دوم (پشتیبانی) رو اینجا به جای این اعداد بذار
]

SUPPORT_USERNAME = "Sup_Bigbang"  # یوزرنیم پشتیبانی خودت رو بدون @ اینجا بنویس

# منوی محصولات با قیمت‌های جدید
def get_main_markup():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🧬 بانک تست زیست جامع - 400 هزار تومان", callback_data="buy_zist"),
        telebot.types.InlineKeyboardButton("🧪 بانک تست شیمی جامع - 350 هزار تومان", callback_data="shimi"),
        telebot.types.InlineKeyboardButton("💡 بانک تست فیزیک جامع - 320 هزار تومان", callback_data="fizik"),
        telebot.types.InlineKeyboardButton("📐 بانک تست ریاضی جامع - 350 هزار تومان", callback_data="math"),
        telebot.types.InlineKeyboardButton("📦 پکیج کامل (هر ۴ بانک تست) - 1,200,000 تومان (تخفیف ویژه)", callback_data="full_4")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! به ربات بیگ بنگ خوش آمدید.\nمحصول مورد نظرت رو انتخاب کن:", reply_markup=get_main_markup())

@bot.callback_query_handler(func=lambda call: call.data in ["buy_zist", "shimi", "fizik", "math", "full_4"])
def process_buy(call):
    prices = {
        "buy_zist": ("بانک تست زیست جامع", "499,000"),
        "shimi": ("بانک تست شیمی جامع", "449,000"),
        "fizik": ("بانک تست فیزیک جامع", "419,000"),
        "math": ("بانک تست ریاضی جامع", "449,000"),
        "full_4": ("پکیج کامل (هر ۴ بانک تست)", "1,500,000")
    }
    
    item_name, price = prices[call.data]
    
    text = (
        f"💳 خرید {item_name}\n\n"
        f"💰 مبلغ قابل پرداخت: {price} تومان\n\n"
        f"شماره کارت: `5022291535771289` به نام سیدحمیدرضامحسنی راد\n\n"
        "لطفاً واریز کن و عکس فیش رو همینجا بفرست تا بررسی کنم."
    )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=text, parse_mode="Markdown")

@bot.message_handler(content_types=['photo', 'document'])
def handle_receipt(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    
    if username:
        chat_link = f"https://t.me/{username}"
        user_info = f"@{username}"
    else:
        chat_link = "ندارد"
        user_info = "بدون آیدی متنی"
    
    markup = telebot.types.InlineKeyboardMarkup()
    if username:
        markup.add(telebot.types.InlineKeyboardButton("💬 چت مستقیم با کاربر", url=chat_link))
    markup.add(telebot.types.InlineKeyboardButton("✅ تایید فیش (بررسی شد)", callback_data=f"approve_{user_id}"))
    
    caption = (
        f"📩 فیش واریزی جدید!\n\n"
        f"👤 نام: {user_name}\n"
        f"🔗 آیدی: {user_info}\n"
        f"🆔 آی‌دی عددی: `{user_id}`\n\n"
        "برای تایید روی دکمه زیر بزنید."
    )
    
    file_id = message.photo[-1].file_id if message.photo else message.document.file_id
    
    # ارسال فیش به همه ادمین‌های لیست
    for admin_id in ADMIN_IDS:
        try:
            bot.send_photo(admin_id, file_id, caption=caption, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"خطا در ارسال به ادمین {admin_id}: {e}")
    
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی و ارسال سوال", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    bot.send_message(
        message.chat.id, 
        "✅ فیش شما دریافت شد.\n"
        "پس از بررسی توسط مدیریت، دسترسی برای شما ارسال خواهد شد.\n\n"
        "اگر سوالی داری یا می‌خوای پیگیر بشی، از طریق دکمه زیر با پشتیبانی در ارتباط باش:",
        reply_markup=user_markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_user(call):
    # چک کردن اینکه آیا کاربری که دکمه رو زده ادمین هست یا نه
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ شما دسترسی ادمین ندارید!", show_alert=True)
        return
        
    user_id = int(call.data.split("_")[1])
    
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    bot.send_message(
        user_id, 
        "✅ فیش واریزی شما تایید شد!\n"
        "برای دریافت لینک دسترسی یا پشتیبانی از طریق دکمه زیر با ما در ارتباط باشید:", 
        reply_markup=user_markup
    )
    
    bot.edit_message_caption(
        chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        caption=call.message.caption + f"\n\n🟢 **وضعیت: تایید شد توسط ادمین**", 
        parse_mode="Markdown"
    )

print("ربات با موفقیت روشن شد و در حال گوش دادن است...")
bot.infinity_polling()
