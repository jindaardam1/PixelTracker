import os
from flask import Flask, send_file, request
from src.utils.LogManager import Logs

# Author: Jagoba Inda

app = Flask(__name__)


@app.route('/tracker.png')
def tracker():
    # Obtiene la ruta completa de la imagen
    image_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'pixel.png')

    # Intenta obtener la IP pública desde el encabezado X-Forwarded-For (en caso de estar detrás de un proxy)
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Otras informaciones adicionales
    user_agent = request.headers.get('User-Agent')
    method = request.method
    url = request.url
    query_parameters = request.args

    # Registra la apertura del correo electrónico y la IP del usuario, junto con otras informaciones
    print("[32m-- Se ha registrado una nueva apertura de correo --[0m")
    print(f'\tCorreo electrónico abierto por[34m {user_ip}[0m')
    print(f'\t[34mUser-Agent:[0m {user_agent}')
    print(f'\tMethod: {method}, URL: {url}, Query Parameters: {query_parameters}')
    print("\t[31m", end="")
    Logs.info_log_manager("Nueva apertura de correo registrada en la base de datos con la ip" + user_ip)
    print("[0m", end="")

    # Sirve la imagen de 1 píxel genérico (imagen transparente)
    return send_file(image_path)


if __name__ == '__main__':
    app.run(debug=True)
