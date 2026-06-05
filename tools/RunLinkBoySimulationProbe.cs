using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Windows.Forms;

internal static class RunLinkBoySimulationProbe
{
    private static string _baseDir = @"D:\linkboy\linkboy";
    private static string _labPath = @"D:\linkboy\work\port_sort.lab";
    private static string _workDir = @"D:\linkboy\work";
    private static string _configPath = @"D:\linkboy\work\simulation_probe_config.txt";
    private static string _mode = "simu";
    private static StreamWriter _log;
    private static int _tickCount;
    private static int _maxSeconds = 32;
    private static bool _clicked;
    private static bool _simRunClicked;
    private static bool _simFormSeen;
    private static bool _mainFormSeen;
    private static bool _normalExit;
    private static int _exitCode;
    private static bool _consoleAvailable = true;
    private static readonly HashSet<string> FailureReasons = new HashSet<string>();

    [STAThread]
    private static int Main(string[] args)
    {
        TrySetConsoleOutputEncoding();
        if (args.Length > 0) _labPath = Path.GetFullPath(args[0]);
        var envMode = Environment.GetEnvironmentVariable("LINKBOY_PROBE_MODE");
        var envSeconds = Environment.GetEnvironmentVariable("LINKBOY_PROBE_SECONDS");
        var config = ReadConfig();
        if (args.Length > 1) _mode = args[1].Trim().ToLowerInvariant();
        else if (!string.IsNullOrWhiteSpace(envMode)) _mode = envMode.Trim().ToLowerInvariant();
        else if (config.ContainsKey("mode")) _mode = config["mode"].Trim().ToLowerInvariant();
        if (args.Length > 2 && !int.TryParse(args[2], out _maxSeconds)) _maxSeconds = 32;
        else if (args.Length <= 2 && !string.IsNullOrWhiteSpace(envSeconds) && !int.TryParse(envSeconds, out _maxSeconds)) _maxSeconds = 32;
        else if (args.Length <= 2 && string.IsNullOrWhiteSpace(envSeconds) && config.ContainsKey("seconds") && !int.TryParse(config["seconds"], out _maxSeconds)) _maxSeconds = 32;
        if (_maxSeconds < 20) _maxSeconds = 20;

        Environment.SetEnvironmentVariable("LINKBOY_PROBE_MODE", _mode);
        Environment.SetEnvironmentVariable("LINKBOY_PROBE_SECONDS", _maxSeconds.ToString());
        WriteConfig();

        Directory.SetCurrentDirectory(_baseDir);
        AppDomain.CurrentDomain.AssemblyResolve += ResolveLocalAssembly;
        Application.ThreadException += (sender, eventArgs) => HandleThreadException(eventArgs.Exception);
        AppDomain.CurrentDomain.UnhandledException += (sender, eventArgs) => LogException("UNHANDLED_EXCEPTION", eventArgs.ExceptionObject as Exception);

        Directory.CreateDirectory(_workDir);
        var logPath = Path.Combine(_workDir, "simulation_probe_" + _mode + ".log");
        using (_log = new StreamWriter(logPath, false, new UTF8Encoding(false)))
        {
            try
            {
                Log("START " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
                Log("BASE=" + _baseDir);
                Log("LAB=" + _labPath);
                Log("MODE=" + _mode);
                Log("MAX_SECONDS=" + _maxSeconds);
                Log("Application.StartupPath=" + Application.StartupPath);

                var linkboyAssembly = Assembly.LoadFrom(Path.Combine(_baseDir, "linkboy.exe"));
                var uType = linkboyAssembly.GetType("U.U", true);
                var main = uType.GetMethod("Main", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static);
                if (main == null)
                {
                    Fail("NO_U_U_MAIN");
                    return 2;
                }

                var timer = new System.Windows.Forms.Timer { Interval = 1000 };
                timer.Tick += ProbeTick;
                timer.Start();

                Log("CALL U.U.Main");
                main.Invoke(null, new object[] { new[] { _labPath } });
                Log("U.U.Main returned");

                if (!_normalExit && _tickCount == 0)
                {
                    Log("WAITING_FOR_NESTED_PROBE");
                    if (_log != null)
                    {
                        _log.Flush();
                        _log.Dispose();
                        _log = null;
                    }
                    return WaitForNestedProbe(logPath, _maxSeconds + 90);
                }

                if (!_normalExit)
                {
                    Fail("MAIN_RETURNED_BEFORE_REQUESTED_DURATION");
                }

                return _exitCode == 0 ? 1 : _exitCode;
            }
            catch (TargetInvocationException ex)
            {
                LogException("FATAL_TARGET", ex.InnerException ?? ex);
                return 1;
            }
            catch (Exception ex)
            {
                LogException("FATAL", ex);
                return 1;
            }
            finally
            {
                Log("END " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
                if (_log != null) _log.Flush();
            }
        }
    }

    private static int WaitForNestedProbe(string logPath, int timeoutSeconds)
    {
        var deadline = DateTime.Now.AddSeconds(timeoutSeconds);
        var lastLength = -1L;
        while (DateTime.Now < deadline)
        {
            try
            {
                if (File.Exists(logPath))
                {
                    var info = new FileInfo(logPath);
                    if (info.Length != lastLength)
                    {
                        lastLength = info.Length;
                        var text = File.ReadAllText(logPath, new UTF8Encoding(false));
                        if (text.IndexOf("EXITING_OK", StringComparison.Ordinal) >= 0) return 0;
                        if (text.IndexOf("EXITING_FAIL", StringComparison.Ordinal) >= 0) return 8;
                        if (text.IndexOf("THREAD_EXCEPTION", StringComparison.Ordinal) >= 0) return 8;
                        if (text.IndexOf("UNHANDLED_EXCEPTION", StringComparison.Ordinal) >= 0) return 8;
                        if (text.IndexOf("FATAL", StringComparison.Ordinal) >= 0) return 8;
                    }
                }
            }
            catch
            {
                // The nested process may be replacing the log file; retry until timeout.
            }
            System.Threading.Thread.Sleep(1000);
        }
        WriteConsoleLine("NESTED_PROBE_TIMEOUT " + timeoutSeconds);
        return 8;
    }

    private static Dictionary<string, string> ReadConfig()
    {
        var result = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        try
        {
            if (!File.Exists(_configPath)) return result;
            foreach (var line in File.ReadAllLines(_configPath, new UTF8Encoding(false)))
            {
                var index = line.IndexOf('=');
                if (index <= 0) continue;
                result[line.Substring(0, index).Trim()] = line.Substring(index + 1).Trim();
            }
        }
        catch
        {
            // Missing or locked config is not fatal; defaults keep the probe usable.
        }
        return result;
    }

    private static void WriteConfig()
    {
        try
        {
            Directory.CreateDirectory(_workDir);
            File.WriteAllLines(
                _configPath,
                new[]
                {
                    "mode=" + _mode,
                    "seconds=" + _maxSeconds,
                    "lab=" + _labPath,
                    "updated=" + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
                },
                new UTF8Encoding(false));
        }
        catch (Exception ex)
        {
            WriteConsoleLine("CONFIG_WRITE_ERROR " + ex.GetType().FullName + " " + ex.Message);
        }
    }

    private static void ProbeTick(object sender, EventArgs e)
    {
        _tickCount++;
        var forms = Application.OpenForms.Cast<Form>().ToList();
        Log("TICK=" + _tickCount + " forms=" + forms.Count);

        var mainFormCurrent = false;
        var simFormCurrent = false;
        foreach (var form in forms)
        {
            var typeName = form.GetType().FullName;
            Log("FORM " + typeName + " title=[" + form.Text + "] visible=" + form.Visible + " disposed=" + form.IsDisposed);
            if (typeName == "v_GForm.GForm")
            {
                _mainFormSeen = true;
                mainFormCurrent = true;
            }
            if (typeName == "n_SimForm.SimForm")
            {
                _simFormSeen = true;
                simFormCurrent = true;
            }
        }

        if (_tickCount == 8)
        {
            CaptureScreen("simulation_probe_" + _mode + "_before.png");
        }

        if (!_clicked && _tickCount >= 10)
        {
            _clicked = true;
            InvokeSimulationButton();
            CaptureScreen("simulation_probe_" + _mode + "_after_invoke.png");
        }

        if (_clicked && !_simRunClicked && _tickCount >= 14)
        {
            InvokeSimFormRun();
            CaptureScreen("simulation_probe_" + _mode + "_after_run.png");
        }

        if (_tickCount == 20 && !_simFormSeen)
        {
            Fail("SIM_FORM_NOT_SEEN");
        }

        if (_tickCount == 24 && !_simRunClicked)
        {
            Fail("SIM_RUN_NOT_INVOKED");
        }

        if (_tickCount == 26 && !_mainFormSeen)
        {
            Fail("MAIN_FORM_NOT_SEEN");
        }

        if (_tickCount > 26 && _simFormSeen && !simFormCurrent)
        {
            Fail("SIM_FORM_DISAPPEARED");
        }

        if (_tickCount > 26 && _mainFormSeen && !mainFormCurrent)
        {
            Fail("MAIN_FORM_DISAPPEARED");
        }

        if (_tickCount > 0 && _tickCount % 300 == 0)
        {
            CaptureScreen("simulation_probe_" + _mode + "_tick_" + _tickCount + ".png");
        }

        if (_tickCount >= _maxSeconds)
        {
            CaptureScreen("simulation_probe_" + _mode + "_after_wait.png");
            if (!_simFormSeen) Fail("SIM_FORM_MISSING_AT_END");
            if (!_simRunClicked) Fail("RUN_NOT_CLICKED_AT_END");
            if (!_mainFormSeen) Fail("MAIN_FORM_MISSING_AT_END");

            _normalExit = true;
            Log(FailureReasons.Count == 0 ? "EXITING_OK" : "EXITING_FAIL code=" + _exitCode);
            if (_log != null) _log.Flush();
            Environment.Exit(FailureReasons.Count == 0 ? 0 : _exitCode);
        }
    }

    private static void InvokeSimulationButton()
    {
        try
        {
            var form = Application.OpenForms.Cast<Form>().FirstOrDefault(f => f.GetType().FullName == "v_GForm.GForm");
            if (form == null)
            {
                Fail("NO_GFORM_FOR_SIM_BUTTON");
                return;
            }

            Log("GFORM_TITLE=" + form.Text);
            TryCallGetSimStatus(form, "before");

            var gFilePanel = GetFieldValue(form, "myGFilePanel");
            Log("myGFilePanel=" + Describe(gFilePanel));
            var gPanel = GetFieldValue(gFilePanel, "GPanel");
            Log("GPanel=" + Describe(gPanel));
            var gHead = GetFieldValue(gPanel, "GHead");
            Log("GHead=" + Describe(gHead));
            if (gHead == null)
            {
                Fail("NO_GHEAD");
                return;
            }

            var methodName = _mode == "sim" ? "SimButton_MouseDownEvent" : "SimuButton_MouseDownEvent";
            var method = gHead.GetType().GetMethod(methodName, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            if (method == null)
            {
                Fail("NO_METHOD_" + methodName);
                return;
            }

            Log("INVOKE " + methodName);
            method.Invoke(gHead, null);
            Log("INVOKED " + methodName);
            TryCallGetSimStatus(form, "after");
        }
        catch (TargetInvocationException ex)
        {
            LogException("INVOKE_TARGET", ex.InnerException ?? ex);
        }
        catch (Exception ex)
        {
            LogException("INVOKE_ERROR", ex);
        }
    }

    private static void InvokeSimFormRun()
    {
        try
        {
            _simRunClicked = true;
            var simForm = Application.OpenForms.Cast<Form>().FirstOrDefault(f => f.GetType().FullName == "n_SimForm.SimForm");
            if (simForm == null)
            {
                _simRunClicked = false;
                Fail("NO_SIM_FORM_FOR_RUN");
                return;
            }

            Log("SIM_FORM_TITLE=" + simForm.Text);
            Log("INVOKE_SIM_FORM_RUN");

            var runMethod = simForm.GetType().GetMethod("ButtonRunClick", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            if (runMethod != null)
            {
                runMethod.Invoke(simForm, new object[] { null, EventArgs.Empty });
                Log("INVOKED ButtonRunClick");
                return;
            }

            var startMethod = simForm.GetType().GetMethod("SimStart", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            if (startMethod != null)
            {
                startMethod.Invoke(simForm, null);
                Log("INVOKED SimStart");
                return;
            }

            _simRunClicked = false;
            Fail("NO_SIM_RUN_METHOD");
        }
        catch (TargetInvocationException ex)
        {
            _simRunClicked = false;
            LogException("SIM_RUN_TARGET", ex.InnerException ?? ex);
        }
        catch (Exception ex)
        {
            _simRunClicked = false;
            LogException("SIM_RUN_ERROR", ex);
        }
    }

    private static void TryCallGetSimStatus(Form form, string label)
    {
        try
        {
            var method = form.GetType().GetMethod("GetSimStatus", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            if (method != null)
            {
                Log("SIM_STATUS_" + label + "=" + method.Invoke(form, null));
            }
        }
        catch (Exception ex)
        {
            Log("SIM_STATUS_" + label + "_ERROR=" + ex.GetType().FullName + " " + ex.Message);
        }
    }

    private static object GetFieldValue(object instance, string fieldName)
    {
        if (instance == null) return null;
        var field = instance.GetType().GetField(fieldName, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static);
        return field == null ? null : field.GetValue(instance);
    }

    private static string Describe(object value)
    {
        if (value == null) return "<null>";
        return value.GetType().FullName;
    }

    private static void CaptureScreen(string fileName)
    {
        try
        {
            var forms = Application.OpenForms
                .Cast<Form>()
                .Where(IsScreenshotTargetForm)
                .Where(form => form.Visible && !form.IsDisposed && form.Width > 0 && form.Height > 0)
                .ToList();

            if (forms.Count == 0)
            {
                Log("WINDOW_SCREEN_SKIPPED no target forms for " + fileName);
                return;
            }

            foreach (var form in forms)
            {
                var size = form.ClientSize;
                if (size.Width <= 0 || size.Height <= 0)
                {
                    size = form.Size;
                }
                if (size.Width <= 0 || size.Height <= 0)
                {
                    Log("WINDOW_SCREEN_SKIPPED empty form " + form.GetType().FullName + " for " + fileName);
                    continue;
                }

                using (var bitmap = new Bitmap(size.Width, size.Height))
                {
                    form.DrawToBitmap(bitmap, new Rectangle(Point.Empty, size));
                    var path = Path.Combine(_workDir, BuildWindowScreenshotName(fileName, form));
                    bitmap.Save(path, ImageFormat.Png);
                    Log("WINDOW_SCREEN=" + path + " type=" + form.GetType().FullName + " title=[" + form.Text + "] size=" + size.Width + "x" + size.Height);
                }
            }
        }
        catch (Exception ex)
        {
            LogException("WINDOW_SCREEN_ERROR", ex);
        }
    }

    private static bool IsScreenshotTargetForm(Form form)
    {
        var typeName = form.GetType().FullName;
        return typeName == "v_GForm.GForm" || typeName == "n_SimForm.SimForm";
    }

    private static string BuildWindowScreenshotName(string fileName, Form form)
    {
        var extension = Path.GetExtension(fileName);
        if (string.IsNullOrEmpty(extension)) extension = ".png";
        var stem = Path.GetFileNameWithoutExtension(fileName);
        var suffix = form.GetType().FullName == "n_SimForm.SimForm" ? "simform" : "gform";
        return stem + "_" + suffix + extension;
    }

    private static void LogException(string prefix, Exception ex)
    {
        if (ex == null)
        {
            Fail(prefix + "_NULL");
            return;
        }

        Log(prefix + " " + ex.GetType().FullName + " " + ex.Message);
        Log(ex.StackTrace ?? "<no stack>");
        Fail(prefix);
        if (ex.InnerException != null)
        {
            LogException(prefix + "_INNER", ex.InnerException);
        }
    }

    private static void HandleThreadException(Exception ex)
    {
        if (IsPostExitPaintException(ex))
        {
            Log("IGNORED_POST_EXIT_PAINT " + ex.GetType().FullName + " " + ex.Message);
            Log(ex.StackTrace ?? "<no stack>");
            return;
        }

        LogException("THREAD_EXCEPTION", ex);
    }

    private static bool IsPostExitPaintException(Exception ex)
    {
        if (!_normalExit || ex == null) return false;
        if (!(ex is ArgumentException) && !(ex is NullReferenceException)) return false;
        var stack = ex.StackTrace ?? "";
        return (stack.IndexOf("System.Drawing.Graphics.Restore", StringComparison.Ordinal) >= 0
                || stack.IndexOf("System.Drawing.BufferedGraphics.Render", StringComparison.Ordinal) >= 0)
            && stack.IndexOf("System.Windows.Forms.Control.WmPaint", StringComparison.Ordinal) >= 0;
    }

    private static void Fail(string reason)
    {
        if (!FailureReasons.Add(reason)) return;
        if (_exitCode == 0) _exitCode = 8;
        Log("FAIL " + reason);
    }

    private static void Log(string line)
    {
        WriteConsoleLine(line);
        if (_log != null)
        {
            _log.WriteLine(line);
            _log.Flush();
        }
    }

    private static void WriteConsoleLine(string line)
    {
        if (!_consoleAvailable) return;
        try
        {
            Console.WriteLine(line);
        }
        catch
        {
            _consoleAvailable = false;
        }
    }

    private static void TrySetConsoleOutputEncoding()
    {
        try
        {
            Console.OutputEncoding = Encoding.UTF8;
        }
        catch
        {
            _consoleAvailable = false;
        }
    }

    private static Assembly ResolveLocalAssembly(object sender, ResolveEventArgs args)
    {
        var simple = new AssemblyName(args.Name).Name;
        foreach (var ext in new[] { ".dll", ".exe" })
        {
            var candidate = Path.Combine(_baseDir, simple + ext);
            if (File.Exists(candidate))
            {
                return Assembly.LoadFrom(candidate);
            }
        }

        return null;
    }
}
