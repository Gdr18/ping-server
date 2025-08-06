import os.path
from flask import Flask, request, jsonify
from threading import Thread
import re

from utils import get_urls, keep_alive, clean_logs, write_log

app = Flask(__name__)


@app.route('/')
def welcome():
	return jsonify(msg="Bienvenidx a Ping Server!"), 200


@app.route("/logs", methods=["GET", "DELETE"])
def handling_logs():
	file_logs = "logs.txt"
	try:
		if request.method == "GET":
			logs = []
			if os.path.exists(file_logs):
				with open(file_logs) as file:
					logs = [line.strip() for line in file if line.strip()]
			return jsonify(logs), 200
		elif request.method == "DELETE":
			clean_logs()
			return jsonify(msg="Historial de registros eliminado correctamente."), 200
	except Exception as e:
		write_log(e, "handling_logs()")
		return jsonify(err=f"Error en 'handling_logs()': {str(e)}"), 500


@app.route("/urls", methods=['GET'])
def getting_urls():
	try:
		urls = get_urls()
		return jsonify(urls), 200
	except Exception as e:
		write_log(e, "getting_urls()")
		return jsonify(err=f"Error en 'getting_urls()': {str(e)}"), 500


@app.route("/urls", methods=['POST', 'DELETE'])
def handling_url():
	file_urls = "urls.txt"
	url = request.get_json().get("url")
	regex_url = r'^https?:\/\/(?:localhost|(?:\d{1,3}\.){3}\d{1,3}|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?::\d+)?(?:\/.*)?$'

	try:
		urls = get_urls()
		if not isinstance(urls, list):
			raise Exception("Error al obtener las URLs.")

		if request.method == 'POST':
			if not url or not re.match(regex_url, url):
				exc = Exception("La URL proporcionada no es válida o no se proporcionó.")
				exc.status_code = 400
				raise exc
			if url in urls:
				exc = Exception(f"La URL '{url}' ya existe.")
				exc.status_code = 409
				raise exc
			with open(file_urls, 'a') as file:
				file.write(f"{url}\n")
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
			with open(file_urls, 'w') as file:
				for existing_url in urls:
					file.write(f"{existing_url}\n")
			return jsonify(msg=f"URL '{url}' eliminada de forma satisfactoria."), 200
	except Exception as e:
		write_log(e, "handling_url()")
		return jsonify(err=f"Error en 'handling_url()': {str(e)}"), getattr(e, "status_code", 500)


if __name__ == '__main__':
	Thread(target=keep_alive, daemon=True).start()
	app.run()
