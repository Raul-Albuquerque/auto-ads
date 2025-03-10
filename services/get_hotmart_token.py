import os, pytz, requests
from dotenv import load_dotenv
from datetime import datetime

from cachetools import TTLCache

from models.report_models import ReportResponse

hotmart_token_cache = TTLCache(maxsize=2, ttl=158400) # 44 horas
load_dotenv(override=True)
timezone = pytz.timezone("America/Sao_Paulo")
local_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

ald_client_id = os.getenv("ALD_CLIENT_ID")
ald_client_secret = os.getenv("ALD_CLIENT_SECRET")
ald_basic = os.getenv("ALD_BASIC")
siberia_client_id = os.getenv("SIBERIA_CLIENT_ID")
siberia_client_secret = os.getenv("SIBERIA_CLIENT_SECRET")
siberia_basic = os.getenv("SIBERIA_BASIC")

def get_hotmart_token_auth(account: str):
  account = account.lower()
  if account == "ald":
    client_id = ald_client_id
    client_secret = ald_client_secret
    basic = f"Basic {ald_basic}"
  elif account == "siberia":
    client_id = siberia_client_id
    client_secret = siberia_client_secret
    basic = f"Basic {siberia_basic}"
  else:
    return ReportResponse(report_title="get_hotmart_token", generated_at=local_time, data=f"A conta: {account} não existe!")
  
  headers = {
    'Content-Type': 'application/json',
    'Authorization': basic
  }

  url = f"https://api-sec-vlc.hotmart.com/security/oauth/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
  response = requests.post(url=url, headers=headers)

  if response.status_code == 200:
    token = response.json().get("access_token")
    hotmart_token_cache[account] = token

  else:
    return ReportResponse(report_title="get_hotmart_token", generated_at=local_time, data=f"Falha ao renovar o token! - Status Code: {response.status_code}")
  

def get_hotmart_token(account:str):
  if account not in hotmart_token_cache or hotmart_token_cache[account] is None:
    get_hotmart_token_auth(account)
  return hotmart_token_cache[account]


