import os
import sqlite3
from datetime import datetime

from colorama import Fore
from src.utils.LogManager import Logs


class InsertDB:
    DB_FOLDER = 'db'
    DB_NAME = 'Datos.db'

    @classmethod
    def _get_db_path(cls):
        return os.path.join(os.getcwd(), cls.DB_FOLDER, cls.DB_NAME)

    @classmethod
    def insert_email_opening_db(cls, id_user, ip, user_agent):
        conn = None
        try:
            # Get the current date and time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Connect to the database
            conn = sqlite3.connect(cls._get_db_path())
            cursor = conn.cursor()

            # Use a parameterized query to avoid SQL injection
            ins = "INSERT INTO EmailsAbiertos (email_guardado_id, ip, user_agent, fecha_abierto) VALUES (?, ?, ?, ?);"
            cursor.execute(ins, (id_user, ip, user_agent, current_datetime))

            # Commit the changes to the database
            conn.commit()

        except sqlite3.Error as e:
            # Log any SQLite errors
            Logs.error_log_manager_custom(f"Error inserting data into EmailsAbiertos table: {e}")

        finally:
            if conn:
                conn.close()

