using System.Data;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.VisualBasic.FileIO;

namespace XMLDataSetProcessorW;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    #region Definitions

    private static string? XMLFilesPath;
    private string? DataPath = "C:\\Users\\K.Rrapaj\\Desktop\\Back-up\\Data.csv";
    private const string DataFieldName = "DATA_FIELD_NAME";
    private const string Group = "GROUP";
    private const string Category = "CATEGORY";
    private const string Visibilities = "VISIBLE";
    private const string Editable = "EDITABLE";
    private const string Nullable = "NULLABLE";

    private static List<string?> DataFieldNames = new List<string?>();
    private static List<string?> Groups = new List<string?>();
    private static List<string?> Categories = new List<string?>();
    private static List<string?> Visibles = new List<string?>();
    private static List<string?> Editables = new List<string?>();
    private static List<string?> Nullables = new List<string?>();

        
    #endregion
    
    public MainWindow()
    {
        InitializeComponent();
    }

    private void ProcessDataButtonClick(object sender, RoutedEventArgs e)
    {
        XMLFilesPath = @$"{txtXMLPath.Text}\";
        
        //CheckPath();
        
        string[] XMLFiles = Directory.GetFiles(XMLFilesPath, "*.xml");

        ProcessData(DataPath);

        foreach (var file in XMLFiles)
        {
            DataSet dataSet = new DataSet();
            dataSet.ReadXml(file);
            
            ProcessFile(file, dataSet);
        }
    }
    
    private static void ProcessData(string dataPath)
        {   
            using TextFieldParser parser = new(dataPath);
            parser.TextFieldType = FieldType.Delimited;
            parser.SetDelimiters(",");
            
            while (!parser.EndOfData)
            {
                string[]? readFields = parser.ReadFields();
                
                DataFieldNames.Add(readFields[0]);
                Groups.Add(readFields[1]);
                Categories.Add(readFields[2]);
                Visibles.Add(readFields[3]);
                Editables.Add(readFields[4]);
                Nullables.Add(readFields[5]);
            }
        }

        private void ProcessFile(string file, DataSet dataSet)
        {
            errorLabel.Content += "\nProcessing file: " + file;
            errorLabel.Foreground = Brushes.Green;
            AddColumns(file, dataSet);
            SetColumns(file, dataSet);
        }

        private static void SetColumns(string file, DataSet dataSet)
        {
            for (int i = 0; i < DataFieldNames.Count; i++)
            {
                foreach (DataRow row in dataSet.Tables[0].Rows)
                {
                    string? dataFieldName = row[DataFieldName].ToString();
                    
                    if (dataFieldName.Contains(DataFieldNames[i]))
                    {
                        row[Group] = Groups[i];
                        row[Category] = Categories[i];
                        row[Visibilities] = Visibles[i];
                        row[Editable] = Editables[i];
                        row[Nullable] = Nullables[i];
                    }
                }
            }
            dataSet.WriteXml(file);
        }

        private static void AddColumns(string file, DataSet dataSet)
        {
            if (dataSet.Tables[0].Columns.Contains(Category) && dataSet.Tables[0].Columns.Contains(Group))
            {
                return;
            }
            dataSet.Tables[0].Columns.Add(Category, typeof(string));
            dataSet.Tables[0].Columns.Add(Group, typeof(string));

            foreach (DataRow row in dataSet.Tables[0].Rows)
            {
                row["CATEGORY"] = "";
                row["GROUP"] = "";
            }
            dataSet.WriteXml(file);
        }

        private void CheckPath()
        {
            
                if (XMLFilesPath == null || !Directory.Exists(XMLFilesPath))
                {
                    errorLabel.Content = "Please enter a valid XML path";
                }

                if (DataPath == null || !Directory.Exists(DataPath))
                {
                    errorLabel.Content = "Please enter a valid DATA path";
                }
            
        }
}