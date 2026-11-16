Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W6 {
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
Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
Start-Process -FilePath "_work\font_test_build\pds-recompile.exe" -WorkingDirectory "_work\font_test_build" | Out-Null
Start-Sleep -Seconds 14
function Key($vk,$scan) {
  $a = New-Object 'W6+INPUT[]' 2
  $a[0].type=1; $a[0].u.ki.vk=$vk; $a[0].u.ki.scan=$scan; $a[0].u.ki.flags=0
  $a[1].type=1; $a[1].u.ki.vk=$vk; $a[1].u.ki.scan=$scan; $a[1].u.ki.flags=2
  [W6]::SendInput(2,$a,[Runtime.InteropServices.Marshal]::SizeOf($a[0])) | Out-Null
}
function Shot($n) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { return }
  $h = $q.MainWindowHandle
  [W6]::SetForegroundWindow($h) | Out-Null
  $r = New-Object W6+RECT; [W6]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.R-$r.L; $ht = $r.B-$r.T
  $bmp = New-Object System.Drawing.Bitmap($w,$ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
  [W6]::PrintWindow($h,$dc,2) | Out-Null
  $g.ReleaseHdc($dc); $g.Dispose()
  $bmp.Save("_work\review_fixes\w_$n.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}
Shot 0
Key 0x0D 0x1C
for ($i=0; $i -lt 18; $i++) {
  Start-Sleep -Seconds 6
  Shot $i
}
Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Stop-Process -Force
