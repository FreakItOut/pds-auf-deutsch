param([string]$In, [string]$Out, [int]$X, [int]$Y, [int]$W, [int]$H, [int]$Scale = 6)
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile((Resolve-Path $In))
$crop = New-Object System.Drawing.Bitmap($W, $H)
$g = [System.Drawing.Graphics]::FromImage($crop)
$g.DrawImage($src, (New-Object System.Drawing.Rectangle(0,0,$W,$H)),
  (New-Object System.Drawing.Rectangle($X,$Y,$W,$H)),
  [System.Drawing.GraphicsUnit]::Pixel)
$g.Dispose(); $src.Dispose()
$big = New-Object System.Drawing.Bitmap(($W*$Scale), ($H*$Scale))
$g2 = [System.Drawing.Graphics]::FromImage($big)
$g2.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g2.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::Half
$g2.DrawImage($crop, 0, 0, ($W*$Scale), ($H*$Scale))
$g2.Dispose(); $crop.Dispose()
$big.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
$big.Dispose()
Write-Output "ok $Out"
