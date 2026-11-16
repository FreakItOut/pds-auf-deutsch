param([int]$Seconds = 180, [string]$Dir = "_work\subwatch6", [int]$Threshold = 60)
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class SW6 {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
if (-not (Test-Path $Dir)) { New-Item -ItemType Directory -Path $Dir | Out-Null }
$sw = [Diagnostics.Stopwatch]::StartNew()
$i = 0; $hits = 0
while ($sw.Elapsed.TotalSeconds -lt $Seconds) {
  $i++
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { Start-Sleep -Milliseconds 500; continue }
  $h = $q.MainWindowHandle
  $r = New-Object SW6+RECT; [SW6]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  if ($w -le 0 -or $ht -le 0) { Start-Sleep -Milliseconds 500; continue }
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [SW6]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $y0 = [int]($ht * 0.855); $y1 = [int]($ht * 0.945)
  $x0 = [int]($w * 0.12); $x1 = [int]($w * 0.88)
  $score = 0
  for ($y = $y0; $y -lt $y1; $y += 2) {
    for ($x = $x0; $x -lt $x1; $x += 2) {
      $c = $bmp.GetPixel($x,$y)
      $v = ($c.R + $c.G + $c.B) / 3
      if ($v -gt 140) { $score++ }
    }
  }
  if ($score -gt $Threshold) {
    $hits++
    $ts = [int]$sw.Elapsed.TotalSeconds
    $bmp.Save("$Dir\hit_$($ts.ToString('000')).jpg", [System.Drawing.Imaging.ImageFormat]::Jpeg)
    Write-Output "hit t=$ts score=$score"
  }
  $bmp.Dispose()
  Start-Sleep -Milliseconds 900
}
Write-Output "fertig hits=$hits"
