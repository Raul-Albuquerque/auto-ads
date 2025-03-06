import pytz, requests
from dotenv import load_dotenv
from fastapi import APIRouter
from datetime import datetime

from core.helpers import get_yesterday_timestamp, get_today_timestamp
from services import get_token
from models.report_models import ReportResponse 

load_dotenv(override=True)
timezone = pytz.timezone("America/Sao_Paulo")
local_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

router = APIRouter()
HOTMART_URL = "https://developers.hotmart.com/payments/api/v1/sales/history"

@router.get("/hotmart/{account}/all/{day}")
def get_all_purchases(account: str, day: str):
  token = get_token(account)
  HEADERS = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
  }

  if day == "today":
    start_date = get_today_timestamp("start")
    end_date = get_today_timestamp("end")
  elif day == "yesterday":
    start_date = get_yesterday_timestamp("start")
    end_date = get_yesterday_timestamp("end")
  
  PARAMS = {
    "start_date": start_date,
    "end_date": end_date,
    "transaction_status": "APPROVED",
    "max_results": 350,
  }

  response = requests.get(HOTMART_URL, params=PARAMS, headers=HEADERS)

  if response.status_code == 200:
    sales = response.json().get("items", [])
    return ReportResponse(report_title="Get All Purchases.", generated_at=local_time, count=len(sales), data=sales)
  else:
    return ReportResponse(report_title="Get All Purchases.", generated_at=local_time, data={"Status": response.status_code, "Error": f"Erro ao consultar as vendas da conta {account}."})