Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Test-NuclearOptionGameDir {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Container)) { return $false }
    $required = @(
        (Join-Path $Path 'NuclearOption.exe'),
        (Join-Path $Path 'NuclearOption_Data\Managed'),
        (Join-Path $Path 'BepInEx\core\BepInEx.dll'),
        (Join-Path $Path 'BepInEx\core\0Harmony.dll')
    )
    return @($required | Where-Object { -not (Test-Path -LiteralPath $_) }).Count -eq 0
}

function Resolve-NuclearOptionGameDir {
    param([string]$GameDir)

    if ($GameDir) {
        $resolved = [IO.Path]::GetFullPath($GameDir)
        if (-not (Test-NuclearOptionGameDir $resolved)) {
            throw "Nuclear Option or BepInEx 5 is incomplete at '$resolved'."
        }
        return $resolved.TrimEnd('\')
    }

    $steamRoots = New-Object System.Collections.Generic.List[string]
    if ($env:NUCLEAR_OPTION_DIR) {
        $candidate = [IO.Path]::GetFullPath($env:NUCLEAR_OPTION_DIR)
        if (Test-NuclearOptionGameDir $candidate) { return $candidate.TrimEnd('\') }
    }

    foreach ($registryPath in @('HKCU:\Software\Valve\Steam', 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam')) {
        try {
            $steam = Get-ItemProperty -LiteralPath $registryPath -ErrorAction Stop
            foreach ($property in @('SteamPath', 'InstallPath')) {
                $value = $steam.$property
                if ($value) { $steamRoots.Add(([IO.Path]::GetFullPath($value)).TrimEnd('\')) }
            }
        } catch { }
    }

    foreach ($standard in @(
        'C:\Program Files (x86)\Steam',
        'C:\Program Files\Steam'
    )) {
        if (Test-Path -LiteralPath $standard) { $steamRoots.Add($standard) }
    }

    foreach ($drive in Get-PSDrive -PSProvider FileSystem -ErrorAction SilentlyContinue) {
        foreach ($folder in @('SteamLibrary', 'Steam')) {
            $library = Join-Path $drive.Root $folder
            if (Test-Path -LiteralPath $library) { $steamRoots.Add($library.TrimEnd('\')) }
        }
    }

    $libraryRoots = New-Object System.Collections.Generic.List[string]
    foreach ($steamRoot in $steamRoots | Select-Object -Unique) {
        $libraryRoots.Add($steamRoot)
        $vdf = Join-Path $steamRoot 'steamapps\libraryfolders.vdf'
        if (-not (Test-Path -LiteralPath $vdf)) { continue }

        foreach ($line in Get-Content -LiteralPath $vdf -ErrorAction SilentlyContinue) {
            if ($line -match '^\s*"(?:path|\d+)"\s*"([^"]+)"') {
                $path = $matches[1] -replace '\\\\', '\'
                if (Test-Path -LiteralPath $path) { $libraryRoots.Add($path.TrimEnd('\')) }
            }
        }
    }

    foreach ($libraryRoot in $libraryRoots | Select-Object -Unique) {
        $candidate = Join-Path $libraryRoot 'steamapps\common\Nuclear Option'
        if (Test-NuclearOptionGameDir $candidate) {
            return ([IO.Path]::GetFullPath($candidate)).TrimEnd('\')
        }
    }

    throw 'Nuclear Option with BepInEx 5 was not found. Pass -GameDir or set NUCLEAR_OPTION_DIR.'
}

function Test-RussianTranslation {
    param([Parameter(Mandatory = $true)][string]$Path)

    $root = Split-Path $PSScriptRoot -Parent
    $result = @(& python -X utf8 (Join-Path $root 'tools\audit-localization.py') --check-only --strict --localization $Path)
    if ($LASTEXITCODE -ne 0) { throw "Objective localization QA failed: $($result -join ' ')" }
    $audit = ($result -join '') | ConvertFrom-Json
    return [int]$audit.metrics.EntryCount
}

function Get-LocalizationReleaseVersion {
    $root = Split-Path $PSScriptRoot -Parent
    $source = [IO.File]::ReadAllText((Join-Path $root 'src\LocalizationPatch\Plugin.cs'))
    $match = [regex]::Match($source, 'BepInPlugin\("com\.noms\.localizationpatch", "Localization Patch", "(\d+\.\d+\.\d+)"\)')
    if (-not $match.Success) { throw 'Runtime version was not found.' }
    return $match.Groups[1].Value
}

function Get-ProductionFiles {
    param([string]$BuildRoot)
    $root = Split-Path $PSScriptRoot -Parent
    if (-not $BuildRoot) { $BuildRoot = $root }
    $files = @(
        [pscustomobject]@{ Name = 'LocalizationPatch.dll'; Path = Join-Path $BuildRoot 'src\LocalizationPatch\bin\Release\net472\LocalizationPatch.dll' },
        [pscustomobject]@{ Name = 'LocalizationPatchDropdown.dll'; Path = Join-Path $BuildRoot 'src\LocalizationPatchDropdown\bin\Release\net472\LocalizationPatchDropdown.dll' },
        [pscustomobject]@{ Name = 'ru.json'; Path = Join-Path $root 'localization\ru.json' },
        [pscustomobject]@{ Name = 'Tektur-Reg.ttf'; Path = Join-Path $root 'fonts\Tektur-Reg.ttf' }
    )
    foreach ($file in $files) {
        if (-not (Test-Path -LiteralPath $file.Path -PathType Leaf)) { throw "Production input missing: $($file.Path)" }
    }
    $version = Get-LocalizationReleaseVersion
    $dllVersion = (Get-Item -LiteralPath $files[0].Path).VersionInfo.FileVersion
    if ($dllVersion -ne "$version.0") { throw "Main DLL version $dllVersion does not match source $version." }
    return $files
}

function Get-ReleaseDocumentationFiles {
    $root = Split-Path $PSScriptRoot -Parent
    $files = @(
        [pscustomobject]@{ ArchivePath = 'LICENSE.md'; Path = Join-Path $root 'LICENSE.md' },
        [pscustomobject]@{ ArchivePath = 'LICENSE-CODE'; Path = Join-Path $root 'LICENSE-CODE' },
        [pscustomobject]@{ ArchivePath = 'LICENSE-TRANSLATION'; Path = Join-Path $root 'LICENSE-TRANSLATION' },
        [pscustomobject]@{ ArchivePath = 'THIRD_PARTY_NOTICES.md'; Path = Join-Path $root 'THIRD_PARTY_NOTICES.md' },
        [pscustomobject]@{ ArchivePath = 'third_party/OFL-1.1.txt'; Path = Join-Path $root 'third_party\OFL-1.1.txt' },
        [pscustomobject]@{ ArchivePath = 'localization/PROVENANCE.md'; Path = Join-Path $root 'localization\PROVENANCE.md' }
    )
    foreach ($file in $files) {
        if (-not (Test-Path -LiteralPath $file.Path -PathType Leaf)) { throw "Release documentation missing: $($file.Path)" }
    }
    return $files
}

function Assert-NoReparsePoint {
    param([Parameter(Mandatory = $true)][string]$Path)
    $itemPath = [IO.Path]::GetFullPath($Path)
    while ($itemPath) {
        if (Test-Path -LiteralPath $itemPath) {
            if ((Get-Item -LiteralPath $itemPath -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Refusing a reparse-point path: $itemPath"
            }
        }
        $parent = Split-Path $itemPath -Parent
        if ($parent -eq $itemPath) { break }
        $itemPath = $parent
    }
}

function Assert-PathUnderRoot {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Root
    )

    $fullPath = [IO.Path]::GetFullPath($Path).TrimEnd('\')
    $fullRoot = [IO.Path]::GetFullPath($Root).TrimEnd('\')
    if (-not $fullPath.StartsWith($fullRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing operation outside '$fullRoot': '$fullPath'."
    }
    return $fullPath
}
