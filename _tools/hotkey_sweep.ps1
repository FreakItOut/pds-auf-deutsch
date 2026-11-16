Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W60 {
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
  if (-not $q) { return }
  $h = $q.MainWindowHandle
  $r = New-Object W60+RECT; [W60]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  if ($w -le 0) { return }
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [W60]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $bmp.Save("_work\review_fixes\hk_$n.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}
function Hold($vk, $scan) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { return }
  [W60]::SetForegroundWindow($q.MainWindowHandle) | Out-Null
  $a = New-Object 'W60+INPUT[]' 4
  $a[0].type=1; $a[0].u.ki.vk=$vk; $a[0].u.ki.scan=$scan
  $a[1].type=1; $a[1].u.ki.vk=$vk; $a[1].u.ki.scan=$scan
  $a[2].type=1; $a[2].u.ki.vk=$vk; $a[2].u.ki.scan=$scan
  $a[3].type=1; $a[3].u.ki.vk=$vk; $a[3].u.ki.scan=$scan; $a[3].u.ki.flags=2
  [W60]::SendInput(4,$a,[Runtime.InteropServices.Marshal]::SizeOf($a[0])) | Out-Null
}
$keys = @(
  @(0x70,0x3B,'F1'), @(0x71,0x3C,'F2'), @(0x72,0x3D,'F3'), @(0x73,0x3E,'F4'),
  @(0x74,0x3F,'F5'), @(0x75,0x40,'F6'), @(0x76,0x41,'F7'), @(0x77,0x42,'F8'),
  @(0x78,0x43,'F9'), @(0x79,0x44,'F10'), @(0x7A,0x57,'F11'), @(0x7B,0x58,'F12')
)
foreach ($k in $keys) {
  Shot ("$($k[2])_pre")
  Hold $k[0] $k[1]
  Start-Sleep -Milliseconds 600
  Shot "$($k[2])"
}
