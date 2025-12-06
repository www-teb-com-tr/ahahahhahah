from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ⚠️ IMPORTANT:
# Get a NEW token from BotFather (/newbot or /revoke) and paste it here.
BOT_TOKEN = "8342196613:AAE7rhjlBm5DXWPrK90H1yGW6t6YNGLloSk"

# Destination link for the campaign
AIRDROP_LINK = "https://astercampaign.space/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Clean, ad-safe explanation text
    text = (
        "Aster campaign assistant bot.\n"
        "\n"
        "This bot helps you follow the steps required to join the Aster campaign.\n"
        "Read the instructions on the next page and continue from there."
    )

    # Single button leading to your link
    keyboard = [
        [InlineKeyboardButton("🔗 Open Aster Campaign", url=AIRDROP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Only /start command is handled
    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
