param([string]$In, [int]$X, [int]$Y, [int]$W, [int]$H)
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile((Resolve-Path $In))
$bmp = New-Object System.Drawing.Bitmap($src)
$chars = ' .:-=+*#%@'
for ($y = $Y; $y -lt ($Y + $H); $y++) {
  $line = ''
  for ($x = $X; $x -lt ($X + $W); $x++) {
    $c = $bmp.GetPixel($x, $y)
    $v = [int](($c.R + $c.G + $c.B) / 3)
    $i = [int]([math]::Floor($v / 26))
    if ($i -gt 9) { $i = 9 }
    $line += $chars[$i]
  }
  Write-Output $line
}
$bmp.Dispose(); $src.Dispose()
