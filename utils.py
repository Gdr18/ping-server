import time
from datetime import datetime
import requests


def get_urls() -> list[str] | None:
	urls_file = 'urls.txt'
	try:
		with open(urls_file) as file:
			urls_list = [line.strip() for line in file]
		return urls_list
	except Exception as e:
		write_log(e, "get_urls()")


INTERVAL = 840
CLEANING_DAY = 1
last_cleaning = None


def write_log(response: requests.Response | Exception , resource: str):
	logs_file = 'logs.txt'
	now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	if isinstance(response, requests.Response):
		status_code = response.status_code
		message = f"[{now}] - {resource} - status: {status_code}\n"
	else:
		message = f"[{now}] - {resource} - error: {str(response)}\n"
	try:
		with open(logs_file, 'a') as file:
			file.write(message)
	except Exception as e:
		message = f"[{now}] - write_log() - error: {str(e)}\n"
		with open(logs_file, 'a') as file:
			file.write(message)


def clean_logs():
	global last_cleaning
	now = datetime.now()
	logs_file = 'logs.txt'
	try:
		with open(logs_file, "w") as file:
			file.write(f'[{now.strftime("%d-%m-%Y %H:%M:%S")}] - Historial de registros limpiado.\n')
		last_cleaning = now.date()
	except Exception as e:
		write_log(e, "clean_logs()")


def checking_cleaning_day():
	today = datetime.now().date()
	if today.day == CLEANING_DAY and (last_cleaning is None or last_cleaning.month != today.month):
		clean_logs()


def keep_alive():
	while True:
		checking_cleaning_day()
		urls = get_urls()
		if isinstance(urls, list):
			for url in urls:
				try:
					response = requests.get(url)
					write_log(response, url)
				except Exception as e:
					write_log(e, url)
		else:
			write_log(Exception("Archivo 'urls.txt' vacío."), "loop_pings()")
		time.sleep(INTERVAL)
