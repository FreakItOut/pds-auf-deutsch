Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32 {
  [StructLayout(LayoutKind.Sequential)] public struct INPUT { public uint type; public U u; }
  [StructLayout(LayoutKind.Explicit)] public struct U { [FieldOffset(0)] public K ki; [FieldOffset(0)] public M mi; }
  [StructLayout(LayoutKind.Sequential)] public struct K { public ushort vk; public ushort scan; public uint flags; public uint time; public IntPtr extra; }
  [StructLayout(LayoutKind.Sequential)] public struct M { public int dx; public int dy; public uint mouseData; public uint dwFlags; public uint time; public IntPtr extra; }
  [DllImport("user32.dll")] public static extern uint SendInput(uint n, INPUT[] p, int cb);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  public struct RECT { public int L, T, R, B; }
}
"@
function Shot($n) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { return }
  $h = $q.MainWindowHandle
  $r = New-Object W32+RECT; [W32]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  if ($w -le 0) { return }
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [W32]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $bmp.Save("_work\review_fixes\fc_$n.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}
function Key($vk, $scan) {
  $a = New-Object 'W32+INPUT[]' 2
  $a[0].type=1; $a[0].u.ki.vk=$vk; $a[0].u.ki.scan=$scan
  $a[1].type=1; $a[1].u.ki.vk=$vk; $a[1].u.ki.scan=$scan; $a[1].u.ki.flags=2
  [W32]::SendInput(2,$a,[Runtime.InteropServices.Marshal]::SizeOf($a[0])) | Out-Null
}
$q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = $q.MainWindowHandle
$r = New-Object W32+RECT; [W32]::GetWindowRect($h, [ref]$r) | Out-Null
# Klick in die Fenstermitte, dann Fokus pruefen
[W32]::SetCursorPos([int](($r.L+$r.R)/2), [int](($r.T+$r.B)/2)) | Out-Null
Start-Sleep -Milliseconds 200
$a = New-Object 'W32+INPUT[]' 2
$a[0].type=0; $a[0].u.mi.dwFlags=0x0002
$a[1].type=0; $a[1].u.mi.dwFlags=0x0004
[W32]::SendInput(2,$a,[Runtime.InteropServices.Marshal]::SizeOf($a[0])) | Out-Null
Start-Sleep -Milliseconds 500
"foreground=$([W32]::GetForegroundWindow()) game=$h"
Key 0x27 0x4D
Start-Sleep -Milliseconds 700
Shot "right1"
Key 0x27 0x4D
Start-Sleep -Milliseconds 700
Shot "right2"
Key 0x28 0x50
Start-Sleep -Milliseconds 700
Shot "down1"
