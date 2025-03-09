import pytz, requests
from datetime import datetime, timedelta
from fastapi import APIRouter
from dotenv import load_dotenv
# import logging
# logging.basicConfig(level=logging.DEBUG)

from services import get_meta_token, get_all_profile_ads_accounts
from models.report_models import ReportResponse

timezone = pytz.timezone("America/Sao_Paulo")
local_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
today = datetime.today().strftime('%Y-%m-%d')

load_dotenv(override=True)
router = APIRouter()

@router.get("/meta/all/{day}")
def get_all_ads(day: str):
  try:
    access_token_first_account = get_meta_token("first")
    access_token_second_account = get_meta_token("second")

    if isinstance(access_token_first_account, ReportResponse) or isinstance(access_token_second_account, ReportResponse):
      return {"error": "Erro ao obter tokens", "details": access_token_first_account or access_token_second_account}

    ads_accounts_first_account = get_all_profile_ads_accounts("first")
    ads_accounts_second_account = get_all_profile_ads_accounts("second")
    period = today if day == "today" else yesterday
    # all_ads_accounts = ads_accounts_first_account + ads_accounts_second_account
    # return {"data": all_ads_accounts, "period": period, "tamanho": len(all_ads_accounts)}
    ads = []

    for ad_account in ads_accounts_first_account:
      params = {
        "access_token": access_token_first_account,
        "level": "ad",
        "time_range": f'{{"since":"{period}","until":"{period}"}}',
        "fields": "ad_id,ad_name,spend,ctr",
        "limit": 25
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
            return ReportResponse(report_title="Get All Ads - first.", generated_at=local_time, data={"Status": response.status_code, "Error": f"Erro ao consultar os anúncios da conta: {ad_account}."})
      else:
        return ReportResponse(report_title="Get All Ads - first.", generated_at=local_time, data={"Status": response.status_code, "Error": f"Erro ao consultar os anúncios da conta: {ad_account}."})
    
    for ad_account in ads_accounts_second_account:
      params = {
        "access_token": access_token_second_account,
        "level": "ad",
        "time_range": f'{{"since":"{period}","until":"{period}"}}',
        "fields": "ad_id,ad_name,spend,ctr",
        "limit": 25
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
            return ReportResponse(report_title="Get All Ads - second.", generated_at=local_time, data={"Status": response.status_code, "Error": f"Erro ao consultar os anúncios da conta: {ad_account}."})
      else:
        return ReportResponse(report_title="Get All Ads - second.", generated_at=local_time, data={"Status": response.status_code, "Error": f"Erro ao consultar os anúncios da conta: {ad_account}."})
    
    return {"data": ads, "length": len(ads)}
  except Exception as e:
    return ReportResponse(report_title="Get All Ads", generated_at=local_time, data={"Error": str(e)})