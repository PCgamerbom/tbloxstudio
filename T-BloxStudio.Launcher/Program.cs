using System.Diagnostics;
using System.Reflection;
using System.Runtime.InteropServices;

try
{
    var studioPath = FindStudioPath();
    InstallPlugin();

    var startInfo = new ProcessStartInfo
    {
        FileName = studioPath,
        WorkingDirectory = Path.GetDirectoryName(studioPath)!,
        UseShellExecute = true,
    };

    foreach (var argument in args)
    {
        startInfo.ArgumentList.Add(argument);
    }

    Process.Start(startInfo);
    return 0;
}
catch (Exception exception)
{
    NativeMethods.ShowError(exception.Message);
    return 1;
}

static string FindStudioPath()
{
    var localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
    var versionsRoot = Path.Combine(localAppData, "Roblox", "Versions");

    if (Directory.Exists(versionsRoot))
    {
        var installedStudio = Directory.EnumerateDirectories(versionsRoot, "version-*")
            .Select(directory => Path.Combine(directory, "RobloxStudioBeta.exe"))
            .Where(File.Exists)
            .OrderByDescending(File.GetLastWriteTimeUtc)
            .FirstOrDefault();

        if (installedStudio is not null)
        {
            return installedStudio;
        }
    }

    var bundledStudio = Path.Combine(AppContext.BaseDirectory, "RobloxStudioBeta.exe");
    if (File.Exists(bundledStudio))
    {
        return bundledStudio;
    }

    throw new FileNotFoundException(
        "Roblox Studio nao foi encontrado. Instale-o pelo site oficial e abra o T-BloxStudio novamente.");
}

static void InstallPlugin()
{
    const string resourceName = "TBloxStudio.plugin.lua";
    using var pluginStream = Assembly.GetExecutingAssembly().GetManifestResourceStream(resourceName)
        ?? throw new InvalidOperationException("O plugin T-BloxStudio nao esta incluido no launcher.");

    var localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
    var pluginDirectory = Path.Combine(localAppData, "Roblox", "Plugins");
    Directory.CreateDirectory(pluginDirectory);

    using var destination = File.Create(Path.Combine(pluginDirectory, "TBloxStudio.lua"));
    pluginStream.CopyTo(destination);
}

static class NativeMethods
{
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int MessageBox(IntPtr window, string text, string caption, uint type);

    public static void ShowError(string message)
    {
        MessageBox(IntPtr.Zero, message, "T-BloxStudio", 0x10);
    }
}