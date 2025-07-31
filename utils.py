import time
from datetime import datetime
import requests
from typing import Union
from flask import Response


def get_urls() -> Union[list, None]:
	urls_file = 'urls.txt'
	try:
		with open(urls_file) as file:
			urls_list = [line.strip() for line in file]
		return urls_list
	except Exception as e:
		print(f"Error al leer '{urls_file}': {str(e)}")


INTERVAL = 840
CLEANING_DAY = 1
last_cleaning = None


def write_log(response: Response, url: str):
	logs_file = 'logs.txt'
	now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	status_code = getattr(response, 'status_code', 'N/A')
	try:
		with open(logs_file, 'a') as file:
			file.write(f"[{now}] - {url} - status: {status_code}\n")
	except Exception as e:
		print(f"Error al escribir en '{logs_file}': {str(e)}")


def clean_logs():
	global last_cleaning
	now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	logs_file = 'logs.txt'
	try:
		with open(logs_file, "w") as f:
			f.write(f"Registros limpiados: [{now}].\n")
		last_cleaning = now
	except Exception as e:
		print(f"Error al limpiar '{logs_file}': {e}")


def checking_cleaning_day():
	today = datetime.now().date()
	if today.day == CLEANING_DAY and (last_cleaning is None or last_cleaning.month != today.month):
		clean_logs()


def loop_pings():
	while True:
		checking_cleaning_day()
		urls = get_urls()
		for url in urls:
			try:
				response = requests.get(url)
				write_log(response, url)
			except Exception as e:
				write_log(e, url)
		time.sleep(INTERVAL)
