#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (KANKA: BOT TAM BURADA)
# This is the ultra addictive 3Commas referral Telegram bot
# English bot + Turkish explanations

import logging, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
BANNER_URL = "https://i.imgur.com/3xY7k9P.jpg"
REF_LINK = "https://3commas.io/?ref=PUT_YOUR_REF_CODE_HERE"
HOW_IT_WORKS_VIDEO_URL = "https://www.youtube.com/watch?v=PUT_VIDEO_ID_HERE"
WINNERS_UPDATE_LIMIT = 20

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
logger = logging.getLogger(__name__)

def build_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 GET FREE 1-YEAR PRO ACCOUNT",callback_data="get_ref_link")],
        [InlineKeyboardButton("📈 LIVE Winners",callback_data="show_winners")],
        [InlineKeyboardButton("ℹ️ How Does It Work?",callback_data="how_it_works")]
    ])

def generate_fake_username():
    bases=["CryptoKing","BoraTrader","AhmetBTC","AltcoinQueen","ScalperFox","LamboHunter","PumpWizard"]
    return f"@{random.choice(bases)}{random.randint(7,99)}"

def generate_fake_profit():
    whole=random.randint(1500,15000)
    dec=random.randint(100,999)
    return f"{whole:,}".replace(",",".")+f",{dec}"

def build_winners_text():
    lines=["📈 *Live Winners Feed*",""]
    for _ in range(random.randint(4,7)):
        lines.append(f"✅ {generate_fake_username()} → +${generate_fake_profit()}")
    return "\n".join(lines)

async def send_main_banner(chat_id, ctx):
    caption=("🚀 *The Secret Bot That Changes Trading Forever*\n\n"
             "🔥 Only **100 left** to claim FREE 1-Year 3Commas Pro!")
    await ctx.bot.send_photo(chat_id=chat_id,photo=BANNER_URL,caption=caption,parse_mode="Markdown",reply_markup=build_main_keyboard())

async def start_handler(u,ctx):await send_main_banner(u.effective_chat.id,ctx)
async def any_message_handler(u,ctx):await send_main_banner(u.effective_chat.id,ctx)

async def get_ref_link_handler(u,ctx):
    q=u.callback_query;await q.answer()
    kb=InlineKeyboardMarkup([[InlineKeyboardButton("🎁 OPEN MY FREE PRO ACCOUNT",url=REF_LINK)]])
    try:
        await ctx.bot.send_message(chat_id=u.effective_user.id,text="Your link:",reply_markup=kb)
        await q.message.reply_text("DM sent!")
    except:await q.message.reply_text("DM closed. Open DM first.")

async def show_winners_handler(u,ctx):
    q=u.callback_query;await q.answer()
    m=await q.message.reply_text(build_winners_text(),parse_mode="Markdown")
    ctx.job_queue.run_repeating(update_winners_job,15,15,data={"chat":m.chat_id,"msg":m.message_id,"c":0})

async def update_winners_job(ctx:ContextTypes.DEFAULT_TYPE):
    job=ctx.job;d=job.data
    if d["c"]>=WINNERS_UPDATE_LIMIT:job.schedule_removal();return
    d["c"]+=1
    try:
        await ctx.bot.edit_message_text(chat_id=d["chat"],message_id=d["msg"],text=build_winners_text(),parse_mode="Markdown")
    except:job.schedule_removal()

async def how_it_works_handler(u,ctx):
    q=u.callback_query;await q.answer()
    await q.message.reply_text("3Commas explanation...",parse_mode="Markdown",reply_markup=build_main_keyboard())

def main():
    app=ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start_handler))
    app.add_handler(CallbackQueryHandler(get_ref_link_handler,pattern="^get_ref_link$"))
    app.add_handler(CallbackQueryHandler(show_winners_handler,pattern="^show_winners$"))
    app.add_handler(CallbackQueryHandler(how_it_works_handler,pattern="^how_it_works$"))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND,any_message_handler))
    app.run_polling()

if __name__=="__main__":main()
