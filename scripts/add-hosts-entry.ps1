<#
.SYNOPSIS
    Maps hub.internal.rg to this machine by adding a line to the Windows hosts file.

.DESCRIPTION
    Must be run from an elevated (Administrator) PowerShell window, because the hosts
    file is owned by the system. Safe to run twice: it does nothing if the entry is
    already present, and it backs the file up before writing.

.EXAMPLE
    .\scripts\add-hosts-entry.ps1
#>

[CmdletBinding()]
param(
    [string]$HostName = "hub.internal.rg",
    [string]$IPAddress = "127.0.0.1"
)

$ErrorActionPreference = "Stop"
$hostsFile = "$env:SystemRoot\System32\drivers\etc\hosts"

$isAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "This script needs Administrator rights." -ForegroundColor Yellow
    Write-Host "Right-click Start -> 'Terminal (Admin)' or 'Windows PowerShell (Admin)', then run it again."
    exit 1
}

$existing = Select-String -Path $hostsFile -Pattern "\s$([regex]::Escape($HostName))\s*$" -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Already mapped: $($existing.Line.Trim())" -ForegroundColor Green
    exit 0
}

$backup = "$hostsFile.bak-$(Get-Date -Format yyyyMMdd-HHmmss)"
Copy-Item $hostsFile $backup
Write-Host "Backed up hosts file to $backup"

Add-Content -Path $hostsFile -Value "$IPAddress`t$HostName" -Encoding ASCII
Write-Host "Added: $IPAddress`t$HostName" -ForegroundColor Green

ipconfig /flushdns | Out-Null

$resolved = (Resolve-DnsName $HostName -ErrorAction SilentlyContinue).IPAddress
if ($resolved -contains $IPAddress) {
    Write-Host "$HostName now resolves to $IPAddress. Start the server and open http://$HostName" -ForegroundColor Green
} else {
    Write-Warning "Entry written, but $HostName did not resolve as expected. Check $hostsFile for a conflicting line."
}
