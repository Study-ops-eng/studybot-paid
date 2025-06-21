from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7490240426:AAE_Xub0Lx7gAvZOJ2NTkffVwdnBjj3EDh0"
ADMIN_ID = 6295626651  # ← आपकी Telegram Numeric ID

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Welcome to StudyBot! Type /help to see available commands.")

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Available Commands:
/start - Start the bot
/help - Show this help message
/buy - Get premium access info
/subjects - List available subjects
/notes - Get important study notes
/test - Take a practice test
""")

# Buy Command with Permission Request
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Request Free Access", callback_data=f"request_free:{user.id}:{user.first_name}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💳 To buy premium access, pay ₹49 to UPI ID: 9528165371@amazonpay\nOr request free access from admin 👇", reply_markup=reply_markup)

# Handle Callback Query from Inline Keyboard
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split(":")
    if data[0] == "request_free":
        user_id = int(data[1])
        user_name = data[2]

        # Notify Admin for Approval
        keyboard = [
            [InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user_id}"),
             InlineKeyboardButton("❌ Deny", callback_data=f"deny:{user_id}")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=ADMIN_ID,
            text=f"👤 User {user_name} (ID: {user_id}) is requesting free access. Approve?",
            reply_markup=markup)

        await query.edit_message_text("⏳ Request sent to admin for approval...")

    elif data[0] == "approve":
        target_id = int(data[1])
        await context.bot.send_message(chat_id=target_id, text="✅ You’ve been granted free premium access by admin!")
        await query.edit_message_text("✅ Approved. User has been notified.")
    elif data[0] == "deny":
        target_id = int(data[1])
        await context.bot.send_message(chat_id=target_id, text="❌ Your request for free access was denied.")
        await query.edit_message_text("❌ Denied. User has been notified.")

# Other Commands
async def subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Available Subjects:\n- General Knowledge\n- Reasoning\n- Math\n- Hindi\n- English")

async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Important Notes:\nDownload from: https://t.me/+abc123note")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧪 Practice Test:\nQ1. भारत का पहला राष्ट्रपति कौन था?\nA. राजेंद्र प्रसाद\nB. महात्मा गांधी\nC. नेहरू\nD. अब्दुल कलाम\n\n(Answer: A)")

# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("subjects", subjects))
    app.add_handler(CommandHandler("notes", notes))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.run_polling()

