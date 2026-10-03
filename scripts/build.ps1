[CmdletBinding()]
param([string]$GameDir, [string]$OutputRoot)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$projectRoot = Split-Path $PSScriptRoot -Parent
$resolvedGameDir = Resolve-NuclearOptionGameDir -GameDir $GameDir
$entryCount = Test-RussianTranslation -Path (Join-Path $projectRoot 'localization\ru.json')
if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) { throw '.NET SDK is required.' }
$buildRoot = $projectRoot
if ($OutputRoot) {
    $buildRoot = Assert-PathUnderRoot -Path $OutputRoot -Root $projectRoot
    Assert-NoReparsePoint $buildRoot
    foreach ($name in @('LocalizationPatch', 'LocalizationPatchDropdown')) {
        $destination = Join-Path $buildRoot "src\$name"
        New-Item -ItemType Directory -Path $destination -Force | Out-Null
        # Isolated source-only build: no game DLLs are copied / без копирования DLL игры.
        foreach ($file in Get-ChildItem -LiteralPath (Join-Path $projectRoot "src\$name") -File) {
            if ($file.Extension -in @('.cs', '.csproj')) {
                Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $destination $file.Name) -Force
            }
        }
    }
}
$offlineFeed = Join-Path $projectRoot '.verification\empty-offline-feed'
Assert-NoReparsePoint $offlineFeed
New-Item -ItemType Directory -Path $offlineFeed -Force | Out-Null
$offlineEnvironment = @{
    DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE = 'true'
    DOTNET_SKIP_FIRST_TIME_EXPERIENCE = '1'
}
$previousDotnetEnvironment = @{}
foreach ($variable in $offlineEnvironment.Keys) {
    $previousDotnetEnvironment[$variable] = [Environment]::GetEnvironmentVariable($variable, 'Process')
    [Environment]::SetEnvironmentVariable($variable, $offlineEnvironment[$variable], 'Process')
}
try {
    foreach ($name in @('LocalizationPatch', 'LocalizationPatchDropdown')) {
        $project = Join-Path $buildRoot "src\$name\$name.csproj"
        # No NuGet endpoints, telemetry, workload notifications or audit traffic.
        & dotnet restore $project --source $offlineFeed --nologo "-p:NuclearOptionDir=$resolvedGameDir" '-p:NuGetAudit=false'
        if ($LASTEXITCODE -ne 0) { throw "Offline restore failed: $name" }
        & dotnet build $project --no-restore --configuration Release --nologo --verbosity minimal -warnaserror "-p:NuclearOptionDir=$resolvedGameDir"
        if ($LASTEXITCODE -ne 0) { throw "Build failed: $name" }
    }
} finally {
    foreach ($variable in $previousDotnetEnvironment.Keys) {
        [Environment]::SetEnvironmentVariable($variable, $previousDotnetEnvironment[$variable], 'Process')
    }
}
Get-ProductionFiles -BuildRoot $buildRoot | Where-Object Name -like '*.dll' | ForEach-Object { Write-Output $_.Path }
Write-Host "Build passed with warnings as errors; ru.json=$entryCount. Game references were read-only."
