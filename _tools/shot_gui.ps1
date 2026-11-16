# Startet die GUI kurz, macht einen PrintWindow-Screenshot und beendet sie.
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class P {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
$py = "C:\Users\FreakItOut\AppData\Local\Programs\Python\Python312\python.exe"
$p = Start-Process -FilePath $py -ArgumentList "_tools\pds_deutsch_patcher_gui.py" -WorkingDirectory (Get-Location) -PassThru
Start-Sleep -Seconds 6
$proc = Get-Process -Id $p.Id -ErrorAction SilentlyContinue
if (-not $proc) { Write-Output "GUI wurde nicht gestartet"; exit 1 }
$h = $proc.MainWindowHandle
if ($h -eq 0) { Start-Sleep -Seconds 3; $proc.Refresh(); $h = $proc.MainWindowHandle }
[P]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 800
$r = New-Object P+RECT
[P]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.R - $r.L; $ht = $r.B - $r.T
$bmp = New-Object System.Drawing.Bitmap($w, $ht)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$dc = $g.GetHdc()
[P]::PrintWindow($h, $dc, 2) | Out-Null   # 2 = PW_RENDERFULLCONTENT
$g.ReleaseHdc($dc); $g.Dispose()
$bmp.Save("_work\review_fixes\gui_screenshot.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
Stop-Process -Id $p.Id -Force
Write-Output "screenshot ok ${w}x${ht}"
