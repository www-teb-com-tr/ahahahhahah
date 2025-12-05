from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8342196613:AAHiSjTRka2V1KFw-f6-j8U8etZs8Zn6mhQ"

# Linki sen buraya koyacaksın
AIRDROP_LINK = "https://astercampaign.space/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    text = (
        "Aster Airdrop is now live!\n"
        "Join the campaign and secure your spot.\n"
        "Simple steps, fast rewards."
    )

    keyboard = [
        [InlineKeyboardButton("🔗 Join Airdrop", url=AIRDROP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()
