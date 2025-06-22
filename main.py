from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8144912216:AAEK80FuyYa2hmZQudO-3oKnIYAqrumIKKY"

# 🔐 Known users who get free access after approval
known_users = [6295626651]  # 🧑‍💼 Add your Telegram numeric ID here (already added)
requested_users = set()

# 🔗 Notes links per subject
notes_links = {
    "General Knowledge": "https://t.me/study_notes_channel/1",
    "Reasoning": "https://t.me/study_notes_channel/2",
    "Math": "https://t.me/study_notes_channel/3",
    "Hindi": "https://t.me/study_notes_channel/4",
    "English": "https://t.me/study_notes_channel/5"
}

# 📍 START command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in known_users:
        await update.message.reply_text("📚 Welcome back! You have free access.")
    else:
        await update.message.reply_text("👋 Welcome to StudyBot!\nPlease wait while we check your access...")
        if user_id not in requested_users:
            requested_users.add(user_id)
            await context.bot.send_message(chat_id=6295626651, text=f"🔔 New user {user_id} is requesting free access. Use /approve {user_id} to approve.")

# ✅ APPROVE command
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != "6295626651":
        await update.message.reply_text("❌ You are not authorized to approve users.")
        return
    if context.args:
        new_user = int(context.args[0])
        known_users.append(new_user)
        await update.message.reply_text(f"✅ Approved user: {new_user}")
        await context.bot.send_message(chat_id=new_user, text="🎉 You have been granted free access to StudyBot!")
    else:
        await update.message.reply_text("❗Usage: /approve <user_id>")

# 📄 HELP command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📌 Commands:
/start - Start the bot
/help - Show this help
/buy - See subscription info
/subjects - List all subjects
/notes - Get notes (premium)
/test - Take test (premium)
""")

# 💰 BUY command
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💳 To get premium access, please pay using UPI ID: 9528165371@amazonpay")

# 📚 SUBJECTS command
async def subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 Available Subjects:\n- General Knowledge\n- Reasoning\n- Math\n- Hindi\n- English")

# 📝 NOTES command (with subject selection for premium users)
async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in known_users:
        keyboard = [
            [InlineKeyboardButton(subject, callback_data=subject)] for subject in notes_links.keys()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("📑 Please choose a subject to get notes:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("🔒 This is a premium feature. Use /buy or request access.")

# 🧾 Callback handler for subject selection
async def notes_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data
    link = notes_links.get(subject, "Link not found.")
    await query.edit_message_text(text=f"📄 {subject} Notes:\n{link}")

# 🧪 TEST command (premium)
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in known_users:
        await update.message.reply_text("🧠 Test: Coming soon! Follow channel for updates.")
    else:
        await update.message.reply_text("🔐 Only for premium users. Use /buy to subscribe.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("subjects", subjects))
    app.add_handler(CommandHandler("notes", notes))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CallbackQueryHandler(notes_callback))
    app.run_polling()
