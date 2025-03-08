import pytz, requests
from datetime import datetime, timedelta
from fastapi import APIRouter
from dotenv import load_dotenv

from services import get_meta_token, get_all_profile_ads_accounts
from models.report_models import ReportResponse

timezone = pytz.timezone("America/Sao_Paulo")
local_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
today = datetime.today().strftime('%Y-%m-%d')

load_dotenv(override=True)
router = APIRouter()

@router.get("/meta/{profile}/all/{day}")
def get_all_profile_ads(profile: str, day: str):
  access_token = get_meta_token(profile)
  ads_accounts = get_all_profile_ads_accounts(profile)
  period = today if day == "today" else yesterday
  ads = []

  for ad_account in ads_accounts:
    params = {
      "access_token": access_token,
      "level": "ad",
      "time_range": f'{{"since":"{period}","until":"{period}"}}',
      "fields": "ad_id,ad_name,spend,ctr",
      "limit": 50
    }

    url = f"https://graph.facebook.com/v22.0/{ad_account}/insights"
    response = requests.get(url=url, params=params)

    if response.status_code == 200:
      ads_response = response.json()
      ads_data = ads_response.get("data", [])
      ads.extend(ads_data)

      while "paging" in ads_response and "next" in ads_response["paging"]:
        next_url = ads_response["paging"]["next"]
        response = requests.get(next_url)

        if response.status_code == 200:
          ads_response = response.json()
          ads_data = ads_response.get("data", [])
          ads.extend(ads_data)
        else:
          return ReportResponse(report_title="Get All Profile Ads.", generated_at=local_time, data={"Status": response.status_code, "Error": f"Erro ao consultar os anúncios da conta: {ad_account}."})
    else:
      return ReportResponse(report_title="Get All Profile Ads.", generated_at=local_time, data={"Status": response.status_code, "Error": f"Erro ao consultar os anúncios da conta: {ad_account}."})

  print(f"Total de anúncios coletados: {len(ads)}")
  return {"data": ads}
