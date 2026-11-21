param(
    [Parameter(Mandatory=$true)][string]$VpsIp,
    [int]$Interval = 30
)

$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Venv = Join-Path (Split-Path $Repo -Parent) ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $Venv)) { Write-Host "Venv not found at $Venv"; exit 1 }

docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker is not running. Start Docker Desktop and wait for Engine running."
    exit 1
}

Push-Location $Repo
docker compose -f docker-compose.db.yml up -d
Pop-Location

Write-Host "Waiting for MySQL..."
$ready = $false
foreach ($i in 1..30) {
    docker exec honeypot-mysql mysqladmin ping --silent *> $null
    if ($LASTEXITCODE -eq 0) { $ready = $true; break }
    Start-Sleep 2
}
if (-not $ready) { Write-Host "MySQL did not become ready."; exit 1 }
Write-Host "MySQL ready."

function Start-Win($title, $cmd) {
    $full = "`$Host.UI.RawUI.WindowTitle='$title'; Set-Location '$Repo'; . '$Venv'; $cmd"
    Start-Process powershell -ArgumentList "-ExecutionPolicy","RemoteSigned","-NoExit","-Command",$full
}

Start-Win "sync"      ".\scripts\sync-vps.ps1 -VpsIp $VpsIp -IntervalSeconds $Interval"
Start-Win "ingest"    "py backend/ingest.py --loop $Interval"
Start-Win "flask"     "py backend/main.py"
Start-Win "dashboard" "Set-Location dashboard; npm start"

Write-Host "Started: sync, ingest, flask, dashboard. Close each window to stop it."
