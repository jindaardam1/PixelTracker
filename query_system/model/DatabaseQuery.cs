using System;
using System.Data;
using System.Data.SQLite;
using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Windows.Controls;

namespace PixelTrackerDBQuery.Model
{
    class DatabaseQuery
    {
        static string connectionString = "Data Source=../db/Datos.db;Version=3;";
        public static void ExecuteDatabaseQuery(string query)
        {
            try
            {
                using (SQLiteConnection connection = new SQLiteConnection(connectionString))
                {
                    connection.Open();

                    using (SQLiteCommand command = new SQLiteCommand(query, connection))
                    {
                        using (SQLiteDataAdapter adapter = new SQLiteDataAdapter(command))
                        {
                            DataTable dataTable = new DataTable();
                            adapter.Fill(dataTable);

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
                // Load CSS from file
                string css = LoadCssFromFile();

                if (dataTable == null || dataTable.Rows.Count == 0)
                {
                    return $"<html><head><style>{css}</style></head><body><p>No data available</p></body></html>";
                }

                string htmlTable = $"<html><head><style>{css}</style></head><body><table border='1'><tr>";

                // Add column headers
                foreach (DataColumn column in dataTable.Columns)
                {
                    htmlTable += $"<th>{column.ColumnName}</th>";
                }
                htmlTable += "</tr>";

                // Add rows and data
                foreach (DataRow row in dataTable.Rows)
                {
                    htmlTable += "<tr>";
                    foreach (DataColumn column in dataTable.Columns)
                    {
                        htmlTable += $"<td>{row[column]}</td>";
                    }
                    htmlTable += "</tr>";
                }

                htmlTable += "</table></body></html>";

                return htmlTable;
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
                string tempFilePath = Path.Combine(Path.GetTempPath(), "tempfile.html");

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


        private static string LoadCssFromFile()
        {
            try
            {
                // CSS file path
                string cssFilePath = Path.Combine("..", "resources", "style", "query.css");

                // Check if the CSS file exists
                if (!File.Exists(cssFilePath))
                {
                    throw new FileNotFoundException("The CSS file was not found.", cssFilePath);
                }

                // Read the content of the CSS file
                string cssContent = File.ReadAllText(cssFilePath);

                return cssContent;
            }
            catch (Exception ex)
            {
                // Handle the exception (you can print the message, log it, etc.)
                MessageBox.Show($"Error loading CSS from file: {ex.Message}");
                return string.Empty;
            }
        }
    }
}
