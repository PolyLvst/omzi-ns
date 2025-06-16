from datetime import datetime, timedelta, timezone
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app import OmziNSEntry
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get("TOKEN_TELEGRAM_BOT", "")
WIB = timezone(timedelta(hours=7))

class OmziNS:
    def __init__(self):
        self.configs = OmziNSEntry.load_config()
        self.chats = self.configs.get("chats")
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_schedules()

    def setup_schedules(self):
        for chat in self.chats:
            name = chat.get("name")
            schedule = chat.get("schedule")
            chat_id = chat.get("chat_id")
            services = chat.get("services")

            job_parameters = {"chat_id":chat_id, "services_uuid":services}
            job_time = datetime.strptime(schedule, "%H:%M:%S").time().replace(tzinfo=WIB)
            # Run daily attach to job queue
            self.app.job_queue.run_daily(self.send_report, time=job_time, data=job_parameters)
            # self.app.job_queue.run_repeating(self.send_report, interval=15, first=0, data=job_parameters)
            print(f"-- Job Queue : {name} Assigned")

    async def send_report(self, context: ContextTypes.DEFAULT_TYPE):
        parameters = context.job.data
        services_uuid = parameters["services_uuid"]
        chat_id = parameters["chat_id"]
        report = OmziNSEntry.collect_report(services_uuid=services_uuid)
        await context.bot.send_message(chat_id=chat_id, text=report, parse_mode="Markdown")

    async def ping_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ I'm up and running!")
    
    def start(self):
        # app.add_handler(CommandHandler("report", send_report))
        self.app.add_handler(CommandHandler("ping", self.ping_command))
        self.app.run_polling()

if __name__ == "__main__":
    print("-- Bot Started --")
    omzins = OmziNS()
    omzins.start()