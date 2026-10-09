# Deploy the indicator to the MT5 data folder (safe: never overwrites without backup).
# استقرار اندیکاتور در پوشه‌ی متاتریدر (با بکاپ‌گیری، بدون بازنویسی کور).
param(
    [string]$RepoRoot = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)),
    [string]$IndicatorsDir = "C:\Users\BazikadeStore\AppData\Roaming\MetaQuotes\Terminal\AF19ECCF568F855DF9D3196BBF8BF315\MQL5\Indicators"
)
$ErrorActionPreference = "Stop"
$src = Join-Path $RepoRoot "MQL5\Indicators\Dec3ptionTradingStrategy.mq5"
if (-not (Test-Path -LiteralPath $src)) { throw "Source not found: $src" }
if (-not (Test-Path -LiteralPath $IndicatorsDir)) { throw "Indicators dir not found: $IndicatorsDir" }
$dst = Join-Path $IndicatorsDir "Dec3ptionTradingStrategy.mq5"
if (Test-Path -LiteralPath $dst) {
    $bak = "$dst.bak_" + (Get-Date -Format "yyyyMMdd_HHmmss")
    Copy-Item -LiteralPath $dst -Destination $bak
    Write-Output "Backup: $bak"
}
Copy-Item -LiteralPath $src -Destination $dst
Write-Output "Deployed: $dst"
Write-Output "Next: open MetaEditor (C:\Program Files\Alpari MT5_2\metaeditor64.exe), compile, then drag onto a chart."
