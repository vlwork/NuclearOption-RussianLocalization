[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param([string]$GameDir, [switch]$SkipBuild, [string]$BuildRoot)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$projectRoot = Split-Path $PSScriptRoot -Parent
$gameRoot = Resolve-NuclearOptionGameDir -GameDir $GameDir
$pluginsRoot = Join-Path $gameRoot 'BepInEx\plugins'
$targetDir = Join-Path $pluginsRoot 'LocalizationPatch'
$backupRoot = Join-Path $gameRoot 'LocalizationPatchBackups'
$legacyBackup = Join-Path $gameRoot 'BepInEx\LocalizationPatchBackups'
foreach ($path in @($pluginsRoot, $targetDir, $backupRoot, $legacyBackup)) { Assert-NoReparsePoint $path }
Test-RussianTranslation (Join-Path $projectRoot 'localization\ru.json') | Out-Null
$duplicates = @()
if (Test-Path -LiteralPath $pluginsRoot) {
    $items = @(Get-ChildItem -LiteralPath $pluginsRoot -Recurse -Force)
    if (@($items | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
        throw 'Plugin scan contains reparse points; inspect manually before installation.'
    }
    foreach ($file in $items | Where-Object { -not $_.PSIsContainer -and $_.Name -match '(?i)\.dll(?:\.(?:bak|backup|old))?$' }) {
        $assemblyName = $null
        try { $assemblyName = [Reflection.AssemblyName]::GetAssemblyName($file.FullName).Name } catch {
            if ($file.Name -match '(?i)^LocalizationPatch.*\.dll') {
                throw "Cannot safely identify suspected localization DLL: $($file.FullName)"
            }
        }
        if ($file.DirectoryName -ieq $targetDir -and $file.Name -in @('LocalizationPatch.dll', 'LocalizationPatchDropdown.dll') -and
            $assemblyName -cne [IO.Path]::GetFileNameWithoutExtension($file.Name)) {
            throw "Intended target contains an unrelated assembly; refusing overwrite: $($file.FullName)"
        }
        if ($assemblyName -in @('LocalizationPatch', 'LocalizationPatchDropdown')) {
            $duplicates += $file
            Write-Host "Identified $assemblyName assembly: $($file.FullName)"
        }
    }
}
$backupDir = Join-Path $backupRoot ('LocalizationPatch_' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '_' + [guid]::NewGuid().ToString('N'))
$backupDir = Assert-PathUnderRoot $backupDir $gameRoot
Write-Host "Backup destination (outside all BepInEx): $backupDir"
# A single transaction decision means -WhatIf never builds, copies, moves or creates directories.
if (-not $PSCmdlet.ShouldProcess($gameRoot, "Back up old localization, relocate identified duplicates/legacy backups, install four validated files")) { return }
if (-not $SkipBuild) { & (Join-Path $PSScriptRoot 'build.ps1') -GameDir $gameRoot -OutputRoot $BuildRoot }
$files = @(Get-ProductionFiles -BuildRoot $BuildRoot)
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
if (Test-Path -LiteralPath $targetDir) {
    Copy-Item -LiteralPath $targetDir -Destination (Join-Path $backupDir 'previous-target') -Recurse
}
# Backups are completed before any active file is moved or replaced.
$moved = New-Object System.Collections.Generic.List[object]
$replaced = New-Object System.Collections.Generic.List[object]
try {
    if (Test-Path -LiteralPath $legacyBackup) {
        if (@(Get-ChildItem -LiteralPath $legacyBackup -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
            throw 'Legacy backup tree contains reparse points; inspect manually.'
        }
        $destination = Join-Path $backupDir 'legacy-backups'
        Move-Item -LiteralPath $legacyBackup -Destination $destination
        $moved.Add([pscustomobject]@{ Source = $legacyBackup; Destination = $destination })
    }
    foreach ($file in $duplicates) {
        # Old exact targets are backed up then replaced; newly installed targets are never rescanned/moved.
        if ($file.DirectoryName -ieq $targetDir -and $file.Name -in @('LocalizationPatch.dll', 'LocalizationPatchDropdown.dll')) { continue }
        $relative = $file.FullName.Substring($pluginsRoot.Length).TrimStart('\')
        $destination = Join-Path (Join-Path $backupDir 'duplicates') $relative
        Assert-PathUnderRoot $destination $backupDir | Out-Null
        New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
        Move-Item -LiteralPath $file.FullName -Destination $destination
        $moved.Add([pscustomobject]@{ Source = $file.FullName; Destination = $destination })
    }
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    foreach ($file in $files) {
        $destination = Join-Path $targetDir $file.Name
        $previous = Join-Path (Join-Path $backupDir 'previous-target') $file.Name
        $replaced.Add([pscustomobject]@{ Path = $destination; Previous = $previous })
        Copy-Item -LiteralPath $file.Path -Destination $destination -Force
        if ((Get-FileHash -LiteralPath $destination).Hash -cne (Get-FileHash -LiteralPath $file.Path).Hash) { throw "Installed hash mismatch: $($file.Name)" }
    }
    $active = @()
    foreach ($file in Get-ChildItem -LiteralPath $pluginsRoot -Recurse -Filter '*.dll' -File) {
        try {
            if ([Reflection.AssemblyName]::GetAssemblyName($file.FullName).Name -in @('LocalizationPatch', 'LocalizationPatchDropdown')) { $active += $file }
        } catch { }
    }
    if ($active.Count -ne 2 -or @($active | Where-Object DirectoryName -ine $targetDir).Count) { throw 'Unexpected active localization assembly after installation.' }
} catch {
    # Recovery never deletes: displaced partial files are kept outside BepInEx for diagnosis.
    foreach ($item in $replaced) {
        if (Test-Path -LiteralPath $item.Path) {
            Move-Item -LiteralPath $item.Path -Destination (Join-Path $backupDir ('partial-' + [IO.Path]::GetFileName($item.Path)))
        }
        if (Test-Path -LiteralPath $item.Previous) { Copy-Item -LiteralPath $item.Previous -Destination $item.Path }
    }
    for ($i = $moved.Count - 1; $i -ge 0; $i--) {
        Move-Item -LiteralPath $moved[$i].Destination -Destination $moved[$i].Source
    }
    throw
}
Write-Host "Installed: $targetDir"
Write-Host "Active localization DLLs: 2; unrelated plugins untouched; recoverable backup: $backupDir"
