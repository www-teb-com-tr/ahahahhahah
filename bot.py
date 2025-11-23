#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ultra addictive 3Commas referral Telegram bot
Python + python-telegram-bot v20+
"""

import logging
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# ================== AYARLAR ==================

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"   # <-- buraya kendi tokenını yaz

BANNER_URL = "https://i.imgur.com/3xY7k9P.jpg"   # banner veya GIF

REF_LINK = "https://3commas.io/?ref=PUT_YOUR_REF_CODE_HERE"   # referral linkin

HOW_IT_WORKS_VIDEO_URL = "https://www.youtube.com/watch?v=PUT_VIDEO_ID_HERE"  # video link

WINNERS_UPDATE_LIMIT = 20   # kazanan listesi kaç kez yenilenecek (her 15 sn)


# ================== LOGGING ==================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ================== YARDIMCI FONKSİYONLAR ==================

def build_main_keyboard() -> InlineKeyboardMarkup:
    """
    Ana ekranda çıkacak inline butonları oluşturur.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="🎁 GET FREE 1-YEAR PRO ACCOUNT",
                callback_data="get_ref_link",
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 LIVE Winners",
                callback_data="show_winners",
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ How Does It Work?",
                callback_data="how_it_works",
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def generate_fake_username() -> str:
    """
    Fake username üretir.
    """
    bases = [
        "CryptoKing", "BoraTrader", "AhmetBTC", "AltcoinQueen", "ScalperFox",
        "LamboHunter", "PumpWizard", "SwingLord", "SniperTR", "WhaleWatcher",
        "BotPilot", "GridMaster", "SwingAngel", "DeltaLord", "BullSniper",
    ]
    base = random.choice(bases)
    suffix = random.randint(7, 99)
    return f"@{base}{suffix}"


def generate_fake_profit() -> str:
    """
    Fake kazanç miktarı üretir.
    """
    whole = random.randint(1500, 15000)
    decimals = random.randint(100, 999)
    return f"{whole:,}".replace(",", ".") + f",{decimals}"


def build_winners_text() -> str:
    """
    Fake kazanan listesi paragrafını üretir.
    """
    lines = ["📈 *Live Winners Feed*\n"]
    count = random.randint(4, 7)
    for _ in range(count):
        u = generate_fake_username()
        p = generate_fake_profit()
        lines.append(f"✅ {u} → +${p}")
    return "\n".join(lines)


async def send_main_banner(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    """
    Ana banner'ı + metni + butonları yollar.
    """
    caption = (
        "🚀 *The Secret Bot That Changes Trading Forever*\n\n"
        "🔥 Only **100 slots left** to claim a *FREE 1-Year 3Commas Pro account!*\n"
        "⏳ Claim yours before it closes!\n\n"
        "💰 Users reported earning over **$47,000 in 2 weeks** using this setup."
    )

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=BANNER_URL,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=build_main_keyboard(),
    )


# ================== HANDLERLAR ==================

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start komutu gelince ana ekranı gösterir.
    """
    await send_main_banner(update.effective_chat.id, context)


async def any_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Kullanıcı herhangi bir mesaj yazarsa yine ana ekranı gösterir.
    """
    await send_main_banner(update.effective_chat.id, context)


async def get_ref_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Kullanıcı referral butonuna basınca:
    - DM'ye özel mesaj yollar
    - Buton tekrar verir
    """
    query = update.callback_query
    await query.answer()

    user = query.from_user

    msg = (
        "🎉 Congratulations!\n\n"
        "Your exclusive **3Commas Pro Referral Link** has been generated.\n"
        "Click the button below to activate your **FREE 1-Year Pro plan**:"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 OPEN MY FREE PRO ACCOUNT", url=REF_LINK)]
    ])

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=msg,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

        await query.message.reply_text(
            "✅ I've sent your private activation link via DM — check your Telegram inbox!"
        )
    except:
        await query.message.reply_text(
            "⚠️ I couldn't DM you. Please open a private chat with me first and press the button again."
        )


async def show_winners_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Kazanan listesi ekranı.
    Sonrasında JobQueue ile her 15 saniye güncellenir.
    """
    query = update.callback_query
    await query.answer()

    text = build_winners_text()
    msg = await query.message.reply_text(
        text=text,
        parse_mode="Markdown"
    )

    context.job_queue.run_repeating(
        update_winners_job,
        interval=15,
        first=15,
        data={
            "chat_id": msg.chat_id,
            "message_id": msg.message_id,
            "counter": 0,
        }
    )


async def update_winners_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Her 15 saniyede fake kazanan listesini günceller.
    """
    job = context.job
    data = job.data

    if data["counter"] >= WINNERS_UPDATE_LIMIT:
        job.schedule_removal()
        return

    data["counter"] += 1

    try:
        await context.bot.edit_message_text(
            chat_id=data["chat_id"],
            message_id=data["message_id"],
            text=build_winners_text(),
            parse_mode="Markdown"
        )
    except:
        job.schedule_removal()


async def how_it_works_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Nasıl çalışıyor metni.
    """
    query = update.callback_query
    await query.answer()

    msg = (
        "ℹ️ *How Does It Work?*\n\n"
        "3Commas is an automated trading platform that executes trades for you 24/7.\n\n"
        "✅ Smart strategies\n"
        "✅ Greed-free entries\n"
        "✅ Stop-Loss + Take-Profit\n"
        "✅ Funds safety\n"
        "✅ No emotions\n\n"
        f"🎥 Watch the explanation video:\n{HOW_IT_WORKS_VIDEO_URL}\n\n"
        "Click the button below to claim your **FREE 1-Year Pro account**."
    )

    await query.message.reply_text(
        text=msg,
        parse_mode="Markdown",
        reply_markup=build_main_keyboard(),
    )


# ================== MAIN ==================

def main():
    """
    Botu başlatır (Polling)
    """
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(get_ref_link_handler, pattern="^get_ref_link$"))
    app.add_handler(CallbackQueryHandler(show_winners_handler, pattern="^show_winners$"))
    app.add_handler(CallbackQueryHandler(how_it_works_handler, pattern="^how_it_works$"))
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), any_message_handler))

    logger.info("Bot started.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
