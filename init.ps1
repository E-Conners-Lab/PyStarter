$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (Test-Path .env) {
    Write-Output '.env already exists; leaving your settings unchanged.'
    exit 0
}
function New-Secret([int]$Length) {
    $bytes = New-Object byte[] $Length
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
    return [BitConverter]::ToString($bytes).Replace('-', '').ToLowerInvariant()
}
$content = @(
    "DJANGO_SECRET_KEY=$(New-Secret 48)"
    "DB_PASSWORD=$(New-Secret 32)"
    "POSTGRES_ADMIN_PASSWORD=$(New-Secret 32)"
    'NGINX_PORT=8080'
    'ANTHROPIC_API_KEY='
    'ANTHROPIC_MODEL='
    'ANTHROPIC_BASE_URL='
) -join "`n"
$stream = [System.IO.File]::Open((Join-Path $PSScriptRoot '.env'), [System.IO.FileMode]::CreateNew)
try {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($content + "`n")
    $stream.Write($bytes, 0, $bytes.Length)
} finally { $stream.Dispose() }
Write-Output 'Created .env with unique local credentials. Keep this file private.'
Write-Output 'Optional: add AI provider settings. Then: docker compose up --build -d'
