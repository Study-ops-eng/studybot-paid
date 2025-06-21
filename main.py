from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# Set your bot token and admin ID
TOKEN = "7490240426:AAE_Xub0Lx7gAvZOJ2NTkffVwdnBjj3EDh0"
ADMIN_ID = 6295626651

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Welcome to StudyBot! Type /help to see available commands.")

# /help command
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

# /buy command
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[
        InlineKeyboardButton("Request Free Access", callback_data=f"request:{user.id}:{user.first_name}")
    ]]
    await update.message.reply_text(
        "💳 To buy premium access, pay ₹49 to UPI: 9528165371@amazonpay\n\n"
        "Or request free access from admin 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Handle callback buttons
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split(":")
    action = parts[0]

    if action == "request":
        user_id = int(parts[1])
        user_name = parts[2]
        keyboard = [[
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user_id}"),
            InlineKeyboardButton("❌ Deny", callback_data=f"deny:{user_id}")
        ]]
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"👤 {user_name} (ID: {user_id}) is requesting free access.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await query.edit_message_text("✅ Request sent to admin for approval.")

    elif action == "approve":
        user_id = int(parts[1])
        await context.bot.send_message(chat_id=user_id, text="✅ Admin has approved your free premium access!")
        await query.edit_message_text("👍 Approved.")

    elif action == "deny":
        user_id = int(parts[1])
        await context.bot.send_message(chat_id=user_id, text="❌ Your free access request was denied by the admin.")
        await query.edit_message_text("🚫 Denied.")

# /subjects command
async def subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Subjects:\n- GK\n- Math\n- Hindi\n- Reasoning\n- English")

# /notes command
async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Notes are available at: https://t.me/+abc123note")

# /test command
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 Sample Test:\n"
        "Q1. भारत का पहला राष्ट्रपति कौन था?\n"
        "A. राजेंद्र प्रसाद\n"
        "B. गांधी जी\n"
        "C. अब्दुल कलाम\n"
        "D. नेहरू\n"
        "उत्तर: A"
    )

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


