from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os

OWNER_ID = 6295626651  # आपका Telegram numeric ID

KNOWN_USERS = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == OWNER_ID or user_id in KNOWN_USERS:
        await update.message.reply_text("🎉 Welcome! Use /buy, /subjects, or /notes to get started.")
    else:
        keyboard = [
            [InlineKeyboardButton("Request Access", callback_data="request_access")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("❌ Access Denied. Request permission below:", reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if query.data == "request_access":
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"👤 User @{query.from_user.username or user_id} requested access. Approve? Use /approve {user_id}"
        )
        await query.edit_message_text("✅ Request sent! Wait for approval.")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ You're not allowed to approve users.")
        return
    try:
        user_id = int(context.args[0])
        KNOWN_USERS.add(user_id)
        await update.message.reply_text(f"✅ User {user_id} approved.")
        await context.bot.send_message(chat_id=user_id, text="🎉 You have been granted access!")
    except:
        await update.message.reply_text("⚠️ Use: /approve <user_id>")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 Buy menu: \n1. ₹49 Notes\n2. ₹99 Full Access\nPay to: `9528165371@amazonpay`")

async def subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Subjects:\n- Hindi\n- GK\n- Reasoning\n- Constitution\nUse /notes to get material.")

async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Notes: Send subject name to get PDF or content.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("subjects", subjects))
    app.add_handler(CommandHandler("notes", notes))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    app.run_polling()

