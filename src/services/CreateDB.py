import os
import sqlite3

from colorama import Fore

from src.utils.LogManager import Logs


class CreateDB:
    DB_FOLDER = 'db'
    DB_NAME = 'Datos.db'

    @staticmethod
    def _get_create_document():
        # Path to the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), '../..', 'resources', 'createTable.sql')

        try:
            # Open the file in read mode
            with open(sql_file_path, 'r') as sql_file:
                # Read the content of the file
                create_sql = sql_file.read()
                return create_sql
        except FileNotFoundError:
            print(f"Error: The file {sql_file_path} was not found.")
            return None

    @classmethod
    def _get_db_path(cls):
        return os.path.join(os.getcwd(), cls.DB_FOLDER, cls.DB_NAME)

    @classmethod
    def create_database(cls):
        if not cls.check_if_db_exists():
            conn = None
            try:
                # Create the db folder if it doesn't exist
                db_folder_path = os.path.join(os.getcwd(), cls.DB_FOLDER)
                if not os.path.exists(db_folder_path):
                    os.mkdir(db_folder_path)
                    print(f"The '{cls.DB_FOLDER}' folder has been created.")

                # Connect to the database or create it if it doesn't exist
                db_file_path = cls._get_db_path()
                conn = sqlite3.connect(db_file_path)

                # Create a cursor object to execute SQL commands
                cursor = conn.cursor()

                # Get the SQL string for table creation
                sql_string = cls._get_create_document()

                if sql_string is not None:
                    # Create the EmailsAbiertos table
                    cursor.execute(sql_string)
                else:
                    # Log an error if there's an issue getting the SQL script
                    Logs.error_log_manager_custom("Error getting the database table creation script")

                # Commit to save the changes
                conn.commit()

                # Log a debug message with the path to the database file
                Logs.debug_log_manager(f"Database set to run. Database file path: {db_file_path}")
                print(Fore.CYAN + f"Database set to run. Database file path: {db_file_path}" + Fore.RESET)

            except sqlite3.Error as e:
                # Log any SQLite errors
                Logs.error_log_manager_custom(f"SQLite error: {e}")
            except OSError as e:
                Logs.error_log_manager_custom(f"Error creating the folder '{cls.DB_FOLDER}': {e}")
            except Exception as e:
                Logs.error_log_manager_custom(f"An unexpected error occurred: {e}")

            finally:
                # Close the connection in the 'finally' block to ensure it's always closed
                if conn:
                    conn.close()
        else:
            print(Fore.CYAN + f"Database set to run" + Fore.RESET)

    @classmethod
    def check_if_db_exists(cls):
        # Verificar si la base de datos existe
        db_file_path = cls._get_db_path()
        return os.path.exists(db_file_path)
