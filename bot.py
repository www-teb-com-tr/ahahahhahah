from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8014881173:AAH9x5bX5uEx7CsyS6Sx7Zxx4zveMvYYxNk"  # sadece burada kullanılıyor kanka

# Hızlıresim görüntü linkin (direkt .jpg/.png olsun)
IMAGE_URL = "https://hizliresim.com/pxgmvio"

# Altında görünecek link
SITE_LINK = "https://3commas.io/?c=ELITE1YEARFREE"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Görseli URL üzerinden gönder → Telegram kendi indirir
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=IMAGE_URL,
        caption=SITE_LINK
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()
