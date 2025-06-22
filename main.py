
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
from telegram.ext import ConversationHandler

TOKEN = "8144912216:AAEK80FuyYa2hmZQudO-3oKnIYAqrumIKKY"

known_users = [6295626651]
requested_users = set()
NOTES_SELECTION = range(1)

notes_links = {
    "à¤¸à¤¾à¤®à¤¾à¤¨à¥à¤¯ à¤œà¥à¤žà¤¾à¤¨ (General Knowledge)": "https://t.me/study_notes_channel/1",
    "à¤—à¤£à¤¿à¤¤ (Math)": "https://t.me/study_notes_channel/2",
    "à¤°à¥€à¤œà¤¨à¤¿à¤‚à¤— (Reasoning)": "https://t.me/study_notes_channel/3",
    "à¤¹à¤¿à¤‚à¤¦à¥€ (Hindi)": "https://t.me/study_notes_channel/4",
    "à¤‡à¤‚à¤—à¥à¤²à¤¿à¤¶ (English)": "https://t.me/study_notes_channel/5"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in known_users:
        await update.message.reply_text("ðŸ“š Welcome back! You have free access.")
    else:
        await update.message.reply_text("ðŸ‘‹ Welcome to StudyBot!\nPlease wait while we check your access...")
        if user_id not in requested_users:
            requested_users.add(user_id)
            await context.bot.send_message(chat_id=6295626651, text=f"ðŸ”” New user {user_id} is requesting free access. Use /approve {user_id} to approve.")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != "6295626651":
        await update.message.reply_text("âŒ You are not authorized to approve users.")
        return
    if context.args:
        new_user = int(context.args[0])
        known_users.append(new_user)
        await update.message.reply_text(f"âœ… Approved user: {new_user}")
        await context.bot.send_message(chat_id=new_user, text="ðŸŽ‰ You have been granted free access to StudyBot!")
    else:
        await update.message.reply_text("â—Usage: /approve <user_id>")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""ðŸ“Œ Commands:
/start - Start the bot
/help - Show this help
/buy - See subscription info
/subjects - List all subjects
/notes - Get notes (premium)
/test - Take test (premium)""")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ðŸ’³ To get premium access, please pay using UPI ID: 9528165371@amazonpay")

async def subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ðŸ“˜ Available Subjects:\n- General Knowledge\n- Reasoning\n- Math\n- Hindi\n- Current Affairs")

async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in known_users:
        await update.message.reply_text("ðŸ”’ This is a premium feature. Use /buy or request access.")
        return ConversationHandler.END

    buttons = [[KeyboardButton(sub)] for sub in notes_links.keys()]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("ðŸ“ à¤•à¥ƒà¤ªà¤¯à¤¾ à¤µà¤¿à¤·à¤¯ à¤šà¥à¤¨à¥‡à¤‚ (Please select a subject):", reply_markup=reply_markup)
    return NOTES_SELECTION

async def handle_note_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice in notes_links:
        await update.message.reply_text(f"ðŸ“„ Notes Link: {notes_links[choice]}")
    else:
        await update.message.reply_text("âŒ Invalid selection. Please use /notes again.")
    return ConversationHandler.END

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in known_users:
        await update.message.reply_text("ðŸ§  Test: Coming soon! Follow channel for updates.")
    else:
        await update.message.reply_text("ðŸ” Only for premium users. Use /buy to subscribe.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("subjects", subjects))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("approve", approve))

    notes_handler = ConversationHandler(
        entry_points=[CommandHandler("notes", notes)],
        states={NOTES_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_note_selection)]},
        fallbacks=[],
    )
    app.add_handler(notes_handler)
    app.run_polling()
