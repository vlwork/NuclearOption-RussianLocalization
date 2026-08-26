[CmdletBinding()]
param(
    [ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version = '3.6.0',
    [string]$GameDir,
    [switch]$SkipBuild
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
Add-Type -AssemblyName System.IO.Compression.FileSystem

$projectRoot = Split-Path $PSScriptRoot -Parent
$releaseDir = Join-Path $projectRoot 'release'
$stageDir = Assert-PathUnderRoot -Path (Join-Path $releaseDir '.staging') -Root $projectRoot
$pluginDir = Join-Path $stageDir 'BepInEx\plugins\LocalizationPatch'
$zipPath = Join-Path $releaseDir "NuclearOption-RussianLocalization-v$Version.zip"

if (-not $SkipBuild) {
    & (Join-Path $PSScriptRoot 'build.ps1') -GameDir $GameDir
    if ($LASTEXITCODE -ne 0) { throw 'Build script failed.' }
}

$entryCount = Test-RussianTranslation -Path (Join-Path $projectRoot 'localization\ru.json')
if (Test-Path -LiteralPath $stageDir) { Remove-Item -LiteralPath $stageDir -Recurse -Force }
New-Item -ItemType Directory -Path $pluginDir -Force | Out-Null

$files = @{
    (Join-Path $projectRoot 'src\LocalizationPatch\bin\Release\net472\LocalizationPatch.dll') = 'LocalizationPatch.dll'
    (Join-Path $projectRoot 'src\LocalizationPatchDropdown\bin\Release\net472\LocalizationPatchDropdown.dll') = 'LocalizationPatchDropdown.dll'
    (Join-Path $projectRoot 'localization\ru.json') = 'ru.json'
    (Join-Path $projectRoot 'fonts\Tektur-Reg.ttf') = 'Tektur-Reg.ttf'
}
foreach ($source in $files.Keys) {
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Package input missing: '$source'." }
    Copy-Item -LiteralPath $source -Destination (Join-Path $pluginDir $files[$source])
}

$activeDlls = @(Get-ChildItem -LiteralPath $pluginDir -Filter 'LocalizationPatch*.dll' -File)
if ($activeDlls.Count -ne 2) { throw "Expected exactly two active LocalizationPatch DLLs; found $($activeDlls.Count)." }
$expectedDlls = @('LocalizationPatch.dll', 'LocalizationPatchDropdown.dll')
if (@($activeDlls.Name | Where-Object { $_ -notin $expectedDlls }).Count -ne 0) {
    throw 'Unexpected active LocalizationPatch DLL found in package staging.'
}
if (@(Get-ChildItem -LiteralPath $stageDir -Recurse -File | Where-Object { $_.Name -like '*.bak' }).Count -ne 0) {
    throw 'Package staging contains .bak files.'
}
if (@(Get-ChildItem -LiteralPath $stageDir -Recurse -File | Where-Object { $_.Name -match '3\.6\.[12]' }).Count -ne 0) {
    throw 'Package staging contains an experimental 3.6.1/3.6.2 file.'
}

if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
Compress-Archive -LiteralPath (Join-Path $stageDir 'BepInEx') -DestinationPath $zipPath -CompressionLevel Optimal

$archive = [IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $entries = @($archive.Entries | Where-Object { $_.Name })
    if (@($entries | Where-Object { $_.FullName -match '(?i)\.bak$' }).Count -ne 0) {
        throw 'Release ZIP contains .bak files.'
    }
    if (@($entries | Where-Object { $_.FullName -match '3\.6\.[12]' }).Count -ne 0) {
        throw 'Release ZIP contains an experimental 3.6.1/3.6.2 file.'
    }
    $zipDlls = @($entries | Where-Object {
        (($_.FullName -replace '\\', '/') -match
            '^BepInEx/plugins/LocalizationPatch/LocalizationPatch[^/]*\.dll$')
    })
    if ($zipDlls.Count -ne 2) {
        throw "Release ZIP must contain exactly two active LocalizationPatch DLLs; found $($zipDlls.Count)."
    }
} finally {
    $archive.Dispose()
}

Remove-Item -LiteralPath $stageDir -Recurse -Force
$hash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash
Write-Host "Package: $zipPath"
Write-Host "ru.json entries: $entryCount"
Write-Host "SHA256: $hash"
Write-Output $zipPath
