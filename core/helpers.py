import time
from datetime import datetime, timedelta

def get_yesterday_timestamp(period: str) -> int:
	yesterday = datetime.now() - timedelta(days=1) 

	if period == "start":
		yesterday = yesterday.replace(hour=0, minute=0, second=0)
	elif period == "end":
		yesterday = yesterday.replace(hour=23, minute=59, second=59)
	else:
		raise ValueError("O parâmetro 'period' deve ser 'start' ou 'end'.")

	timestamp = int(time.mktime(yesterday.timetuple()) * 1000)
	return timestamp

def get_today_timestamp(period: str) -> int:
	today = datetime.now()

	if period == "start":
		today = today.replace(hour=0, minute=0, second=0, microsecond=0)
	elif period == "end":
		today = today.replace(hour=23, minute=59, second=59, microsecond=999999)
	else:
		raise ValueError("O parâmetro 'period' deve ser 'start' ou 'end'.")

	timestamp = int(today.timestamp() * 1000)
	return timestamp