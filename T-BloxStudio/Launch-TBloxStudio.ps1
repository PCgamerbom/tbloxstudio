$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$bundledStudio = Join-Path $projectRoot "RobloxStudioBeta.exe"
$versionsRoot = Join-Path $env:LOCALAPPDATA "Roblox\Versions"
$studioPath = $null

if (Test-Path -LiteralPath $versionsRoot) {
    $studioPath = Get-ChildItem -LiteralPath $versionsRoot -Directory -Filter "version-*" |
        Sort-Object LastWriteTime -Descending |
        ForEach-Object { Join-Path $_.FullName "RobloxStudioBeta.exe" } |
        Where-Object { Test-Path -LiteralPath $_ } |
        Select-Object -First 1
}

if (-not $studioPath -and (Test-Path -LiteralPath $bundledStudio)) {
    $studioPath = $bundledStudio
}

if (-not $studioPath) {
    throw "RobloxStudioBeta.exe nao foi encontrado na instalacao nem na pasta deste projeto."
}

$pluginSource = Join-Path $PSScriptRoot "TBloxStudio.plugin.lua"
$pluginDirectory = Join-Path $env:LOCALAPPDATA "Roblox\Plugins"
$pluginDestination = Join-Path $pluginDirectory "TBloxStudio.lua"

if (-not (Test-Path -LiteralPath $pluginSource)) {
    throw "O arquivo do plugin T-BloxStudio nao foi encontrado: $pluginSource"
}

New-Item -ItemType Directory -Path $pluginDirectory -Force | Out-Null
Copy-Item -LiteralPath $pluginSource -Destination $pluginDestination -Force

Start-Process -FilePath $studioPath -WorkingDirectory (Split-Path -Parent $studioPath)