param([int]$Count = 60, [double]$Interval = 1.0, [string]$Dir = "_work\subwatch2")
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class SW2 {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
if (-not (Test-Path $Dir)) { New-Item -ItemType Directory -Path $Dir | Out-Null }
function Shot($n) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { Write-Output "$n noboot"; return }
  $h = $q.MainWindowHandle
  $r = New-Object SW2+RECT; [SW2]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  if ($w -le 0) { Write-Output "$n zerorect"; return }
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [SW2]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  # Untertitelband: unterer schwarzer Bereich (Bild endet bei 16:9 im Fenster)
  $y0 = [int]($ht * 0.845); $y1 = [int]($ht * 0.935)
  $x0 = [int]($w * 0.15); $x1 = [int]($w * 0.85)
  $score = 0
  for ($y = $y0; $y -lt $y1; $y += 2) {
    for ($x = $x0; $x -lt $x1; $x += 2) {
      $c = $bmp.GetPixel($x,$y)
      if ($c.R -gt 190 -and $c.G -gt 190 -and $c.B -gt 190) { $score++ }
    }
  }
  $fc = $n.ToString("0000")
  $bmp.Save("$Dir\h$fc.jpg", [System.Drawing.Imaging.ImageFormat]::Jpeg)
  $bmp.Dispose()
  Write-Output "$fc score=$score"
}
for ($i = 1; $i -le $Count; $i++) {
  Shot $i
  Start-Sleep -Milliseconds ([int]($Interval * 1000))
}
$p = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Select-Object -First 1
if ($p) { Write-Output "frame $($p.MainWindowTitle)" }
