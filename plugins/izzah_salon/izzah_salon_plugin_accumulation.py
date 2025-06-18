from datetime import datetime, timedelta
from decimal import Decimal
import pytz
import requests
from requests import Response
from dotenv import load_dotenv
import os

def get_omzet():
    env_path = "./plugins/izzah_salon/.env"
    if not os.path.exists(env_path):
        print("Plugin Izzah Salon : env not found")
        raise Exception
    load_dotenv()
    BASE_URL = os.environ.get("BASE_URL_IZZAH", None)
    LOGIN_URL = f"{BASE_URL}login/"
    OMZET_URL = f"{BASE_URL}transactions/omzet"
    USERNAME = os.environ.get("USERNAME_IZZAH", "")
    PASSWORD = os.environ.get("PASSWORD_IZZAH", "")
    result:Response = requests.post(LOGIN_URL, data={"username":USERNAME, "password":PASSWORD})
    if not result.ok: raise Exception
    token = result.json().get("access_token", "")
    now = datetime.now(pytz.UTC)
    this_month_first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_day_period = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)  # exclusive end of day
    result:Response = requests.get(OMZET_URL, params={"start":this_month_first_day, "end":current_day_period}, headers={"Authorization": f"Bearer {token}"})
    # result:Response = requests.get(OMZET_URL, headers={"Authorization": f"Bearer {token}"})
    if not result.ok: raise Exception
    omzet = result.json().get("omzet", "")
    omzet = Decimal(omzet)
    return omzet

if __name__ == "__main__":
    print(get_omzet())