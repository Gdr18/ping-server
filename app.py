from flask import Flask, request, jsonify
from threading import Thread

from utils import get_urls, loop_pings, clean_logs

app = Flask(__name__)


@app.route('/')
def welcome():
	return jsonify(msg="Bienvenidx a Ping Server!"), 200


@app.route("/logs")
def getting_logs():
	file_logs = 'logs.txt'
	try:
		with open(file_logs) as file:
			logs = file.readlines()
		return jsonify(logs), 200
	except FileNotFoundError:
		return jsonify("No hay registros aún. Vuelva a intentarlo dentro de un rato."), 404
	except Exception as e:
		return jsonify(err=f"Error al leer '{file_logs}': {str(e)}"), 500


@app.route("/logs", methods=['DELETE'])
def deleting_logs():
	clean_logs()
	return jsonify(msg="Registros limpiados de forma satisfactoria."), 200


@app.route("/urls", methods=['GET'])
def getting_urls():
	urls = get_urls()
	return jsonify(urls), 200


@app.route("/urls", methods=['POST'])
def adding_url():
	file_urls = 'urls.txt'
	new_url = request.json.get('url').lower().strip()
	urls = get_urls()
	if new_url in urls:
		return jsonify(err=f"La URL '{new_url}' ya existe."), 400
	try:
		with open(file_urls, 'a') as file:
			file.write(f"{new_url}\n")
		return jsonify(msg=f"URL '{new_url}' añadida de forma satisfactoria."), 201
	except Exception as e:
		return jsonify(err=f"Error al escribir en '{file_urls}': {str(e)}"), 500


@app.route("/urls/<url>", methods=['DELETE'])
def deleting_url(url):
	url = url.lower().strip()
	file_urls = 'urls.txt'
	urls = get_urls()
	if url not in urls:
		return jsonify(err=f"La URL '{url}' no existe."), 404
	urls.remove(url)
	try:
		with open(file_urls, 'w') as file:
			for existing_url in urls:
				file.write(f"{existing_url}\n")
		return jsonify(msg=f"URL '{url}' eliminada de forma satisfactoria."), 200
	except Exception as e:
		return jsonify(err=f"Error al escribir en '{file_urls}': {str(e)}"), 500


if __name__ == '__main__':
	Thread(target=loop_pings, daemon=True).start()
	app.run()
