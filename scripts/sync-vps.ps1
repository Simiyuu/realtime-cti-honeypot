param(
    [Parameter(Mandatory=$true)][string]$VpsIp,
    [string]$Key = "$env:USERPROFILE\.ssh\vps-key.key",
    [int]$Port = 22022,
    [int]$Lines = 2000,
    [int]$IntervalSeconds = 60,
    [int]$SshTimeoutSec = 60,
    [int]$ScpTimeoutSec = 120,
    [switch]$Once
)

if (-not ('ConsoleMode' -as [type])) {
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class ConsoleMode {
    [DllImport("kernel32.dll")] public static extern IntPtr GetStdHandle(int n);
    [DllImport("kernel32.dll")] public static extern bool GetConsoleMode(IntPtr h, out uint m);
    [DllImport("kernel32.dll")] public static extern bool SetConsoleMode(IntPtr h, uint m);
    public static bool DisableQuickEdit() {
        IntPtr h = GetStdHandle(-10);
        uint m;
        if (!GetConsoleMode(h, out m)) return false;
        m &= ~0x0040u;
        m |= 0x0080u;
        return SetConsoleMode(h, m);
    }
}
"@
}
try {
    if ([ConsoleMode]::DisableQuickEdit()) { Write-Host "QuickEdit disabled" }
    else { Write-Host "Could not disable QuickEdit (timeouts still protect the loop)" }
} catch { Write-Host "QuickEdit step skipped: $_" }

$Remote  = "/home/ubuntu/realtime-cti-honeypot/honeypot/cowrie-logs/cowrie.json"
$Local   = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\data\cowrie.json"))
$Tmp     = "$Local.tmp"
$LogFile = Join-Path (Split-Path $Local) "sync.log"

function Log($msg) {
    $line = "$(Get-Date -Format 'HH:mm:ss') $msg"
    Write-Host $line
    try { Add-Content -Path $LogFile -Value $line } catch {}
}

function Invoke-Timed($exe, $argString, $timeoutSec) {
    $p = Start-Process -FilePath $exe -ArgumentList $argString -NoNewWindow -PassThru
    $null = $p.Handle
    if (-not $p.WaitForExit($timeoutSec * 1000)) {
        try { $p.Kill() } catch {}
        return -999
    }
    return $p.ExitCode
}

$common = "-o BatchMode=yes -o ConnectTimeout=10 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -i `"$Key`""

do {
    try {
        $sshArgs = "$common -p $Port ubuntu@$VpsIp `"tail -n $Lines $Remote > /tmp/cowrie-latest.json`""
        $c1 = Invoke-Timed "ssh" $sshArgs $SshTimeoutSec
        if ($c1 -eq 0) {
            if (Test-Path $Tmp) { Remove-Item $Tmp -Force }
            $scpArgs = "-C $common -P $Port ubuntu@${VpsIp}:/tmp/cowrie-latest.json `"$Tmp`""
            $c2 = Invoke-Timed "scp" $scpArgs $ScpTimeoutSec
            if ($c2 -eq 0 -and (Test-Path $Tmp)) {
                Move-Item -Force $Tmp $Local
                $kb = [math]::Round((Get-Item $Local).Length / 1KB)
                Log "synced ($kb KB)"
            }
            elseif ($c2 -eq -999) { Log "scp timed out after $ScpTimeoutSec s, killed" }
            else { Log "scp failed (code $c2)" }
        }
        elseif ($c1 -eq -999) { Log "ssh timed out after $SshTimeoutSec s, killed" }
        else { Log "ssh failed (code $c1)" }
    } catch {
        Log "error: $_"
    }
    if (-not $Once) { Start-Sleep $IntervalSeconds }
} while (-not $Once)
