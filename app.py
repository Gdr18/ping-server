import os
from flask import Flask, request, jsonify
from threading import Thread
import re

from utils import get_urls, keep_alive, clean_logs, write_log, URLS_FILE, LOGS_FILE

app = Flask(__name__)


def start_keep_alive():
	Thread(target=keep_alive, daemon=True).start()


start_keep_alive()


@app.route('/')
def welcome():
	return jsonify(msg="Bienvenidx a Ping Server!"), 200


@app.route("/logs", methods=["GET", "DELETE"])
def handling_logs():
	try:
		if request.method == "GET":
			logs = []
			if os.path.exists(LOGS_FILE):
				with open(LOGS_FILE) as file:
					logs = [line.strip() for line in file if line.strip()]
			return jsonify(logs), 200
		elif request.method == "DELETE":
			clean_logs()
			return jsonify(msg="Historial de registros eliminado correctamente."), 200
	except Exception as e:
		write_log(e, "handling_logs()")
		return jsonify(err=f"Error en 'handling_logs()' [{request.method}]: {str(e)}"), 500


@app.route("/urls", methods=['GET'])
def getting_urls():
	try:
		urls = get_urls()
		return jsonify(urls), 200
	except Exception as e:
		write_log(e, "getting_urls()")
		return jsonify(err=f"Error en 'getting_urls()' [{request.method}]: {str(e)}"), 500


@app.route("/urls", methods=['POST', 'DELETE'])
def handling_url():
	url = request.get_json().get("url")
	regex_url = r'^https?:\/\/(?:localhost|(?:\d{1,3}\.){3}\d{1,3}|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?::\d+)?(?:\/.*)?$'
	try:
		urls = get_urls()

		if request.method == 'POST':
			if not url or not re.match(regex_url, url):
				exc = Exception("La URL proporcionada no es válida o no se proporcionó.")
				exc.status_code = 400
				raise exc
			if url in urls:
				exc = Exception(f"La URL '{url}' ya existe.")
				exc.status_code = 409
				raise exc
			with open(URLS_FILE, 'a') as file:
				file.write(f"{url}\n")
			write_log(f"URL '{url}' añadida.", "handling_url()")
			return jsonify(msg=f"URL '{url}' añadida de forma satisfactoria."), 201

		elif request.method == 'DELETE':
			if not url or not re.match(regex_url, url):
				exc = Exception("La URL proporcionada no es válida o no se proporcionó.")
				exc.status_code = 400
				raise exc
			if url not in urls:
				exc = Exception(f"La URL '{url}' no existe.")
				exc.status_code = 404
				raise exc
			urls.remove(url)
			with open(URLS_FILE, 'w') as file:
				for existing_url in urls:
					file.write(f"{existing_url}\n")
			write_log(f"URL '{url}' eliminada.", "handling_url()")
			return jsonify(msg=f"URL '{url}' eliminada de forma satisfactoria."), 200
	except Exception as e:
		write_log(e, f"handling_url() [{request.method}]")
		return jsonify(err=f"Error en 'handling_url()' [{request.method}]: {str(e)}"), getattr(e, "status_code", 500)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
