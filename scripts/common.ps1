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

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Translation file not found: '$Path'."
    }

    Add-Type -AssemblyName System.Web.Extensions
    $serializer = New-Object System.Web.Script.Serialization.JavaScriptSerializer
    $serializer.MaxJsonLength = [int]::MaxValue
    try {
        $json = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
        $data = $serializer.DeserializeObject($json)
    } catch {
        throw "Invalid JSON in '$Path': $($_.Exception.Message)"
    }

    if ($null -eq $data -or $data.Count -ne 3716) {
        $actual = if ($null -eq $data) { 0 } else { $data.Count }
        throw "ru.json must contain exactly 3716 entries; found $actual."
    }
    if (-not $data.ContainsKey('IR Flares') -or $data['IR Flares'] -cne 'IR Flares') {
        throw 'ru.json["IR Flares"] must equal "IR Flares".'
    }
    if (-not $data.ContainsKey('Radar Countermeasures') -or
        $data['Radar Countermeasures'] -cne 'Radar Countermeasures') {
        throw 'ru.json["Radar Countermeasures"] must equal "Radar Countermeasures".'
    }

    $identityNames = @(
        'AFV6 AA', 'AFV6 APC', 'AFV6 AT', 'AFV6 IFV',
        'AFV8 APC', 'AFV8 IFV', 'AFV8 Mobile Air Defense',
        'ALND-4 (20kt)', 'Annex Class Carrier', 'Argus Class Frigate',
        'AT-145 Emplacement', 'Cursor Class LFD', 'Dynamo Class Destroyer',
        'FGA-57 Anvil', 'GBM-500LR', 'GPO-N (1.5kt)', 'GS25',
        'HGR-H', 'HGR-M', 'Hexhound GMG', 'Hexhound SAM',
        'HLT Mobile Artillery', 'HLT Munitions Truck', 'HLT Radar Truck',
        'HLT-CRAM', 'HLT-HEL', 'Hyperion Class Carrier',
        'IRM-S1 Emplacement', 'IRM-S2',
        'LCV25', 'LCV25 AA', 'LCV25 AT', 'LCV25 Cannon', 'LCV25 SAM',
        'LCV45', 'LCV45 Recon Truck',
        'Linebreaker APC', 'Linebreaker IFV', 'Linebreaker SAM',
        'MSV Ballistic Missile Launcher', 'MSV Nuclear Ballistic Missile Launcher',
        'MSV R9 Stratolance Launcher', 'MSV Radar', 'NL-98',
        'OTB-31 landing craft', 'Shard Class Corvette',
        'StratoLance R9 Launcher', 'Surf Class Patrol Boat'
    )
    foreach ($name in $identityNames) {
        if (-not $data.ContainsKey($name) -or $data[$name] -cne $name) {
            throw "Unit/vehicle name must remain in English: '$name'."
        }
    }

    # Model designations present in an English source string must survive verbatim inside the
    # Russian value. The two excluded all-caps labels are ordinary UI terms, not designations.
    $designationPattern = '\b(?:[A-Z]{2,}[A-Z0-9]*(?:-[A-Z0-9]+)+|[A-Z]{2,}\d+[A-Z0-9-]*)\b'
    foreach ($pair in $data.GetEnumerator()) {
        foreach ($match in [regex]::Matches([string]$pair.Key, $designationPattern)) {
            $designation = $match.Value
            if ($designation -in @('NON-NUCLEAR', 'ANTI-GRAV')) { continue }
            if (-not ([string]$pair.Value).Contains($designation)) {
                throw "Designation '$designation' was not preserved in translation key '$($pair.Key)'."
            }
        }
    }

    return $data.Count
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
