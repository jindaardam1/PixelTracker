import os
import sqlite3
from datetime import datetime
import ipaddress
import re

from colorama import Fore
from src.utils.LogManager import Logs
from src.utils.IpToLocation import IpToLocation


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

            ip_info = IpToLocation.get_ip_info(ip)

            location = ip_info.__getitem__(0)
            zip_code = ip_info.__getitem__(1)

            # Use a parameterized query to avoid SQL injection
            ins = ("INSERT INTO EmailsAbiertos (email_guardado_id, ip, location, zip, user_agent, fecha_abierto) " +
                   "VALUES (?, ?, ?, ?, ?, ?);")
            values = (id_user, ip, location, zip_code,  user_agent, current_datetime)

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

        # Limit the size to a maximum of 150 characters
        cleaned_user_agent = cleaned_user_agent[:150]

        # Check for SQL keywords
        sql_keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'TABLE', 'CREATE']
        if any(keyword in cleaned_user_agent.upper() for keyword in sql_keywords):
            return "User Agent removed due to security concerns"

        return cleaned_user_agent.strip()  # Remove leading and trailing spaces


class InsertNewEmails:
    NEW_EMAILS_FILE_PATH = os.path.join(os.getcwd(), "resources", "new_emails.txt")
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @staticmethod
    def read_new_emails():
        try:
            new_emails = []
            with open(InsertNewEmails.NEW_EMAILS_FILE_PATH, 'r') as txt:
                for line in txt:
                    new_emails.append(line.strip())
            return new_emails
        except IOError as e:
            # Log or handle the specific error for file reading
            print(f"Error reading new emails file: {e}")
            Logs.error_log_manager_custom(f"Error reading new emails file: {e}")
            return []

    @classmethod
    def _clear_file_content(cls):
        try:
            # Overwrite the file without including anything
            with open(cls.NEW_EMAILS_FILE_PATH, 'w'):
                pass
        except IOError as e:
            # Log or handle the specific error for file writing
            print(f"Error deleting content of new emails file: {e}")
            Logs.error_log_manager_custom(f"Error deleting content of new emails file: {e}")

    @classmethod
    def _is_valid_email(cls, email):
        try:
            if not bool(re.match(cls.email_pattern, email)):
                return False  # Return False immediately if the format is not valid

            # Perform a database query to check if the email already exists
            query = "SELECT COUNT(*) FROM EmailsGuardados WHERE email = ?;"

            # Connect to the database
            with sqlite3.connect(InsertDB.get_db_path()) as connection:
                cursor = connection.cursor()
                cursor.execute(query, (email,))
                result = cursor.fetchone()

            return result[0] == 0  # If result[0] is 0, it means the email does not exist in the database

        except sqlite3.Error as e:
            print(f"Error querying the database: {e}")
            return False  # Return False in case of any database error

    @classmethod
    def insert_new_emails(cls, emails):
        try:
            # Transform emails to a set with unique elements
            unique_emails = set(emails)

            # Connect to the database using a context manager
            with sqlite3.connect(InsertDB.get_db_path()) as conn:
                cursor = conn.cursor()

                # Use a transaction to ensure atomicity
                conn.execute("BEGIN TRANSACTION;")

                for new_email in unique_emails:
                    if not new_email.strip() == "":
                        if cls._is_valid_email(new_email):
                            # Use a parameterized query to avoid SQL injection
                            ins = "INSERT INTO EmailsGuardados (email) VALUES (?);"
                            values = (new_email,)

                            cursor.execute(ins, values)

                            print(f"\t{Fore.GREEN}Email inserted into the database: "
                                  f"{Fore.BLUE} {new_email} {Fore.RESET}")
                        else:
                            print(f"\t{Fore.RED}Email{Fore.BLUE} {new_email} {Fore.RED}" +
                                  f" is not a valid email or already exists{Fore.RESET}")

                # Commit the changes to the database
                conn.execute("COMMIT;")

            cls._clear_file_content()

        except sqlite3.Error as e:
            # Log any SQLite errors
            print(f"{Fore.RED}\tError inserting data into EmailsGuardados table: {e} {Fore.RESET}")
            Logs.error_log_manager_custom(f"Error inserting data into EmailsGuardados table: {e}")
