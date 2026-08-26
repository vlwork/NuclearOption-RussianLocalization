[CmdletBinding()]
param([string]$GameDir)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$projectRoot = Split-Path $PSScriptRoot -Parent
$resolvedGameDir = Resolve-NuclearOptionGameDir -GameDir $GameDir
$pluginsRoot = Join-Path $resolvedGameDir 'BepInEx\plugins'
$targetDir = Join-Path $pluginsRoot 'LocalizationPatch'
$backupRoot = Join-Path $resolvedGameDir 'BepInEx\LocalizationPatchBackups'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDir = Join-Path $backupRoot "LocalizationPatch_$stamp"

& (Join-Path $PSScriptRoot 'build.ps1') -GameDir $resolvedGameDir
if ($LASTEXITCODE -ne 0) { throw 'Build script failed.' }
Test-RussianTranslation -Path (Join-Path $projectRoot 'localization\ru.json') | Out-Null

New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
if (Test-Path -LiteralPath $targetDir) {
    Copy-Item -LiteralPath $targetDir -Destination $backupDir -Recurse -Force
    Write-Host "Backup created outside the plugin scan path: $backupDir"
} else {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

# A full backup now exists. Remove only loadable DLLs and DLL backup artifacts from the
# active plugin tree; unrelated user files stay in place.
Get-ChildItem -LiteralPath $targetDir -Recurse -File | Where-Object {
    $_.Extension -ieq '.dll' -or $_.Name -match '(?i)\.dll\.(bak|backup|old)$'
} | Remove-Item -Force

$installFiles = @{
    (Join-Path $projectRoot 'src\LocalizationPatch\bin\Release\net472\LocalizationPatch.dll') = 'LocalizationPatch.dll'
    (Join-Path $projectRoot 'src\LocalizationPatchDropdown\bin\Release\net472\LocalizationPatchDropdown.dll') = 'LocalizationPatchDropdown.dll'
    (Join-Path $projectRoot 'localization\ru.json') = 'ru.json'
    (Join-Path $projectRoot 'fonts\Tektur-Reg.ttf') = 'Tektur-Reg.ttf'
}
foreach ($source in $installFiles.Keys) {
    Copy-Item -LiteralPath $source -Destination (Join-Path $targetDir $installFiles[$source]) -Force
}

$activeDlls = @(Get-ChildItem -LiteralPath $targetDir -Recurse -Filter '*.dll' -File)
if ($activeDlls.Count -ne 2) { throw "Installation has $($activeDlls.Count) active DLLs; expected two." }
$expectedDlls = @('LocalizationPatch.dll', 'LocalizationPatchDropdown.dll')
if (@($activeDlls.Name | Where-Object { $_ -notin $expectedDlls }).Count -ne 0) {
    throw 'Installation contains an unexpected active LocalizationPatch DLL.'
}

Write-Host "Installed to: $targetDir"
Write-Host 'Active DLLs: LocalizationPatch.dll, LocalizationPatchDropdown.dll'
if (Test-Path -LiteralPath $backupDir) { Write-Host "Backup: $backupDir" }
