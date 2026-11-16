Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W50 {
  [StructLayout(LayoutKind.Sequential)] public struct INPUT { public uint type; public U u; }
  [StructLayout(LayoutKind.Explicit)] public struct U { [FieldOffset(0)] public K ki; }
  [StructLayout(LayoutKind.Sequential)] public struct K { public ushort vk; public ushort scan; public uint flags; public uint time; public IntPtr extra; }
  [DllImport("user32.dll")] public static extern uint SendInput(uint n, INPUT[] p, int cb);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
}
"@
function Key($vk, $scan) {
  $q = Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if (-not $q) { return }
  [W50]::SetForegroundWindow($q.MainWindowHandle) | Out-Null
  $a = New-Object 'W50+INPUT[]' 2
  $a[0].type=1; $a[0].u.ki.vk=$vk; $a[0].u.ki.scan=$scan
  $a[1].type=1; $a[1].u.ki.vk=$vk; $a[1].u.ki.scan=$scan; $a[1].u.ki.flags=2
  [W50]::SendInput(2,$a,[Runtime.InteropServices.Marshal]::SizeOf($a[0])) | Out-Null
}
Get-Process -Name pds-recompile -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
Start-Process -FilePath "pds-recompile.exe" -WorkingDirectory "_build\pds-recompile-de" | Out-Null
Start-Sleep -Seconds 380
Key 0x0D 0x1C
Start-Sleep -Seconds 6
C:\Users\FreakItOut\AppData\Local\Programs\Python\Python312\python.exe _tools\watch_subtitles2.py
