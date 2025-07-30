from flask import Flask, request, jsonify

from utils import reload_urls, urls

app = Flask(__name__)


@app.route('/')
def welcome():
	return jsonify(msg="Bienvenidx a Ping Server!"), 200


@app.route("/logs")
def get_logs():
	file_logs = 'logs.txt'
	try:
		with open(file_logs) as file:
			logs = file.readlines()
		return jsonify(logs), 200
	except FileNotFoundError:
		return jsonify("No hay registros aún. Vuelva a intentarlo dentro de un rato."), 404
	except Exception as e:
		return jsonify(err=f"Error al leer '{file_logs}': {str(e)}"), 500


@app.route("/urls", methods=['GET'])
def get_urls():
	reload_urls()
	return jsonify(urls), 200


@app.route("/urls", methods=['POST'])
def add_url():
	file_urls = 'urls.txt'
	new_url = request.json.get('url')
	if new_url in urls:
		raise ValueError(f"La URL '{new_url}' ya existe.")
	try:
		with open(file_urls, 'a') as file:
			file.write(f"\n{new_url}")
		reload_urls()
		return jsonify(msg=f"URL '{new_url}' añadida de forma satisfactoria."), 201
	except Exception as e:
		return jsonify(err=f"Error al escribir en '{file_urls}': {str(e)}"), 500


if __name__ == '__main__':
	app.run(debug=True)
