import os
from flask import Flask, send_file, request
from colorama import init, Fore, Style

from src.services.CreateDB import CreateDB
from src.utils.LogManager import Logs

# Author: Jagoba Inda

init()

app = Flask(__name__)


@app.route('/pix.png')
def tracker():
    try:
        # Get the full path of the image
        image_path = os.path.join(os.path.dirname(__file__), '../..', 'resources', 'pixel.png')

        # Safely get the client's IP address
        user_ip = request.remote_addr

        # Other additional information
        user_agent = request.headers.get('User-Agent')
        method = request.method
        url = request.url
        query_parameters = request.args
        user_id = query_parameters.get('id')

        # Colored console log
        print(Fore.GREEN + "-- A new email opening has been logged --" + Style.RESET_ALL)
        print(f'\tEmail opened by {Fore.BLUE}{user_ip}{Style.RESET_ALL}')
        print(f'\tUser-Agent: {Fore.BLUE}{user_agent}{Style.RESET_ALL}')
        print(f'\tMethod: {method}, URL: {url}, Query Parameters: {query_parameters}')
        print(f'\tUser ID: {Fore.YELLOW}{user_id}{Fore.RESET}')
        print(Fore.RED + "\t", end="")
        Logs.info_log_manager("New email opening logged in the database with IP " + user_ip)
        print(Style.RESET_ALL, end="")

        # Return the 1-pixel image
        return send_file(image_path)
    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {e}")
        Logs.error_log_manager(e)
        return "An error occurred", 500  # HTTP status code 500 indicates internal server error


if __name__ == '__main__':
    # Run the application in debug mode only during development
    app.run(debug=False)

print(Fore.LIGHTGREEN_EX + "Server loaded successfully" + Fore.RESET)

CreateDB.create_database()
