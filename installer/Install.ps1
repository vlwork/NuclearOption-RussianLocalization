[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param([string]$GameDir)

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

function Select-NuclearOptionGameDir {
    $selected = $null
    try {
        Add-Type -AssemblyName System.Windows.Forms
        $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
        $dialog.Description = 'Выберите папку Nuclear Option, где находится NuclearOption.exe'
        $dialog.ShowNewFolderButton = $false
        if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            $selected = $dialog.SelectedPath
        }
        $dialog.Dispose()
    } catch { }

    if (-not $selected) {
        $selected = Read-Host 'Введите полный путь к папке Nuclear Option'
    }
    return $selected
}

function Resolve-NuclearOptionGameDir {
    param([string]$RequestedGameDir)

    if ($RequestedGameDir) {
        $resolved = [IO.Path]::GetFullPath($RequestedGameDir)
        if (-not (Test-NuclearOptionGameDir $resolved)) {
            throw "Nuclear Option или BepInEx 5 не найдены полностью в '$resolved'."
        }
        return $resolved.TrimEnd('\')
    }

    if ($env:NUCLEAR_OPTION_DIR) {
        $candidate = [IO.Path]::GetFullPath($env:NUCLEAR_OPTION_DIR)
        if (Test-NuclearOptionGameDir $candidate) { return $candidate.TrimEnd('\') }
    }

    $steamRoots = New-Object System.Collections.Generic.List[string]
    foreach ($registryPath in @('HKCU:\Software\Valve\Steam', 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam')) {
        try {
            $steam = Get-ItemProperty -LiteralPath $registryPath -ErrorAction Stop
            foreach ($property in @('SteamPath', 'InstallPath')) {
                $value = $steam.$property
                if ($value) { $steamRoots.Add(([IO.Path]::GetFullPath($value)).TrimEnd('\')) }
            }
        } catch { }
    }

    foreach ($standard in @('C:\Program Files (x86)\Steam', 'C:\Program Files\Steam')) {
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

    $selected = Select-NuclearOptionGameDir
    if (-not $selected) { throw 'Установка отменена: папка Nuclear Option не выбрана.' }
    $selected = [IO.Path]::GetFullPath($selected)
    if (-not (Test-NuclearOptionGameDir $selected)) {
        throw "В выбранной папке не найдены Nuclear Option и рабочая установка BepInEx 5: '$selected'."
    }
    return $selected.TrimEnd('\')
}

function Assert-NoReparsePoint {
    param([Parameter(Mandatory = $true)][string]$Path)

    $itemPath = [IO.Path]::GetFullPath($Path)
    while ($itemPath) {
        if (Test-Path -LiteralPath $itemPath) {
            if ((Get-Item -LiteralPath $itemPath -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Установка через reparse point запрещена: $itemPath"
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
        throw "Отказ от операции вне '$fullRoot': '$fullPath'."
    }
    return $fullPath
}

$packageRoot = [IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\')
$sourceDir = Join-Path $packageRoot 'BepInEx\plugins\LocalizationPatch'
$expectedNames = @('LocalizationPatch.dll', 'LocalizationPatchDropdown.dll', 'ru.json', 'Tektur-Reg.ttf')

Assert-NoReparsePoint $packageRoot
Assert-NoReparsePoint $sourceDir

if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
    throw "Повреждён пакет: не найдена папка '$sourceDir'."
}

$sourceItems = @(Get-ChildItem -LiteralPath $sourceDir -Force)
if (@($sourceItems | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
    throw 'Повреждён пакет: runtime-каталог содержит reparse point.'
}
$sourceFiles = @($sourceItems | Where-Object { -not $_.PSIsContainer })
$sourceNames = @($sourceFiles.Name | Sort-Object)
if ($sourceNames.Count -ne 4 -or ($sourceNames -join '|') -cne (($expectedNames | Sort-Object) -join '|')) {
    throw "Повреждён пакет: ожидались ровно четыре runtime-файла: $($expectedNames -join ', ')."
}

foreach ($name in $expectedNames) {
    $path = Join-Path $sourceDir $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf) -or (Get-Item -LiteralPath $path).Length -le 0) {
        throw "Повреждён пакет: отсутствует или пуст файл '$name'."
    }
}

$mainAssembly = [Reflection.AssemblyName]::GetAssemblyName((Join-Path $sourceDir 'LocalizationPatch.dll')).Name
$dropdownAssembly = [Reflection.AssemblyName]::GetAssemblyName((Join-Path $sourceDir 'LocalizationPatchDropdown.dll')).Name
if ($mainAssembly -cne 'LocalizationPatch' -or $dropdownAssembly -cne 'LocalizationPatchDropdown') {
    throw 'Повреждён пакет: имена runtime-сборок не совпадают с ожидаемыми.'
}

try {
    Add-Type -AssemblyName System.Web.Extensions
    $jsonPath = Join-Path $sourceDir 'ru.json'
    $jsonText = [IO.File]::ReadAllText($jsonPath, [Text.Encoding]::UTF8)
    if ([string]::IsNullOrWhiteSpace($jsonText)) { throw 'empty' }
    $serializer = New-Object System.Web.Script.Serialization.JavaScriptSerializer
    $serializer.MaxJsonLength = [int]::MaxValue
    $translation = $serializer.DeserializeObject($jsonText)
    if ($null -eq $translation) { throw 'empty' }
} catch {
    throw "Повреждён пакет: ru.json не является корректным непустым JSON. $($_.Exception.Message)"
}

$gameRoot = Resolve-NuclearOptionGameDir -RequestedGameDir $GameDir
$pluginsRoot = Join-Path $gameRoot 'BepInEx\plugins'
$targetDir = Join-Path $pluginsRoot 'LocalizationPatch'
$backupRoot = Join-Path $gameRoot 'LocalizationPatchBackups'
$legacyBackup = Join-Path $gameRoot 'BepInEx\LocalizationPatchBackups'

foreach ($path in @($gameRoot, $pluginsRoot, $targetDir, $backupRoot, $legacyBackup)) {
    Assert-NoReparsePoint $path
}

$duplicates = @()
if (Test-Path -LiteralPath $pluginsRoot) {
    $pluginItems = @(Get-ChildItem -LiteralPath $pluginsRoot -Recurse -Force)
    if (@($pluginItems | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
        throw 'В BepInEx\plugins найден reparse point. Проверьте каталог вручную перед установкой.'
    }

    foreach ($file in $pluginItems | Where-Object { -not $_.PSIsContainer -and $_.Name -match '(?i)\.dll(?:\.(?:bak|backup|old))?$' }) {
        $assemblyName = $null
        try {
            $assemblyName = [Reflection.AssemblyName]::GetAssemblyName($file.FullName).Name
        } catch {
            if ($file.Name -match '(?i)^LocalizationPatch.*\.dll') {
                throw "Не удалось безопасно определить подозрительный DLL: $($file.FullName)"
            }
        }

        if ($file.DirectoryName -ieq $targetDir -and
            $file.Name -in @('LocalizationPatch.dll', 'LocalizationPatchDropdown.dll') -and
            $assemblyName -cne [IO.Path]::GetFileNameWithoutExtension($file.Name)) {
            throw "В целевой папке находится посторонняя сборка с ожидаемым именем: $($file.FullName)"
        }

        if ($assemblyName -in @('LocalizationPatch', 'LocalizationPatchDropdown')) {
            $duplicates += $file
        }
    }
}

$backupDir = Join-Path $backupRoot ('LocalizationPatch_' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '_' + [guid]::NewGuid().ToString('N'))
$backupDir = Assert-PathUnderRoot -Path $backupDir -Root $gameRoot
$version = (Get-Item -LiteralPath (Join-Path $sourceDir 'LocalizationPatch.dll')).VersionInfo.FileVersion

Write-Host ''
Write-Host "Nuclear Option: $gameRoot"
Write-Host "Версия локализации: $version"
Write-Host "Резервная копия: $backupDir"
Write-Host ''

if (-not $PSCmdlet.ShouldProcess($gameRoot, 'Создать резервную копию и установить русскую локализацию')) { return }

New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
$previousTarget = Join-Path $backupDir 'previous-target'
if (Test-Path -LiteralPath $targetDir) {
    Copy-Item -LiteralPath $targetDir -Destination $previousTarget -Recurse
}

$externalMoved = New-Object System.Collections.Generic.List[object]
try {
    if (Test-Path -LiteralPath $legacyBackup) {
        $legacyItems = @(Get-ChildItem -LiteralPath $legacyBackup -Recurse -Force)
        if (@($legacyItems | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
            throw 'Старое дерево резервных копий содержит reparse point.'
        }
        Move-Item -LiteralPath $legacyBackup -Destination (Join-Path $backupDir 'legacy-backups')
    }

    foreach ($file in $duplicates) {
        if ($file.DirectoryName -ieq $targetDir -and
            $file.Name -in @('LocalizationPatch.dll', 'LocalizationPatchDropdown.dll')) {
            continue
        }

        $relative = $file.FullName.Substring($pluginsRoot.Length).TrimStart('\')
        $destination = Join-Path (Join-Path $backupDir 'duplicates') $relative
        Assert-PathUnderRoot -Path $destination -Root $backupDir | Out-Null
        New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null

        $isInsideTarget = $file.FullName.StartsWith($targetDir + '\', [StringComparison]::OrdinalIgnoreCase)
        Move-Item -LiteralPath $file.FullName -Destination $destination
        if (-not $isInsideTarget) {
            $externalMoved.Add([pscustomobject]@{ Source = $file.FullName; Destination = $destination })
        }
    }

    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    foreach ($name in $expectedNames) {
        $source = Join-Path $sourceDir $name
        $destination = Join-Path $targetDir $name
        Copy-Item -LiteralPath $source -Destination $destination -Force
        if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -cne
            (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash) {
            throw "Ошибка проверки установленного файла: $name"
        }
    }

    $active = @()
    foreach ($file in Get-ChildItem -LiteralPath $pluginsRoot -Recurse -Filter '*.dll' -File) {
        try {
            if ([Reflection.AssemblyName]::GetAssemblyName($file.FullName).Name -in @('LocalizationPatch', 'LocalizationPatchDropdown')) {
                $active += $file
            }
        } catch { }
    }

    if ($active.Count -ne 2 -or @($active | Where-Object { $_.DirectoryName -ine $targetDir }).Count) {
        throw 'После установки обнаружено неожиданное количество активных сборок локализации.'
    }
} catch {
    $originalError = $_

    if (Test-Path -LiteralPath $targetDir) {
        $failedTarget = Join-Path $backupDir 'failed-target'
        Move-Item -LiteralPath $targetDir -Destination $failedTarget
    }
    if (Test-Path -LiteralPath $previousTarget) {
        Copy-Item -LiteralPath $previousTarget -Destination $targetDir -Recurse
    }

    for ($i = $externalMoved.Count - 1; $i -ge 0; $i--) {
        if (Test-Path -LiteralPath $externalMoved[$i].Destination) {
            Move-Item -LiteralPath $externalMoved[$i].Destination -Destination $externalMoved[$i].Source
        }
    }

    throw $originalError
}

Write-Host ''
Write-Host 'Установка завершена успешно.' -ForegroundColor Green
Write-Host "Файлы локализации: $targetDir"
Write-Host "Резервная копия: $backupDir"
Write-Host 'Можно запускать Nuclear Option через Steam.'
