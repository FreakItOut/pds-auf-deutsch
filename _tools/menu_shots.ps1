param([string]$Label = "menu", [int]$Start = 16, [int]$Step = 4, [int]$Count = 6, [string]$Extra = "")
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class KM {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
function Shot($n) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { Write-Output "$n noboot"; return }
  $h = $q.MainWindowHandle
  $r = New-Object KM+RECT; [KM]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  if ($w -le 0) { Write-Output "$n zerorect"; return }
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [KM]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $bmp.Save("_work\review_fixes\km_${Label}_$n.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}
Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
$args = @()
if ($Extra) { $args = $Extra.Split(' ') }
Start-Process -FilePath "pds-recompile.exe" -WorkingDirectory "_build\pds-recompile-de" -ArgumentList $args
Start-Sleep -Seconds $Start
for ($i = 1; $i -le $Count; $i++) {
  Shot $i
  Start-Sleep -Seconds $Step
}
$p = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Select-Object -First 1
if ($p) { Write-Output "frame $($p.MainWindowTitle)" }
