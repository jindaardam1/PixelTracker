using PixelTrackerDBQuery.Model;
using System.Windows;
using System.Windows.Controls;

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

            await DatabaseQuery.ExecuteDatabaseQueryAsync(TextBoxCustomQuery.Text);

            CustomQueryButton.IsEnabled = true;
        }

        private void OnClearCustomQueryButtonClick(object sender, RoutedEventArgs e)
        {
            TextBoxCustomQuery.Text = "";
        }

        private async void OnUserQueryButtonClick(object sender, RoutedEventArgs e)
        {
            UserQueryButton.IsEnabled = false;

            await DatabaseQuery.ExecuteDatabaseQueryAsync(GetUserIdQueryString());

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

            await DatabaseQuery.ExecuteDatabaseQueryAsync(GetLocationQueryString());

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
                string query = GetEmailQueryString(email);

                SearchEmailButton.IsEnabled = false;

                await DatabaseQuery.ExecuteDatabaseQueryAsync(query);

                SearchEmailButton.IsEnabled = true;
            }
        }

        private void OnRunEmailServerButtonClick(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Email server comming soon...", "Email server", MessageBoxButton.OK, MessageBoxImage.Information) ;
        }

        private string GetUserIdQueryString()
        {
            var userID = UserIdTextBox.Text;
            var order = OrderByComboBox.SelectedItem as ComboBoxItem;


            if (userID != "" && int.TryParse(userID, out int idAsInt))
            {
                return "SELECT EA.*, EG.email " +
                "FROM EmailsAbiertos EA " +
                "JOIN EmailsGuardados EG ON EA.email_guardado_id = EG.id " +
                $"WHERE EA.email_guardado_id = {idAsInt} " +
                $"ORDER BY EA.{GetOrderByColumn(order.Content.ToString())};";
            }
            else
            {
                MessageBox.Show("ID is required.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }
        }

        private string GetLocationQueryString()
        {
            var location = LocationTextBox.Text;
            var order = OrderByComboBoxLocation.SelectedItem as ComboBoxItem;


            if (location != "")
            {
                return "SELECT EA.*, EG.email " +
                "FROM EmailsAbiertos EA " +
                "JOIN EmailsGuardados EG ON EA.email_guardado_id = EG.id " +
                $"WHERE EA.location = '{location}' " +
                $"ORDER BY EA.{GetOrderByColumn(order.Content.ToString())};";
            }
            else
            {
                MessageBox.Show("Location is required.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }
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
            return $"SELECT COUNT(*) AS '0 = not found / 1 = found' FROM EmailsGuardados WHERE email = '{email}'";
        }
    }
}
