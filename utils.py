import time
from datetime import datetime
import os.path
import requests

URLS_FILE = '/data/urls.txt'
LOGS_FILE = '/data/logs.txt'
INTERVAL = 480
last_cleaning = None


def get_urls() -> list:
	if not os.path.exists(URLS_FILE):
		return []
	with open(URLS_FILE) as file:
		urls_list = [line.strip() for line in file]
	return urls_list


def write_log(message: requests.Response | Exception | str, resource: str):
	now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	if isinstance(message, requests.Response):
		status_code = message.status_code
		message = f"[{now}] - {resource} - status: {status_code}\n"
	elif isinstance(message, Exception):
		message = f"[{now}] - {resource} - error: {str(message)}\n"
	else:
		message = f"[{now}] - {resource} - info: {message}\n"
	with open(LOGS_FILE, 'a') as file:
		file.write(message)


def clean_logs():
	global last_cleaning
	now = datetime.now()
	with open(LOGS_FILE, "w") as file:
		file.write(f'[{now.strftime("%d-%m-%Y %H:%M:%S")}] - Historial de registros limpiado.\n')
	last_cleaning = now.date()


def check_cleaning():
	today = datetime.now().date()
	if last_cleaning != today:
		clean_logs()


def keep_alive():
	while True:
		try:
			check_cleaning()
			urls = get_urls()
			if len(urls) > 0:
				for url in urls:
					response = requests.get(url)
					write_log(response, url)
			else:
				write_log(Exception("Archivo 'urls.txt' vacío."), "loop_pings()")
		except Exception as e:
			write_log(e, "keep_alive()")

		time.sleep(INTERVAL)
