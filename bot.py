import telebot

TOKEN = '8604260086:AAGvY_Y6MALYk8T72zN8cMF7tu2TRdcNCVU'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 6202317657  # آیدی عددی دقیق خودت
SUPPORT_USERNAME = "Hamid9981"  # یوزرنیم پشتیبانی خودت رو بدون @ اینجا بنویس (مثلا: Hamid_Support)

# منوی محصولات با تخفیف‌های ویژه تا ۳۱ مرداد
def get_main_markup():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🧬 بانک تست زیست جامع - ۳۵۹ هزار تومان (تخفیف ویژه)", callback_data="bio"),
        telebot.types.InlineKeyboardButton("🧪 بانک تست شیمی جامع - ۳۱۹ هزار تومان (تخفیف ویژه)", callback_data="chem"),
        telebot.types.InlineKeyboardButton("💡 بانک تست فیزیک جامع - ۲۹۹ هزار تومان (تخفیف ویژه)", callback_data="phys"),
        telebot.types.InlineKeyboardButton("📐 بانک تست ریاضی جامع - ۳۱۹ هزار تومان (تخفیف ویژه)", callback_data="math"),
        telebot.types.InlineKeyboardButton("📦 پکیج کامل (هر ۴ بانک تست) - ۱۰۵۰ هزار تومان (تخفیف ویژه‌تر)", callback_data="all_pack_v2")
    )
    return markup
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! به ربات بیگ بنگ خوش آمدید.\nمحصول مورد نظرت رو انتخاب کن:", reply_markup=get_main_markup())

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_") or call.data in ["shimi", "fizik", "full"])
def process_buy(call):
    prices = {
        "buy_zist": ("زیست جامع", "359,000"),
        "shimi": ("شیمی جامع", "319,000"),
        "fizik": ("فیزیک جامع", "299,000"),
        "full": ("پکیج کامل (هر سه با تخفیف)", "800,000")
    }
    
    item_name, price = prices[call.data]
    
    text = (
        f"💳 خرید {item_name}\n\n"
        f"💰 مبلغ قابل پرداخت با تخفیف: {price} تومان\n"
        f"⚠️ توجه: این تخفیف فقط تا ۳۱ مرداد معتبر است.\n\n"
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
    bot.send_photo(ADMIN_ID, file_id, caption=caption, reply_markup=markup, parse_mode="Markdown")
    
    # اینجا به کاربر به جای پیام معمولی، دکمه ارتباط با پشتیبانی رو می‌دیم
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی و ارسال سوال", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    bot.send_message(
        message.chat.id, 
        "✅ فیش شما دریافت شد.\n"
        "پس از بررسی توسط مدیریت، دسترسی برای شما ارسال خواهد شد.\n\n"
        "اگر سوالی داری یا می‌وای پیگیر بشی، از طریق دکمه زیر با پشتیبانی در ارتباط باش:",
        reply_markup=user_markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_user(call):
    user_id = int(call.data.split("_")[1])
    
    # پیامی که به کاربر بعد از تایید فیش میره (شامل لینک پشتیبانی یا لینک فایل)
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
        caption=call.message.caption + "\n\n🟢 **وضعیت: تایید شد**", 
        parse_mode="Markdown"
    )

print("ربات با موفقیت روشن شد و در حال گوش دادن است...")
bot.infinity_polling()
