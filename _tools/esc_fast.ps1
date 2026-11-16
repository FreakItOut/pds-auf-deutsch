Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W22 {
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
  $r = New-Object W22+RECT; [W22]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  if ($w -le 0) { return }
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [W22]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $bmp.Save("_work\review_fixes\st_$n.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}
function Key($vk, $scan) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  [W22]::SetForegroundWindow($q.MainWindowHandle) | Out-Null
  $a = New-Object 'W22+INPUT[]' 2
  $a[0].type=1; $a[0].u.ki.vk=$vk; $a[0].u.ki.scan=$scan
  $a[1].type=1; $a[1].u.ki.vk=$vk; $a[1].u.ki.scan=$scan; $a[1].u.ki.flags=2
  [W22]::SendInput(2,$a,[Runtime.InteropServices.Marshal]::SizeOf($a[0])) | Out-Null
}
Key 0x1B 0x01
Start-Sleep -Milliseconds 400
Shot "esc_a"
Start-Sleep -Milliseconds 800
Shot "esc_b"
