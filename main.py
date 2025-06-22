from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("📚 Welcome to StudyBot! Type /help to see commands.")

def help_command(update, context):
    update.message.reply_text("/start\n/help\n/buy\n/subjects\n/notes\n/test")

updater = Updater("YOUR_BOT_TOKEN", use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))

updater.start_polling()
updater.idle()
