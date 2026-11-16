Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W25 {
  [StructLayout(LayoutKind.Sequential)] public struct INPUT { public uint type; public U u; }
  [StructLayout(LayoutKind.Explicit)] public struct U { [FieldOffset(0)] public K ki; }
  [StructLayout(LayoutKind.Sequential)] public struct K { public ushort vk; public ushort scan; public uint flags; public uint time; public IntPtr extra; }
  [DllImport("user32.dll")] public static extern uint SendInput(uint n, INPUT[] p, int cb);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
function Shot($n) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { Write-Output "weg"; return }
  $h = $q.MainWindowHandle
  $r = New-Object W25+RECT; [W25]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  if ($w -le 0) { return }
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [W25]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $bmp.Save("_work\review_fixes\mk_$n.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}
function Key($vk, $scan) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  [W25]::SetForegroundWindow($q.MainWindowHandle) | Out-Null
  $a = New-Object 'W25+INPUT[]' 2
  $a[0].type=1; $a[0].u.ki.vk=$vk; $a[0].u.ki.scan=$scan
  $a[1].type=1; $a[1].u.ki.vk=$vk; $a[1].u.ki.scan=$scan; $a[1].u.ki.flags=2
  [W25]::SendInput(2,$a,[Runtime.InteropServices.Marshal]::SizeOf($a[0])) | Out-Null
}
$keys = @(
  @(0x43,0x2E,'C'), @(0x58,0x2D,'X'), @(0x5A,0x2C,'Z'),
  @(0x41,0x1E,'A'), @(0x53,0x1F,'S'), @(0x44,0x20,'D'),
  @(0x09,0x0F,'TAB'), @(0x31,0x02,'1'), @(0x32,0x03,'2'), @(0x33,0x04,'3')
)
foreach ($k in $keys) {
  Key $k[0] $k[1]
  Start-Sleep -Seconds 2
  Shot $k[2]
}
Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Select-Object Id, MainWindowTitle
