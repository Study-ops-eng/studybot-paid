from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "8144912216:AAEK80FuyYa2hmZQudO-3oKnIYAqrumIKKY"  # 🔁 Use your actual bot token

known_users = [6295626651]  # 🧑‍💼 Approved users list
requested_users = set()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in known_users:
        await update.message.reply_text("📚 Welcome back! You have free access.")
    else:
        await update.message.reply_text("👋 Welcome to StudyBot!\nPlease wait while we check your access...")
        if user_id not in requested_users:
            requested_users.add(user_id)
            await context.bot.send_message(chat_id=6295626651, text=f"🔔 New user {user_id} is requesting access.\nUse /approve {user_id} to approve.")

# /approve command (admin only)
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

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📌 Commands:
/start - Start the bot
/help - Show help
/buy - See subscription info
/subjects - List subjects
/notes - Get notes (premium)
/test - Take test (premium)
""")

# /buy command
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💳 To get premium access, please pay via UPI: 9528165371@amazonpay")

# /subjects command
async def subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 Available Subjects:\n- General Knowledge\n- Math\n- Reasoning\n- Hindi\n- English")

# /notes command with subject options (for premium)
async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in known_users:
        keyboard = [[KeyboardButton("General Knowledge")]]  # Add more subjects later
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("📝 Select subject for notes:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("🔒 This is a premium feature. Use /buy or request access.")

# Handle subject choice for notes
async def handle_subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    subject = update.message.text.strip().lower()

    if user_id not in known_users:
        return

    if subject == "general knowledge":
        await update.message.reply_text("📄 General Knowledge Notes:\nhttps://t.me/padhai_notes/2")
    else:
        await update.message.reply_text("🚧 Notes for this subject are not available yet.")

# /test command
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in known_users:
        await update.message.reply_text("🧠 Test: Coming soon! Stay tuned.")
    else:
        await update.message.reply_text("🔐 Only for premium users. Use /buy to subscribe.")

# App Initialization
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("subjects", subjects))
    app.add_handler(CommandHandler("notes", notes))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_subject_selection))

    app.run_polling()
