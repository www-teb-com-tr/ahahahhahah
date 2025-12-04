from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8014881173:AAH9x5bX5uEx7CsyS6Sx7Zxx4zveMvYYxNk"  # your BotFather token

# Direct image URL (must end with .jpg / .png)
IMAGE_URL = "https://hizliresim.com/pxgmvio"

# Website link
SITE_LINK = "https://free3commas.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    keyboard = [
        [InlineKeyboardButton("🔗 Visit Website", url=SITE_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=IMAGE_URL,
        reply_markup=reply_markup,
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()

                                   

