from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7650633591:AAFJFvsTfXSEKdNYRjmjv-24P0HO_9AyfKw"
OWNER_ID = 6295626651

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Access Denied. Paid Users Only.")
        return
    await update.message.reply_text("✅ Welcome to the Study Bot!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
