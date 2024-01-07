using PixelTrackerDBQuery.Model;
using System;
using System.Data;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace PixelTrackerDBQuery
{
    /// <summary>
    /// Lógica de interacción para MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private async void OnCustomQueryButtonClick(object sender, RoutedEventArgs e)
        {
            CustomQueryButton.IsEnabled = false;

            DataTable query = await DatabaseQuery.ExecuteDatabaseQueryAsync(TextBoxCustomQuery.Text);
            DatabaseQuery.ShowDataOnBrowser(DatabaseQuery.ConvertDataTableToHtml(query));

            CustomQueryButton.IsEnabled = true;
        }

        private void OnClearCustomQueryButtonClick(object sender, RoutedEventArgs e)
        {
            TextBoxCustomQuery.Text = "";
        }

        private async void OnUserQueryButtonClick(object sender, RoutedEventArgs e)
        {
            UserQueryButton.IsEnabled = false;

            var userID = UserIdTextBox.Text;
            var order = OrderByComboBox.SelectedItem as ComboBoxItem;

            if (userID != "" && int.TryParse(userID, out int idAsInt))
            {
                DataTable query = await DatabaseQuery.ExecuteDatabaseQueryAsync(GetUserIdQueryString(idAsInt, order));
                DatabaseQuery.ShowDataOnBrowser(DatabaseQuery.ConvertDataTableToHtml(query));
            }
            else
            {
                MessageBox.Show("ID is required.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }



            UserQueryButton.IsEnabled = true;
        }

        private void OnClearUserQueryButtonClick(object sender, RoutedEventArgs e)
        {
            UserIdTextBox.Text = "";
            OrderByComboBox.SelectedIndex = 0;
        }

        private async void OnLocationQueryButtonClick(object sender, RoutedEventArgs e)
        {
            LocationQueryButton.IsEnabled = false;

            var location = LocationTextBox.Text;
            var order = OrderByComboBoxLocation.SelectedItem as ComboBoxItem;

            if (location != "")
            {
                DataTable query = await DatabaseQuery.ExecuteDatabaseQueryAsync(GetLocationQueryString(location, order));
                DatabaseQuery.ShowDataOnBrowser(DatabaseQuery.ConvertDataTableToHtml(query));
            }
            else
            {
                MessageBox.Show("Location is required.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }

            LocationQueryButton.IsEnabled = true;
        }

        private void OnClearLocationQueryButtonClick(object sender, RoutedEventArgs e)
        {
            LocationTextBox.Text = "";
            OrderByComboBoxLocation.SelectedIndex = 0;
        }

        private async void OnSearchEmailButtonClick(object sender, RoutedEventArgs e)
        {
            var email = EmailTextBox.Text;

            if (email != "")
            {
                string queryString = GetEmailQueryString(email);

                SearchEmailButton.IsEnabled = false;

                DataTable queryRes = await DatabaseQuery.ExecuteDatabaseQueryAsync(queryString);
                var exists = CheckEmailExists(queryRes);

                if (exists)
                {
                    var queryID = $"SELECT id FROM EmailsGuardados WHERE email = '{email}'";
                    DataTable emailIdQueryTable = await DatabaseQuery.ExecuteDatabaseQueryAsync(queryID);
                    var emailID = GetEmailID(emailIdQueryTable);

                    EmailFoundTextBlock.Foreground = new SolidColorBrush(Colors.Green);
                    EmailFoundTextBlock.Text = $"Email found! [ID = {emailID}]";
                }
                else
                {
                    EmailFoundTextBlock.Foreground = new SolidColorBrush(Colors.Red);
                    EmailFoundTextBlock.Text = "Email not found!";
                }

                SearchEmailButton.IsEnabled = true;
            }
        }

        private void OnRunEmailServerButtonClick(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Email server comming soon...", "Email server", MessageBoxButton.OK, MessageBoxImage.Information) ;
        }

        private string GetUserIdQueryString(int userID, ComboBoxItem order)
        {
            return "SELECT EA.*, EG.email " +
                "FROM EmailsAbiertos EA " +
                "JOIN EmailsGuardados EG ON EA.email_guardado_id = EG.id " +
                $"WHERE EA.email_guardado_id = {userID} " +
                $"ORDER BY EA.{GetOrderByColumn(order.Content.ToString())};";
        }

        private string GetLocationQueryString(string location, ComboBoxItem order)
        {
            return "SELECT EA.*, EG.email " +
                "FROM EmailsAbiertos EA " +
                "JOIN EmailsGuardados EG ON EA.email_guardado_id = EG.id " +
                $"WHERE EA.location = '{location}' " +
                $"ORDER BY EA.{GetOrderByColumn(order.Content.ToString())};";
        }

        private string GetOrderByColumn(string comboBoxString)
        {
            switch (comboBoxString)
            {
                case "DATE":
                    return "fecha_abierto";
                case "IP":
                    return "ip";
                case "ID":
                    return "id";
                case "LOCATION":
                    return "location";
                default:
                    return "fecha_abierto";
            }
        }

        private string GetEmailQueryString(string email)
        {
            return $"SELECT COUNT(*) FROM EmailsGuardados WHERE email = '{email}'";
        }

        public static bool CheckEmailExists(DataTable dataTable)
        {
            try
            {
                if (dataTable != null && dataTable.Rows.Count > 0)
                {
                    int emailCount = Convert.ToInt32(dataTable.Rows[0][0]);

                    if (emailCount == 1 || emailCount == 0)
                    {
                        return emailCount == 1;
                    }
                    else
                    {
                        Console.WriteLine($"Unexpected email count: {emailCount}");
                        return false;
                    }
                }
                else
                {
                    Console.WriteLine("DataTable is null or empty");
                    return false;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error checking email existence: {ex.Message}");
                return false;
            }
        }

        public static int GetEmailID(DataTable queryTable)
        {
            try
            {
                if (queryTable?.Rows.Count > 0)
                {
                    if (int.TryParse(queryTable.Rows[0]["id"].ToString(), out int emailID))
                    {
                        return emailID;
                    }
                    else
                    {
                        Console.WriteLine("Error converting 'id' to int.");
                    }
                }
                else
                {
                    Console.WriteLine("DataTable is null or empty.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting email ID: {ex.Message}");
            }

            return 0;
        }

    }
}
