import os, pytz, requests
from dotenv import load_dotenv
from datetime import datetime

from cachetools import TTLCache

from models.report_models import ReportResponse

meta_token_cache = TTLCache(maxsize=2, ttl=4320000)
load_dotenv(override=True)

timezone = pytz.timezone("America/Sao_Paulo")
local_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

first_app_id = os.getenv("FIRST_APP_ID")
first_app_secret = os.getenv("FIRST_APP_SECRET") 
first_app_long_lived_token = os.getenv("FIRST_APP_LONG_LIVED_TOKEN")
second_app_id = os.getenv("SECOND_APP_ID") 
second_app_secret = os.getenv("SECOND_APP_SECRET") 
second_app_long_lived_token = os.getenv("SECOND_APP_LONG_LIVED_TOKEN")

def get_meta_token_auth(profile: str):
  profile = profile.lower()
  if profile == "first":
    client_id = first_app_id
    client_secret = first_app_secret
    fb_exchange_token = first_app_long_lived_token
  elif profile == "second":
    client_id = second_app_id
    client_secret = second_app_secret
    fb_exchange_token = second_app_long_lived_token
  else:
    return ReportResponse(report_title="get_meta_token", generated_at=local_time, data=f"O perfil: {profile} não existe!")
  
  url = "https://graph.facebook.com/v22.0/oauth/access_token"
  params = {
    "grant_type": "fb_exchange_token",
    "client_id": client_id,
    "client_secret": client_secret,
    "fb_exchange_token": fb_exchange_token
  }

  response = requests.get(url=url, params=params)
  if response.status_code == 200:
    new_token = response.json().get("access_token")
    meta_token_cache[profile] = new_token
  else:
    return ReportResponse(report_title="get_meta_token", generated_at=local_time, data=f"Falha ao renovar o token! - Status Code: {response.status_code}")

def get_meta_token(profile: str):
  if profile not in meta_token_cache or meta_token_cache[profile] is None:
    get_meta_token_auth(profile)
  return meta_token_cache[profile]