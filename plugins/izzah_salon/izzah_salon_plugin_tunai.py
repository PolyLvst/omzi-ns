from decimal import Decimal
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
    OMZET_URL = f"{BASE_URL}transactions/omzet-tunai"
    USERNAME = os.environ.get("USERNAME_IZZAH", "")
    PASSWORD = os.environ.get("PASSWORD_IZZAH", "")
    result:Response = requests.post(LOGIN_URL, data={"username":USERNAME, "password":PASSWORD})
    if not result.ok: raise Exception
    token = result.json().get("access_token", "")
    # result:Response = requests.get(OMZET_URL, params={"start":"2025-06-01T00:00:00Z", "end":"2025-06-14T00:00:00Z"}, headers={"Authorization": f"Bearer {token}"})
    result:Response = requests.get(OMZET_URL, headers={"Authorization": f"Bearer {token}"})
    if not result.ok: raise Exception
    omzet = result.json().get("omzet", "")
    omzet = Decimal(omzet)
    return omzet

if __name__ == "__main__":
    print(get_omzet())