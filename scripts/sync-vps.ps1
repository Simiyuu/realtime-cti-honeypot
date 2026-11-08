param(
    [Parameter(Mandatory=$true)][string]$VpsIp,
    [string]$Key = "$env:USERPROFILE\.ssh\vps-key.key",
    [int]$Port = 22022,
    [int]$Lines = 2000,
    [int]$IntervalSeconds = 60,
    [switch]$Once
)

$Remote = "/home/ubuntu/realtime-cti-honeypot/honeypot/cowrie-logs/cowrie.json"
$Local  = Join-Path $PSScriptRoot "..\data\cowrie.json"
$Tmp    = "$Local.tmp"

do {
    ssh -p $Port -i $Key "ubuntu@$VpsIp" "tail -n $Lines $Remote > /tmp/cowrie-latest.json"
    if ($LASTEXITCODE -eq 0) {
        scp -C -P $Port -i $Key "ubuntu@${VpsIp}:/tmp/cowrie-latest.json" $Tmp
        if ($LASTEXITCODE -eq 0) {
            Move-Item -Force $Tmp $Local
            Write-Host "$(Get-Date -Format HH:mm:ss) synced"
        }
    } else {
        Write-Host "sync failed, will retry"
    }
    if (-not $Once) { Start-Sleep $IntervalSeconds }
} while (-not $Once)
