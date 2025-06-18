from datetime import datetime
from decimal import Decimal
import os
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from requests import Session

def login(login_url:str, username:str, password:str):
    session:Session = Session()
    response = session.post(login_url, data={"username":username, "password":password})
    if not response.ok: print("Plugin Uchi Parfume Jember : Login failed"); raise Exception
    return session

def scrape_omzet(session:Session, omzet_url:str):
    # start_date = datetime.now().date()
    # end_date = datetime.now().date()
    response = session.get(omzet_url)
    if not response.ok: print("Plugin Uchi Parfume Jember : Get failed"); raise Exception

    soup = BeautifulSoup(response.text, "html.parser")
    portlets = soup.select(".m-portlet") # normally this contains 3 portlets
    portlet_all_cabang = portlets[1]
    first_match = portlet_all_cabang.find("span", string=re.compile(r"Rp"))

    omzet = None
    if first_match:
        omzet = first_match.get_text(strip=True)
        omzet = omzet.replace("Rp.", "").replace(",", "").strip()
    return omzet

def get_omzet():
    env_path = "./plugins/uchi_parfume/.env"
    if not os.path.exists(env_path):
        print("Plugin Uchi Parfume Jember : env not found")
        raise Exception
    load_dotenv()
    BASE_URL = os.environ.get("BASE_URL_UCHI_PARFUME_JEMBER", None)
    LOGIN_URL = f"{BASE_URL}auth/"
    OMZET_URL = f"{BASE_URL}dashboard_owner/"
    USERNAME = os.environ.get("USERNAME_UCHI_PARFUME_JEMBER", "")
    PASSWORD = os.environ.get("PASSWORD_UCHI_PARFUME_JEMBER", "")

    session:Session = login(LOGIN_URL, USERNAME, PASSWORD)
    omzet:str = scrape_omzet(session, OMZET_URL)
    
    omzet = Decimal(omzet)
    return omzet

if __name__ == "__main__":
    print(get_omzet())