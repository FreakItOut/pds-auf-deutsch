param([string]$Label = "orig")
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class KW {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
function Shot($n) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { Write-Output "$n noboot"; return }
  $h = $q.MainWindowHandle
  $r = New-Object KW+RECT; [KW]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  if ($w -le 0) { Write-Output "$n zerorect"; return }
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [KW]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $path = "_work\review_fixes\kb_${Label}_$n.png"
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
  # mittlere Helligkeit
  $sum = 0.0; $cnt = 0
  for ($y = 0; $y -lt $ht; $y += 8) {
    for ($x = 0; $x -lt $w; $x += 8) {
      $c = $bmp.GetPixel($x,$y); $sum += ($c.R + $c.G + $c.B) / 3.0; $cnt++
    }
  }
  $bmp.Dispose()
  $m = if ($cnt -gt 0) { [math]::Round($sum / $cnt, 1) } else { -1 }
  Write-Output "$n bright=$m"
}
Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
Start-Process -FilePath "pds-recompile.exe" -WorkingDirectory "_build\pds-recompile-de" | Out-Null
$waits = @(8, 8, 10)
$i = 0
foreach ($w in $waits) {
  Start-Sleep -Seconds $w
  $i++
  Shot ("t$i")
}
$p = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Select-Object -First 1
if ($p) { Write-Output "frame $($p.MainWindowTitle)"; Stop-Process -Id $p.Id -Force }
