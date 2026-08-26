[CmdletBinding()]
param([string]$GameDir)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$projectRoot = Split-Path $PSScriptRoot -Parent
$translationPath = Join-Path $projectRoot 'localization\ru.json'
$resolvedGameDir = Resolve-NuclearOptionGameDir -GameDir $GameDir

$dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
if ($null -eq $dotnet) { throw '.NET SDK was not found in PATH.' }
$sdks = @(& dotnet --list-sdks)
if ($LASTEXITCODE -ne 0 -or $sdks.Count -eq 0) { throw '.NET SDK is not installed.' }

$entryCount = Test-RussianTranslation -Path $translationPath
Write-Host "Game: $resolvedGameDir"
Write-Host ".NET SDK: $($sdks | Select-Object -Last 1)"
Write-Host "ru.json: valid, $entryCount entries"

$projects = @(
    (Join-Path $projectRoot 'src\LocalizationPatch\LocalizationPatch.csproj'),
    (Join-Path $projectRoot 'src\LocalizationPatchDropdown\LocalizationPatchDropdown.csproj')
)

foreach ($project in $projects) {
    Write-Host "Building $([IO.Path]::GetFileName($project))..."
    $arguments = @(
        'build', $project,
        '--configuration', 'Release',
        '--nologo',
        '--verbosity', 'minimal',
        '-warnaserror',
        "-p:NuclearOptionDir=$resolvedGameDir"
    )
    & dotnet @arguments
    if ($LASTEXITCODE -ne 0) { throw "Build failed: '$project'." }
}

$mainDll = Join-Path $projectRoot 'src\LocalizationPatch\bin\Release\net472\LocalizationPatch.dll'
$dropdownDll = Join-Path $projectRoot 'src\LocalizationPatchDropdown\bin\Release\net472\LocalizationPatchDropdown.dll'
foreach ($dll in @($mainDll, $dropdownDll)) {
    if (-not (Test-Path -LiteralPath $dll -PathType Leaf)) { throw "Build output missing: '$dll'." }
}

Write-Host 'Build completed successfully with warnings treated as errors.'
Write-Output $mainDll
Write-Output $dropdownDll
