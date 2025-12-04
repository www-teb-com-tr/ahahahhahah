from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8014881173:AAH9x5bX5uEx7CsyS6Sx7Zxx4zveMvYYxNk"

# Hızlıresim direkt resim linki (.jpg / .png olsun)
IMAGE_URL = "https://hizliresim.com/pxgmvio"

# Yönlendireceğin site
SITE_LINK = "https://free3commas.com"  # ref linkin neyse onu koy


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Tek satır buton
    keyboard = [
        [InlineKeyboardButton("🔗 Siteye Git", url=SITE_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Sadece görsel + buton (caption yok bile)
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=IMAGE_URL,
        reply_markup=reply_markup,
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_




