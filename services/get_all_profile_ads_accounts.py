import pytz, requests
from datetime import datetime

from services import get_meta_token
from models.report_models import ReportResponse

timezone = pytz.timezone("America/Sao_Paulo")
local_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

def get_all_profile_ads_accounts(profile: str):
  profile = profile.lower()
  access_token = get_meta_token(profile)
  url = f"https://graph.facebook.com/v22.0/me/adaccounts?access_token={access_token}"
  response = requests.get(url=url)
  ads_accounts = []
  
  if response.status_code == 200:
    accounts = response.json().get("data")
    for account in accounts:
      ads_accounts.append(account["id"])
    return ads_accounts

  else:
    return ReportResponse(report_title="Get All Profile Ads Accounts", generated_at=local_time, data={"Status": response.status_code, "Error": f"Erro ao consultar as contas de anúncio do perfil: {profile}."})