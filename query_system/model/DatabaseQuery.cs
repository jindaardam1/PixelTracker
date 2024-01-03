using System;
using System.Data;
using System.Data.SQLite;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace PixelTrackerDBQuery.Model
{
    class DatabaseQuery
    {
        static string connectionString = "Data Source=../db/Datos.db;Version=3;";

        public static async Task ExecuteDatabaseQueryAsync(string query)
        {
            try
            {
                using (SQLiteConnection connection = new SQLiteConnection(connectionString))
                {
                    await connection.OpenAsync();

                    using (SQLiteCommand command = new SQLiteCommand(query, connection))
                    {
                        using (SQLiteDataAdapter adapter = new SQLiteDataAdapter(command))
                        {
                            DataTable dataTable = new DataTable();
                            await Task.Run(() => adapter.Fill(dataTable));

                            ShowDataOnBrowser(ConvertDataTableToHtml(dataTable));
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error executing the query: {ex.Message}");
            }
        }

        private static string ConvertDataTableToHtml(DataTable dataTable)
        {
            try
            {
                // Load CSS and JS from files
                string css = LoadCodeFromFile("style/query.css");
                string js = LoadCodeFromFile("js/copy.js");

                if (dataTable == null || dataTable.Rows.Count == 0)
                {
                    return $"<html><head><style>{css}</style></head><body><p>No data available</p></body></html>";
                }

                StringBuilder htmlTable = new StringBuilder();
                htmlTable.Append("<html><head><style>").Append(css).Append("</style></head><body><table border='1'><tr>");

                // Add column headers
                foreach (DataColumn column in dataTable.Columns)
                {
                    htmlTable.Append($"<th>{column.ColumnName}</th>");
                }
                htmlTable.Append("</tr>");

                // Add rows and data
                foreach (DataRow row in dataTable.Rows)
                {
                    htmlTable.Append("<tr>");
                    foreach (DataColumn column in dataTable.Columns)
                    {
                        htmlTable.Append($"<td>{row[column]}</td>");
                    }
                    htmlTable.Append("</tr>");
                }

                htmlTable.Append($@"</table>
                            <button id=""buttonCopyToClipboard"">Copy Emails to Clipboard</button>
                            <script>{js}</script>
                            </body></html>");

                return htmlTable.ToString();
            }
            catch (Exception ex)
            {
                // Handle the exception
                return $"<html><body><p>Error generating HTML table: {ex.Message}</p></body></html>";
            }
        }

        private static void ShowDataOnBrowser(string htmlData)
        {
            try
            {
                // Create a temporary file with .html extension
                string tempFilePath = Path.Combine(Path.GetTempPath(), "query.html");

                // Write the HTML to the temporary file
                File.WriteAllText(tempFilePath, htmlData);

                // Open the file in the default browser
                Process.Start(new ProcessStartInfo
                {
                    FileName = tempFilePath,
                    UseShellExecute = true
                });
            }
            catch (Exception ex)
            {
                // Handle the exception
                MessageBox.Show($"Error displaying data in the browser: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private static string LoadCodeFromFile(string path)
        {
            try
            {
                // file path
                string filePath = Path.Combine("..", "resources", path);

                // Check if the file exists
                if (!File.Exists(filePath))
                {
                    throw new FileNotFoundException("The file was not found.", filePath);
                }

                // Read the content of the file
                return File.ReadAllText(filePath);
            }
            catch (Exception ex)
            {
                // Handle the exception (you can print the message, log it, etc.)
                MessageBox.Show($"Error loading code from file: {ex.Message}");
                return string.Empty;
            }
        }
    }
}
