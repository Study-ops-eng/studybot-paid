import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN") or "7650633591:AAFJFvsTfXSEKdNYRjmjv-24P0HO_9AyfKw"
OWNER_ID = 6295626651  # आपका Telegram ID

APPROVED_USERS_FILE = "approved_users.json"

# Approved users को load/save करने के functions
def load_approved_users():
    if not os.path.exists(APPROVED_USERS_FILE):
        return []
    with open(APPROVED_USERS_FILE, "r") as f:
        return json.load(f)

def save_approved_users(users):
    with open(APPROVED_USERS_FILE, "w") as f:
        json.dump(users, f)

approved_users = load_approved_users()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID and user_id not in approved_users:
        await update.message.reply_text(
            "🔒 यह बॉट सबके लिए नहीं है।\nअनुमति के लिए Owner से संपर्क करें।"
        )
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"🔔 User @{update.effective_user.username or 'NoUsername'} (ID: {user_id}) permission मांग रहा है।\n\nउसे free access देने के लिए /approve {user_id} भेजें।"
        )
        return

    await update.message.reply_text(
        "📚 Welcome to StudyBot!\n\nUse /help to see available commands."
    )

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if context.args:
        try:
            user_id = int(context.args[0])
            if user_id not in approved_users:
                approved_users.append(user_id)
                save_approved_users(approved_users)
                await update.message.reply_text(f"✅ User {user_id} को access दे दिया गया।")
                await context.bot.send_message(chat_id=user_id, text="🎉 आपको बॉट की access मिल गई है!")
            else:
                await update.message.reply_text("ℹ️ User पहले से approved है।")
        except:
            await update.message.reply_text("❌ Invalid user ID.")
    else:
        await update.message.reply_text("❗ Usage: /approve <user_id>")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Premium access के लिए ₹99 UPI करें: 9528165371@amazonpay")

async def subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 उपलब्ध विषय:\n- हिंदी\n- गणित\n- विज्ञान\n- इतिहास")

async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📒 अभी नोट्स अपडेट किए जा रहे हैं। जल्द आ रहे हैं!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤖 Available Commands:
/start - बॉट शुरू करें
/buy - प्रीमियम खरीदें
/subjects - विषय सूची
/notes - नोट्स देखें
/approve <user_id> - (Owner only)
""")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("subjects", subjects))
    app.add_handler(CommandHandler("notes", notes))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("approve", approve))
    app.run_polling()

if __name__ == "__main__":
    main()

 
