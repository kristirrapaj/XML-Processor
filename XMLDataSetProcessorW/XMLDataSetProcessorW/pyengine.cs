using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace XMLDataSetProcessorW{
    private static void DoPython(){
        ScriptEngine engine = Python.CreateEngine();
        ScriptScope scope = engine.CreateScope();
        engine.ExecuteFile("./sister-tool-py/processor.py", scope);
    }
}