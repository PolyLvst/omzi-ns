from datetime import datetime
from decimal import Decimal
import pytz
import yaml
import importlib
import os
from babel.numbers import format_currency

class OmziNSEntry:
    def format_rupiah(value):
        return format_currency(value, 'IDR', locale='id_ID').replace(",00","")

    def load_config(path="config.yml"):
        if not os.path.exists(path=path):
            print("-- NO Config yml found --")
            exit()
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def collect_report(services_uuid:list[str]):
        config = OmziNSEntry.load_config()
        services:list = config.get("services", [])
        header = config.get("header")
        footer = config.get("footer")
        
        messages = []
        for service in services:
            if service["uuid"] not in services_uuid: continue
            try:
                module = importlib.import_module(service["module"])
                omzet = module.get_omzet()
                messages.append(f"{service['name']}:\n└── {OmziNSEntry.format_rupiah(omzet)}")
            except Exception as e:
                print(f"⚠️ {service['name']} failed: {e}")
                messages.append(f"⚠️ {service['name']} failed: CHECK SERVER LOG")
        
        if len(messages) == 0:
            messages.append("No configured service --")
        joined_messages = '\n'.join(messages)
        now = datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime("%d/%m/%Y")
        report = f"{header}\n\n{joined_messages}\n\n{footer}\n{now}"
        return report

if __name__ == "__main__":
    configs = OmziNSEntry.load_config()
    chats = configs.get("chats")
    for chat in chats:
        services = chat.get("services")
        print(OmziNSEntry.collect_report(services_uuid=services))