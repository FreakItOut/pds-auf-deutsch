param([int]$Seconds = 300, [string]$Dir = "_work\subwatch3")
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class SW3 {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
if (-not (Test-Path $Dir)) { New-Item -ItemType Directory -Path $Dir | Out-Null }
$q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $q) { Write-Output "noboot"; exit }
$h = $q.MainWindowHandle
$r = New-Object SW3+RECT; [SW3]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.R-$r.L; $ht = $r.B-$r.T
Write-Output "win ${w}x${ht}"
$y0 = [int]($ht * 0.840); $y1 = [int]($ht * 0.940)
$x0 = [int]($w * 0.12); $x1 = [int]($w * 0.88)
$sw = [Diagnostics.Stopwatch]::StartNew()
$i = 0; $hits = 0
while ($sw.Elapsed.TotalSeconds -lt $Seconds) {
  $i++
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [SW3]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $score = 0
  for ($y = $y0; $y -lt $y1; $y += 2) {
    for ($x = $x0; $x -lt $x1; $x += 2) {
      $c = $bmp.GetPixel($x,$y)
      if ($c.R -gt 190 -and $c.G -gt 190 -and $c.B -gt 190) { $score++ }
    }
  }
  if ($score -gt 90) {
    $hits++
    $ts = [int]$sw.Elapsed.TotalSeconds
    $bmp.Save("$Dir\hit_$($ts.ToString('000')).jpg", [System.Drawing.Imaging.ImageFormat]::Jpeg)
    Write-Output "hit t=$ts score=$score"
  }
  $bmp.Dispose()
  Start-Sleep -Milliseconds 900
}
Write-Output "fertig hits=$hits"
