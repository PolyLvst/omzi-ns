from datetime import time, timedelta, timezone
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app import collect_report
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get("TOKEN_TELEGRAM_BOT", "")
CHAT_ID = os.environ.get("CHAT_ID_TELEGRAM", "")
HOUR_SCHEDULE = int(os.environ.get("HOUR_SCHEDULE", 19))
WIB = timezone(timedelta(hours=7))

async def send_report(context: ContextTypes.DEFAULT_TYPE):
    report = collect_report()
    await context.bot.send_message(chat_id=CHAT_ID, text=report, parse_mode="Markdown")

if __name__ == "__main__":
    print("-- Bot Started --")
    app = Application.builder().token(BOT_TOKEN).build()
    # app.add_handler(CommandHandler("report", send_report))
    app.job_queue.run_daily(send_report, time=time(hour=HOUR_SCHEDULE, tzinfo=WIB))
    # app.job_queue.run_repeating(send_report, interval=5, first=0)
    app.run_polling()