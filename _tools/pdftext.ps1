# Extract readable text from a PDF by decompressing FlateDecode streams
# Usage: powershell -File _tools\pdftext.ps1 "path.pdf"
param([string]$Path)

$data = [System.IO.File]::ReadAllBytes($Path)
$ascii = [System.Text.Encoding]::ASCII.GetString($data)
$results = New-Object System.Collections.Generic.List[string]
$idx = 0
while ($true) {
  $start = $ascii.IndexOf('stream', $idx)
  if ($start -lt 0) { break }
  $end = $ascii.IndexOf('endstream', $start)
  if ($end -lt 0) { break }
  $bodyStart = $start + 7
  if ($ascii[$bodyStart] -eq "`r") { $bodyStart += 2 } elseif ($ascii[$bodyStart] -eq "`n") { $bodyStart += 1 }
  $len = $end - $bodyStart
  if ($len -gt 10) {
    $body = New-Object byte[] $len
    [Array]::Copy($data, $bodyStart, $body, 0, $len)
    try {
      $msIn = New-Object System.IO.MemoryStream(,$body)
      $defl = New-Object System.IO.MemoryStream
      $ds = New-Object System.IO.Compression.DeflateStream($msIn, [System.IO.Compression.CompressionMode]::Decompress)
      $ds.CopyTo($defl); $ds.Dispose()
      $raw = [System.Text.Encoding]::GetEncoding(28591).GetString($defl.ToArray())
      $results.Add($raw)
    } catch {}
  }
  $idx = $end + 9
}
$results -join "`n=====NEXT STREAM=====`n" | Out-String -Width 200
