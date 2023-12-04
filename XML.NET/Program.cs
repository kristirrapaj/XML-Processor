using System;
using System.Data;
using System.IO;
using System.Xml;

namespace XMLProcessorTool;


/*
Questo tool sviluppato in C# legge un file XML e stampa a video i valori di due campi specifici
Usiamo la libreria di System.Data, che semplifica la lettura. I resultati vengono stampati in Console,
oppure file di testo, a base della funzione richiesta.
*/

internal class XMLProcessor
{
    private const string XMLFilePath = "C:\\Users\\K.Rrapaj\\Desktop\\daniele.xml";
    private const string OutputTXTFilePath = "C:\\Users\\K.Rrapaj\\Desktop\\output.txt";
    private const string DataFieldName = "DATA_FIELD_NAME";
    private const string Caption = "CAPTION";

    public static void Main(string[] args)
    {
        DataSet dataSet = new DataSet();
        dataSet.ReadXml(XMLFilePath, XmlReadMode.Auto);

        // Scrivi sulla CONSOLE
        WriteToConsole(dataSet, DataFieldName, Caption);

        // Scrivi su FILE
        WriteToFile(dataSet, DataFieldName, Caption, OutputTXTFilePath);

        Console.WriteLine("Press any key to exit.");
    }

    private static void WriteToConsole(DataSet dataSet, string dataFieldName, string caption)
    {
        foreach (DataTable table in dataSet.Tables)
        {
            foreach (DataRow row in table.Rows)
            {
                Console.WriteLine($"{row[dataFieldName]},{row[caption]}");
            }
        }
    }

    private static void WriteToFile(DataSet dataSet, string dataFieldName, string caption, string outputPath)
    {
        using var writer = new StreamWriter(outputPath);
        foreach (DataTable table in dataSet.Tables)
        {
            foreach (DataRow row in table.Rows)
            {
                writer.WriteLine($"{row[dataFieldName]},{row[caption]}");
            }
        }
    }
}

