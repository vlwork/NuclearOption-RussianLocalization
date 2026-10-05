[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$BuildRoot)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$repoRoot = Split-Path $PSScriptRoot -Parent
$testRoot = Assert-PathUnderRoot (Join-Path $repoRoot ('.verification\release-installer-tests-' + [guid]::NewGuid().ToString('N'))) $repoRoot
$runtimeFiles = @(Get-ProductionFiles -BuildRoot $BuildRoot)
$packageRoot = Join-Path $testRoot 'package'
$packagePlugin = Join-Path $packageRoot 'BepInEx\plugins\LocalizationPatch'
New-Item -ItemType Directory -Path $packagePlugin -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot 'installer\Install.ps1') -Destination (Join-Path $packageRoot 'Install.ps1')
Copy-Item -LiteralPath (Join-Path $repoRoot 'installer\Install.cmd') -Destination (Join-Path $packageRoot 'Install.cmd')
foreach ($file in $runtimeFiles) {
    Copy-Item -LiteralPath $file.Path -Destination (Join-Path $packagePlugin $file.Name)
}
$installer = Join-Path $packageRoot 'Install.ps1'

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
}

function New-MockGame {
    param([string]$Name)
    $path = Join-Path $testRoot $Name
    Assert-PathUnderRoot $path $repoRoot | Out-Null
    foreach ($directory in @('NuclearOption_Data\Managed', 'BepInEx\core', 'BepInEx\plugins')) {
        New-Item -ItemType Directory -Path (Join-Path $path $directory) -Force | Out-Null
    }
    foreach ($marker in @('NuclearOption.exe', 'BepInEx\core\BepInEx.dll', 'BepInEx\core\0Harmony.dll')) {
        New-Item -ItemType File -Path (Join-Path $path $marker) | Out-Null
    }
    return $path
}

function Get-TreeFingerprint {
    param([string]$Root)
    $records = @(Get-ChildItem -LiteralPath $Root -Recurse -Force | Sort-Object FullName | ForEach-Object {
        $relative = $_.FullName.Substring($Root.Length)
        if ($_.PSIsContainer) { "DIR:$relative" } else { "FILE:$relative=$((Get-FileHash -LiteralPath $_.FullName).Hash)" }
    })
    return $records -join "`n"
}

function Assert-Installed {
    param([string]$Game)
    $target = Join-Path $Game 'BepInEx\plugins\LocalizationPatch'
    $names = @(Get-ChildItem -LiteralPath $target -File | Sort-Object Name | ForEach-Object Name)
    Assert-True ($names.Count -eq 4) 'Release installer did not produce exactly four files in a clean target.'
    Assert-True (($names -join '|') -ceq ((@($runtimeFiles.Name) | Sort-Object) -join '|')) 'Release installer produced unexpected target files.'
    foreach ($file in $runtimeFiles) {
        Assert-True ((Get-FileHash -LiteralPath (Join-Path $target $file.Name)).Hash -ceq (Get-FileHash -LiteralPath $file.Path).Hash) "Installed content mismatch: $($file.Name)"
    }
}

$results = New-Object System.Collections.Generic.List[object]

$game = New-MockGame 'A clean release install'
& $installer -GameDir $game -Confirm:$false
Assert-Installed $game
$results.Add([pscustomobject]@{ Test = 'A clean release install'; Result = 'PASS' })

$backupCount = @(Get-ChildItem -LiteralPath (Join-Path $game 'LocalizationPatchBackups') -Directory).Count
& $installer -GameDir $game -Confirm:$false
Assert-Installed $game
Assert-True (@(Get-ChildItem -LiteralPath (Join-Path $game 'LocalizationPatchBackups') -Directory).Count -eq $backupCount + 1) 'Upgrade did not create a new backup.'
$results.Add([pscustomobject]@{ Test = 'B repeated install creates recoverable backup'; Result = 'PASS' })

$dryRun = New-MockGame 'C whatif'
$fingerprint = Get-TreeFingerprint $dryRun
& $installer -GameDir $dryRun -WhatIf -Confirm:$false
Assert-True ((Get-TreeFingerprint $dryRun) -ceq $fingerprint) 'Release installer -WhatIf mutated filesystem.'
$results.Add([pscustomobject]@{ Test = 'C whatif is read-only'; Result = 'PASS' })

$duplicateGame = New-MockGame 'D duplicate relocation'
$duplicateDir = Join-Path $duplicateGame 'BepInEx\plugins\old localization'
New-Item -ItemType Directory -Path $duplicateDir -Force | Out-Null
Copy-Item -LiteralPath $runtimeFiles[0].Path -Destination (Join-Path $duplicateDir 'renamed.dll')
& $installer -GameDir $duplicateGame -Confirm:$false
Assert-Installed $duplicateGame
Assert-True (-not (Test-Path -LiteralPath (Join-Path $duplicateDir 'renamed.dll'))) 'Duplicate localization assembly remained active under BepInEx.'
$results.Add([pscustomobject]@{ Test = 'D duplicate assembly is relocated'; Result = 'PASS' })

$results | Format-Table -AutoSize
$resultPath = Join-Path $testRoot 'results.json'
[IO.File]::WriteAllText($resultPath, ($results | ConvertTo-Json), (New-Object Text.UTF8Encoding($false)))
Write-Host "All release installer tests passed. Evidence retained at: $testRoot"
