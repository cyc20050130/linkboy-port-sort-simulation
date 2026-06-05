param(
  [string]$OutputDir = "D:\linkboy\work",
  [string]$NamePrefix = "linkboy_window"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

$signature = @"
using System;
using System.Text;
using System.Runtime.InteropServices;

public static class Win32Capture {
  public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

  [DllImport("user32.dll")]
  public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

  [DllImport("user32.dll")]
  public static extern bool IsWindowVisible(IntPtr hWnd);

  [DllImport("user32.dll")]
  public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

  [DllImport("user32.dll")]
  public static extern int GetWindowTextLength(IntPtr hWnd);

  [DllImport("user32.dll")]
  public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);

  [DllImport("user32.dll")]
  public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);

  [DllImport("user32.dll")]
  public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdcBlt, uint nFlags);

  [DllImport("user32.dll")]
  public static extern bool SetForegroundWindow(IntPtr hWnd);

  public struct RECT {
    public int Left;
    public int Top;
    public int Right;
    public int Bottom;
  }
}
"@

Add-Type $signature

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$targets = @()
[Win32Capture]::EnumWindows({
  param([IntPtr]$hWnd, [IntPtr]$lParam)
  if (-not [Win32Capture]::IsWindowVisible($hWnd)) { return $true }
  $len = [Win32Capture]::GetWindowTextLength($hWnd)
  if ($len -le 0) { return $true }
  $sb = New-Object System.Text.StringBuilder ($len + 1)
  [void][Win32Capture]::GetWindowText($hWnd, $sb, $sb.Capacity)
  $title = $sb.ToString()
  $pidValue = [uint32]0
  [void][Win32Capture]::GetWindowThreadProcessId($hWnd, [ref]$pidValue)
  $proc = Get-Process -Id $pidValue -ErrorAction SilentlyContinue
  if ($null -eq $proc) { return $true }
  if ($proc.ProcessName -in @("RunLinkBoySimulationProbe", "linkboy") -or $title -like "*linkboy*" -or $title -like "*环境模拟机*") {
    $targets += [pscustomobject]@{
      HWnd = $hWnd
      Pid = $pidValue
      ProcessName = $proc.ProcessName
      Title = $title
    }
  }
  return $true
}, [IntPtr]::Zero) | Out-Null

$index = 0
foreach ($target in $targets) {
  $rect = New-Object Win32Capture+RECT
  if (-not [Win32Capture]::GetWindowRect($target.HWnd, [ref]$rect)) { continue }
  $width = $rect.Right - $rect.Left
  $height = $rect.Bottom - $rect.Top
  if ($width -le 0 -or $height -le 0) { continue }

  $safeTitle = ($target.Title -replace '[^\w\-.]+', '_').Trim('_')
  if ($safeTitle.Length -gt 80) { $safeTitle = $safeTitle.Substring(0, 80) }
  if (-not $safeTitle) { $safeTitle = "untitled" }
  $path = Join-Path $OutputDir ("{0}_{1}_{2}_{3}.png" -f $NamePrefix, $index, $target.ProcessName, $safeTitle)

  $bitmap = New-Object System.Drawing.Bitmap $width, $height
  $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
  try {
    $hdc = $graphics.GetHdc()
    try {
      $ok = [Win32Capture]::PrintWindow($target.HWnd, $hdc, 0)
    } finally {
      $graphics.ReleaseHdc($hdc)
    }
    if (-not $ok) {
      [void][Win32Capture]::SetForegroundWindow($target.HWnd)
      Start-Sleep -Milliseconds 200
      $graphics.CopyFromScreen($rect.Left, $rect.Top, 0, 0, (New-Object System.Drawing.Size $width, $height))
    }
    $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    [pscustomobject]@{
      Path = $path
      Width = $width
      Height = $height
      Pid = $target.Pid
      ProcessName = $target.ProcessName
      Title = $target.Title
    }
  } finally {
    $graphics.Dispose()
    $bitmap.Dispose()
  }
  $index += 1
}
