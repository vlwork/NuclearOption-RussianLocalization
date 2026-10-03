[CmdletBinding()]
param(
    [ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version,
    [string]$GameDir,
    [switch]$SkipBuild,
    [string]$BuildRoot,
    [string]$OutputDirectory
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtimeVersion = Get-LocalizationReleaseVersion
if (-not $Version) { $Version = $runtimeVersion }
if ($Version -ne $runtimeVersion -or $Version -in @('3.6.1', '3.6.2')) { throw 'Package version must match the supported runtime source.' }
if (-not $OutputDirectory) { $OutputDirectory = Join-Path $projectRoot 'release' }
$outputDir = Assert-PathUnderRoot -Path $OutputDirectory -Root $projectRoot
Assert-NoReparsePoint $outputDir
if (-not $SkipBuild) {
    & (Join-Path $PSScriptRoot 'build.ps1') -GameDir $GameDir -OutputRoot $BuildRoot
}
$entryCount = Test-RussianTranslation (Join-Path $projectRoot 'localization\ru.json')
$files = @(Get-ProductionFiles -BuildRoot $BuildRoot)
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
$zipPath = Join-Path $outputDir "NuclearOption-RussianLocalization-v$Version.zip"
$temporaryZip = Join-Path $outputDir ('.validated-' + [guid]::NewGuid().ToString('N') + '.zip')
$archive = [IO.Compression.ZipFile]::Open($temporaryZip, [IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($file in $files | Sort-Object Name) {
        $entry = $archive.CreateEntry(('BepInEx/plugins/LocalizationPatch/' + $file.Name), [IO.Compression.CompressionLevel]::Optimal)
        $entry.LastWriteTime = [DateTimeOffset]::new(2020, 1, 1, 0, 0, 0, [TimeSpan]::Zero)
        $inputStream = [IO.File]::OpenRead($file.Path)
        $outputStream = $entry.Open()
        try { $inputStream.CopyTo($outputStream) }
        finally { $inputStream.Dispose(); $outputStream.Dispose() }
    }
} finally { $archive.Dispose() }
$archive = [IO.Compression.ZipFile]::OpenRead($temporaryZip)
try {
    if ($archive.Entries.Count -ne 4) { throw 'Archive must contain exactly four production files.' }
    foreach ($file in $files) {
        $entries = @($archive.Entries | Where-Object FullName -ceq ('BepInEx/plugins/LocalizationPatch/' + $file.Name))
        if ($entries.Count -ne 1) { throw "Missing/duplicate/unexpected archive entry: $($file.Name)" }
        $stream = $entries[0].Open()
        $sha = [Security.Cryptography.SHA256]::Create()
        try { $embeddedHash = [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-', '') }
        finally { $stream.Dispose(); $sha.Dispose() }
        if ($embeddedHash -cne (Get-FileHash -LiteralPath $file.Path -Algorithm SHA256).Hash) { throw "Archive content changed: $($file.Name)" }
    }
} finally { $archive.Dispose() }
# Keep previous local artifacts recoverable; never delete them to make packaging pass.
if (Test-Path -LiteralPath $zipPath) {
    $previous = Join-Path $projectRoot ('.verification\previous-packages\' + [guid]::NewGuid().ToString('N') + '-' + [IO.Path]::GetFileName($zipPath))
    Assert-NoReparsePoint $previous
    New-Item -ItemType Directory -Path (Split-Path $previous -Parent) -Force | Out-Null
    Move-Item -LiteralPath $zipPath -Destination $previous
}
Move-Item -LiteralPath $temporaryZip -Destination $zipPath
Write-Host "Package validated: four exact files; entries=$entryCount; version=$Version"
Write-Host "SHA256: $((Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash)"
Write-Output $zipPath
