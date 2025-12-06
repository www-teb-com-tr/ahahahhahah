from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Buraya YENİ bot tokenini koy (BotFather'dan aldığın)
BOT_TOKEN = "7791813822:AAG4ZzvZ4vziwIk2O2fbB3XS0oPPIWafZ5w"

# Kullanıcıyı yönlendireceğin link (Aster veya başka ne istiyorsan)
TARGET_LINK = "https://astercampaign.space/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Telegram Ads için nötr, temiz açıklama
    text = (
        "Welcome to the assistant bot.\n\n"
        "Here you can access structured steps and useful links in a simple layout.\n"
        "Use the button below to continue."
    )

    keyboard = [
        [InlineKeyboardButton("Continue", url=TARGET_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Sadece /start komutu
    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
