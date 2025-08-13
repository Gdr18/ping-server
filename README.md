# 🟢 Ping Server – Keep-Alive de URLs, API REST y Logs

Este proyecto es un servidor en Python que no solo realiza pings periódicos a una lista de URLs para mantener activos servicios web (ideal para evitar que se duerman en hostings gratuitos), sino que también expone una API ligera para gestionar dinámicamente el sistema.

⚠️ **Limitaciones en hostings gratuitos:** 
- Suspensión automática por inactividad (reinicios → pérdida de archivos .txt).
- Almacenamiento no fiable para urls.txt y logs.txt.
- Restricciones de rate limit al realizar pings periódicos.
- Por ello se recomienda ejecutarlo en un entorno controlado (equipo local, Raspberry Pi, contenedor siempre activo)

---

## 🚀 Tecnologías utilizadas

- **Python 3**
- **requests** – Para realizar peticiones HTTP
- **datetime** y **time** – Gestión de fechas y temporizadores
- **Flask** 

---

## ✨ Funcionalidades principales

- Keep-Alive de URLs:
  - Lee una lista de URLs desde `urls.txt`
  - Realiza pings periódicos a cada URL y registra el estado en `logs.txt`
  - Limpieza automática de logs el día configurado de cada mes
  - Registro de errores en `logs.txt`'

- API REST:
  - Permite añadir nuevas URLs, solicitar las existentes o eliminarlas a través del endpoint `/urls`
  - Permite leer el historial de logs y limpiarlo a través del endpoint `/logs`

---

## ⚙️ Instalación y uso

1. Clona este repositorio:
```bash
git clone https://github.com/Gdr18/ping-server.git
cd ping_server  
```
2. Crea y activa un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate
```
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```
4. Ejecuta el script principal:
```bash
python app.py
```
---

## 📝 Archivos importantes

- `utils.py`: Lógica principal de monitorización y loop periódico.
- `app.py`: Punto de entrada del servidor y configuración de rutas.

### ⚠️ Nota importante!
Este proyecto no trabaja con una base de datos, sino que utiliza archivos de texto (`urls.txt` y `logs.txt`) para almacenar la información.
No hace falta crear los archivos `urls.txt` ni `logs.txt`, el script los crea automáticamente si no existen.

---

## ⚙️ Variables configurables

- `INTERVAL`: Intervalo entre solicitudes (segundos).

---

## 📓 Documentación de la API

Puedes consultar la documentación y probar todos los endpoints desde la colección de Postman: 
🔗 [Colección de Postman](https://.postman.co/workspace/My-Workspace~959b1184-c553-4747-8bce-84d1bf72923a/collection/26739293-8e0873ea-2de2-468f-baf1-e6770c96f6c3?action=share&creator=26739293)

---

## 👩‍💻 Autor

Desarrollado por **Gádor García Martínez**  
[GitHub](https://github.com/Gdr18) · [LinkedIn](https://www.linkedin.com/in/g%C3%A1dor-garc%C3%ADa-mart%C3%ADnez-99a33717b/)

