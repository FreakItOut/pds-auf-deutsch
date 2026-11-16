# Screenshot der EXE-GUI (PrintWindow) nach Titel.
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public class Q {
  [DllImport("user32.dll", CharSet=CharSet.Unicode)]
  public static extern IntPtr FindWindow(string cls, string title);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
$py = Start-Process -FilePath "_dist\PDS_Deutsch_Patcher.exe" -WorkingDirectory (Get-Location) -PassThru
$h = [IntPtr]::Zero
for ($i = 0; $i -lt 30; $i++) {
  Start-Sleep -Seconds 1
  $win = Get-Process -Name PDS_Deutsch_Patcher -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if ($win) { $h = $win.MainWindowHandle; break }
}
if ($h -eq 0) { Write-Output "kein fenster"; Get-Process -Name PDS_Deutsch_Patcher -ErrorAction SilentlyContinue | Stop-Process -Force; exit 1 }
$r = New-Object Q+RECT
[Q]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.R - $r.L; $ht = $r.B - $r.T
$bmp = New-Object System.Drawing.Bitmap($w, $ht)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$dc = $g.GetHdc()
[Q]::PrintWindow($h, $dc, 2) | Out-Null
$g.ReleaseHdc($dc); $g.Dispose()
$bmp.Save("_work\review_fixes\exe_screenshot.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
Stop-Process -Name PDS_Deutsch_Patcher -Force -ErrorAction SilentlyContinue
Write-Output "screenshot ok ${w}x${ht}"
