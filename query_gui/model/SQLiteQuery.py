import sqlite3

from tabulate import tabulate


class DatabaseQuery:
    @staticmethod
    def execute_query_and_get_html(query):
        try:
            conn = sqlite3.connect('/db/Datos.db')

            cursor = conn.cursor()

            cursor.execute(query)

            results = cursor.fetchall()

            conn.close()

            html_table = tabulate(results, headers=[desc[0] for desc in cursor.description], tablefmt='html')

            return html_table
        except Exception as e:
            return f"Error executing query: {str(e)}"
