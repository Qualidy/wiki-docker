Param(
  [string]$Root = "docs/content"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -Path $Root)) {
  Write-Error "Root path not found: $Root"
  exit 1
}

$files = Get-ChildItem -Path $Root -Filter *.ipynb -File -Recurse

foreach ($f in $files) {
  $nbJson = Get-Content -Raw -Path $f.FullName -Encoding UTF8
  $nb = $nbJson | ConvertFrom-Json

  $lang = $null
  if ($nb.metadata -and $nb.metadata.language_info -and $nb.metadata.language_info.name) {
    $lang = $nb.metadata.language_info.name
  }

  $lines = New-Object System.Collections.Generic.List[string]

  foreach ($cell in $nb.cells) {
    if ($cell.cell_type -eq 'markdown') {
      foreach ($line in $cell.source) { [void]$lines.Add($line) }
      [void]$lines.Add("")
    } else {
      if ($cell.cell_type -eq 'code') {
        $langTag = ""
        if ($lang) { $langTag = $lang }
        [void]$lines.Add("```$langTag")
        foreach ($line in $cell.source) { [void]$lines.Add($line) }
        [void]$lines.Add("```")
        [void]$lines.Add("")
      }
    }
  }

  $mdPath = [System.IO.Path]::ChangeExtension($f.FullName, ".md")
  [System.IO.File]::WriteAllLines($mdPath, $lines, [System.Text.Encoding]::UTF8)
  Write-Host "Wrote $mdPath"
}
