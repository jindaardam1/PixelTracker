import os
from flask import Flask, send_file, request
from colorama import init, Fore, Style
from src.utils.LogManager import Logs

# Author: Jagoba Inda

init()

app = Flask(__name__)


@app.route('/tracker.png')
def tracker():
    # Get the full path of the image
    image_path = os.path.join(os.path.dirname(__file__), '../..', 'resources', 'pixel.png')

    # Try to get the public IP from the X-Forwarded-For header (in case behind a proxy)
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Other additional information
    user_agent = request.headers.get('User-Agent')
    method = request.method
    url = request.url
    query_parameters = request.args

    # Log the email opening and user IP along with other information
    print(Fore.GREEN + "-- A new email opening has been logged --" + Style.RESET_ALL)
    print(f'\tEmail opened by {Fore.BLUE}{user_ip}{Style.RESET_ALL}')
    print(f'\tUser-Agent: {Fore.BLUE}{user_agent}{Style.RESET_ALL}')
    print(f'\tMethod: {method}, URL: {url}, Query Parameters: {query_parameters}')
    print(Fore.RED + "\t", end="")
    Logs.info_log_manager("New email opening logged in the database with IP " + user_ip)
    print(Style.RESET_ALL, end="")

    # Serve the 1-pixel generic image (transparent image)
    return send_file(image_path)


if __name__ == '__main__':
    app.run(debug=True)
