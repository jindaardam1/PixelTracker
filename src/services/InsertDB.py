import os
import sqlite3
from datetime import datetime
import ipaddress

from colorama import Fore
from src.utils.LogManager import Logs


class InsertDB:
    DB_FOLDER = 'db'
    DB_NAME = 'Datos.db'

    @classmethod
    def get_db_path(cls):
        return os.path.join(os.getcwd(), cls.DB_FOLDER, cls.DB_NAME)

    @classmethod
    def insert_email_opening_db(cls, id_user, ip, user_agent):
        conn = None
        try:
            # Get the current date and time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Connect to the database
            conn = sqlite3.connect(cls.get_db_path())
            cursor = conn.cursor()

            # Use a parameterized query to avoid SQL injection
            ins = "INSERT INTO EmailsAbiertos (email_guardado_id, ip, user_agent, fecha_abierto) VALUES (?, ?, ?, ?);"
            values = (id_user, ip, user_agent, current_datetime)

            cursor.execute(ins, values)

            # Commit the changes to the database
            conn.commit()

            print(Fore.LIGHTMAGENTA_EX + "\tUser information inserted into the database." + Fore.RESET)

        except sqlite3.Error as e:
            # Log any SQLite errors
            Logs.error_log_manager_custom(f"Error inserting data into EmailsAbiertos table: {e}")

        finally:
            if conn:
                conn.close()


class DataValidator:
    @staticmethod
    def validate_email_opening_data(id_user, ip, user_agent):
        validated_id = DataValidator._id_validation(id_user)
        validated_ip = DataValidator._ip_validation(ip)
        validated_user_agent = DataValidator._user_agent_validation(user_agent)

        InsertDB.insert_email_opening_db(validated_id, validated_ip, validated_user_agent)

    @staticmethod
    def _id_validation(id_user):
        conn = None
        try:
            # Connect to the database
            conn = sqlite3.connect(InsertDB.get_db_path())
            cursor = conn.cursor()

            # Get the number of entries in the EmailsGuardados table
            cursor.execute("SELECT COUNT(*) FROM EmailsGuardados;")
            num_entries = cursor.fetchone()[0]

            # Validate that the ID is an integer between 1 and the number of entries
            if isinstance(id_user, int) and 1 <= id_user <= num_entries:
                return id_user
            else:
                # Return 0 if the ID is not valid
                return 0

        except sqlite3.Error as e:
            # Log any SQLite errors
            Logs.error_log_manager_custom(f"Error validating ID: {e}")
            # Return 0 in case of an error
            return 0

        finally:
            # Close the connection, if it exists
            if conn:
                conn.close()

    @staticmethod
    def _ip_validation(ip):
        try:
            # Try to create an ipaddress.IPv4Address or ipaddress.IPv6Address object
            ip_obj = ipaddress.ip_address(ip)
            return str(ip_obj)  # Returns the IP if it is valid

        except ValueError:
            # If an exception is raised, the string does not represent a valid IP
            return None

    @staticmethod
    def _user_agent_validation(user_agent):
        # Remove special and potentially dangerous characters
        cleaned_user_agent = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in user_agent)
        return cleaned_user_agent.strip()  # Remove leading and trailing spaces
