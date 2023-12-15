import os
from datetime import datetime


class Logs:
    @staticmethod
    def error_log_manager(exception):
        """Logs an error in the error log.

        Args:
            exception (Exception): The exception to be logged.
        """
        Logs._add_log(Logs._create_string_log("ERROR", str(exception)))

    @staticmethod
    def error_log_manager_custom(custom_error_message):
        """Logs a custom error in the error log.

        Args:
            custom_error_message (str): The custom error message to be logged.
        """
        Logs._add_log(Logs._create_string_log("ERROR", custom_error_message))

    @staticmethod
    def debug_log_manager(message):
        """Logs a debug message in the event log.

        Args:
            message (str): The debug message to be logged.
        """
        Logs._add_log(Logs._create_string_log("DEBUG", message))

    @staticmethod
    def info_log_manager(message):
        """Logs an information message in the event log.

        Args:
            message (str): The information message to be logged.
        """
        Logs._add_log(Logs._create_string_log("INFO", message))

    @staticmethod
    def _create_string_log(log_type, log_message):
        """Creates a formatted log string.

        Args:
            log_type (str): The log type (e.g., "INFO", "ERROR", "DEBUG").
            log_message (str): The log message.

        Returns:
            str: The formatted log string.
        """
        log_format = "{} [{}] -> {}"
        return log_format.format(Logs._get_current_datetime(), log_type, log_message)

    @staticmethod
    def _add_log(new_log):
        """Adds a log entry to the current month's log file.

        Args:
            new_log (str): The log entry to be added.
        """
        log_file = Logs._load_current_month_log()

        try:
            with open(log_file, 'a') as log_file_writer:
                log_file_writer.write(new_log + '\n')
                print("Added log entry.")
        except IOError as e:
            print("Error adding log to file: {}".format(e))

    @staticmethod
    def _load_current_month_log():
        """Loads the log file for the current month.

        Returns:
            str: The log file for the current month.
        """
        log_folder = Logs._load_logs_folder()
        current_date = datetime.now()
        file_name = current_date.strftime("%Y-%m") + ".log"
        log_file = os.path.join(log_folder, file_name)

        try:
            if not os.path.isfile(log_file):
                open(log_file, 'a').close()
                print("File '{}' created successfully.".format(file_name))
        except IOError as e:
            print("Failed to load log file: {}".format(e))
            pass

        return log_file

    @staticmethod
    def _load_logs_folder():
        """Loads the logs folder.

        Returns:
            str: File object representing the logs folder.
        """
        logs_folder = "logs"

        try:
            if not os.path.exists(logs_folder):
                os.makedirs(logs_folder)
                print("Folder 'logs' created successfully.")
        except OSError as e:
            print("Failed to create 'logs' folder: {}".format(e))
            pass

        return logs_folder

    @staticmethod
    def _get_current_datetime():
        """Returns the current date and time formatted as a string.

        Returns:
            str: The current date and time in the "yyyy-MM-dd HH:mm:ss" format.
        """
        now = datetime.now()
        formatter = "%Y-%m-%d %H:%M:%S"
        return now.strftime(formatter)
