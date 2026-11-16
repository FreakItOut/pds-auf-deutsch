param([string]$TitleLike = "Panzer Dragoon Saga", [string]$Out = "_work\review_fixes\gui.png")
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WSHOT {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowTextW(IntPtr h, System.Text.StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lp);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  public delegate bool EnumProc(IntPtr h, IntPtr lp);
  public struct RECT { public int L, T, R, B; }
}
"@
$found = [IntPtr]::Zero
$cb = [WSHOT+EnumProc]{
  param($h, $lp)
  if ([WSHOT]::IsWindowVisible($h)) {
    $sb = New-Object System.Text.StringBuilder 512
    [WSHOT]::GetWindowTextW($h, $sb, 512) | Out-Null
    if ($sb.ToString() -like "*$TitleLike*") { $script:found = $h }
  }
  return $true
}
[WSHOT]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null
if ($found -eq [IntPtr]::Zero) { Write-Output "window not found"; exit 1 }
$r = New-Object WSHOT+RECT; [WSHOT]::GetWindowRect($found, [ref]$r) | Out-Null
$w = $r.R-$r.L; $ht = $r.B-$r.T
$bmp = New-Object System.Drawing.Bitmap($w,$ht)
$g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
[WSHOT]::PrintWindow($found,$dc,2) | Out-Null
$g.ReleaseHdc($dc); $g.Dispose()
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
Write-Output "ok $Out ${w}x${ht}"
