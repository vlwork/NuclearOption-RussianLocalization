[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$BuildRoot)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$repoRoot = Split-Path $PSScriptRoot -Parent
$testRoot = Assert-PathUnderRoot (Join-Path $repoRoot ('.verification\installer-tests-' + [guid]::NewGuid().ToString('N'))) $repoRoot
$files = @(Get-ProductionFiles -BuildRoot $BuildRoot)
$installer = Join-Path $PSScriptRoot 'install-local.ps1'

function Assert-True { param([bool]$Condition, [string]$Message); if (-not $Condition) { throw $Message } }
function New-MockGame {
    param([string]$Name)
    $path = Join-Path $testRoot $Name
    Assert-PathUnderRoot $path $repoRoot | Out-Null
    foreach ($directory in @('NuclearOption_Data\Managed', 'BepInEx\core', 'BepInEx\plugins')) {
        New-Item -ItemType Directory -Path (Join-Path $path $directory) -Force | Out-Null
    }
    # Empty mock markers only: never copy/install game binaries / только пустые маркеры.
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
    foreach ($file in $files) {
        Assert-True ((Get-FileHash -LiteralPath (Join-Path $target $file.Name)).Hash -ceq (Get-FileHash -LiteralPath $file.Path).Hash) "Installed content mismatch: $($file.Name)"
    }
    $localizationDlls = @(Get-ChildItem -LiteralPath (Join-Path $Game 'BepInEx') -Recurse -Filter '*.dll' -File | Where-Object { $_.DirectoryName -notlike '*\core' -and $_.Name -ne 'OtherMod.dll' })
    Assert-True ($localizationDlls.Count -eq 2) 'Backup/duplicate DLL remains under BepInEx.'
}

$results = New-Object System.Collections.Generic.List[object]
$game = New-MockGame 'A clean game with spaces'
& $installer -GameDir $game -SkipBuild -BuildRoot $BuildRoot
Assert-Installed $game
$results.Add([pscustomobject]@{ Test = 'A clean install / E spaces'; Result = 'PASS' })
$target = Join-Path $game 'BepInEx\plugins\LocalizationPatch'
[IO.File]::WriteAllText((Join-Path $target 'user.cfg'), 'keep-user-config')
[IO.File]::WriteAllText((Join-Path $target 'OtherMod.dll'), 'unrelated-user-file')
$beforeUser = (Get-FileHash -LiteralPath (Join-Path $target 'user.cfg')).Hash
$beforeOther = (Get-FileHash -LiteralPath (Join-Path $target 'OtherMod.dll')).Hash
$beforePlugin = (Get-FileHash -LiteralPath (Join-Path $target 'LocalizationPatch.dll')).Hash
& $installer -GameDir $game -SkipBuild -BuildRoot $BuildRoot
Assert-Installed $game
Assert-True ((Get-FileHash -LiteralPath (Join-Path $target 'user.cfg')).Hash -ceq $beforeUser) 'User config changed.'
Assert-True ((Get-FileHash -LiteralPath (Join-Path $target 'OtherMod.dll')).Hash -ceq $beforeOther) 'Unrelated DLL changed.'
$backup = @(Get-ChildItem -LiteralPath (Join-Path $game 'LocalizationPatchBackups') -Directory | Sort-Object Name)[-1]
Assert-True ((Get-FileHash -LiteralPath (Join-Path $backup.FullName 'previous-target\LocalizationPatch.dll')).Hash -ceq $beforePlugin) 'Upgrade backup missing or wrong.'
$results.Add([pscustomobject]@{ Test = 'B upgrade preserves user files and backup'; Result = 'PASS' })
foreach ($relative in @('BepInEx\plugins\old backup folder', 'BepInEx\plugins\another plugin', 'BepInEx\LocalizationPatchBackups\historic')) {
    $directory = Join-Path $game $relative
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
    Copy-Item -LiteralPath $files[0].Path -Destination (Join-Path $directory 'renamed-old.dll')
}
$fingerprint = Get-TreeFingerprint $game
& $installer -GameDir $game -SkipBuild -BuildRoot $BuildRoot -WhatIf
Assert-True ((Get-TreeFingerprint $game) -ceq $fingerprint) 'WhatIf mutated filesystem.'
$results.Add([pscustomobject]@{ Test = 'F dry-run no filesystem mutation'; Result = 'PASS' })
& $installer -GameDir $game -SkipBuild -BuildRoot $BuildRoot
Assert-Installed $game
Assert-True (-not (Test-Path -LiteralPath (Join-Path $game 'BepInEx\LocalizationPatchBackups'))) 'Legacy backup root was not relocated.'
$results.Add([pscustomobject]@{ Test = 'C old plugins backup / D renamed duplicate / external legacy relocation'; Result = 'PASS' })
$oldBackups = @(Get-ChildItem -LiteralPath (Join-Path $game 'LocalizationPatchBackups') -Directory).Count
& $installer -GameDir $game -SkipBuild -BuildRoot $BuildRoot
Assert-Installed $game
Assert-True (@(Get-ChildItem -LiteralPath (Join-Path $game 'LocalizationPatchBackups') -Directory).Count -eq $oldBackups + 1) 'Repeated invocation reused/deleted a backup.'
$results.Add([pscustomobject]@{ Test = 'G repeated invocation keeps previous backups'; Result = 'PASS' })
foreach ($suspectName in @('LocalizationPatch-conflict.dll', 'LocalizationPatchOld.dll')) {
    $ambiguous = New-MockGame "H ambiguous duplicate $suspectName"
    $suspect = Join-Path (Join-Path $ambiguous 'BepInEx\plugins') $suspectName
    [IO.File]::WriteAllText($suspect, 'not-a-managed-assembly')
    $fingerprint = Get-TreeFingerprint $ambiguous
    $failed = $false
    try { & $installer -GameDir $ambiguous -SkipBuild -BuildRoot $BuildRoot } catch { $failed = $true }
    Assert-True ($failed -and (Get-TreeFingerprint $ambiguous) -ceq $fingerprint) 'Ambiguous duplicate was not rejected before mutation.'
}
$results.Add([pscustomobject]@{ Test = 'H ambiguous candidate fails read-only'; Result = 'PASS' })
$unrelated = New-MockGame 'I unrelated target'
$unrelatedTarget = Join-Path $unrelated 'BepInEx\plugins\LocalizationPatch'
New-Item -ItemType Directory -Path $unrelatedTarget | Out-Null
Copy-Item -LiteralPath ([string].Assembly.Location) -Destination (Join-Path $unrelatedTarget 'LocalizationPatch.dll')
$fingerprint = Get-TreeFingerprint $unrelated
$failed = $false
try { & $installer -GameDir $unrelated -SkipBuild -BuildRoot $BuildRoot } catch { $failed = $true }
Assert-True ($failed -and (Get-TreeFingerprint $unrelated) -ceq $fingerprint) 'Unrelated exact target assembly was overwritten.'
$results.Add([pscustomobject]@{ Test = 'I unrelated exact target assembly fails read-only'; Result = 'PASS' })
$results | Format-Table -AutoSize
$resultPath = Join-Path $testRoot 'results.json'
[IO.File]::WriteAllText($resultPath, ($results | ConvertTo-Json), (New-Object Text.UTF8Encoding($false)))
Write-Host "All installer tests passed. Mock evidence retained at: $testRoot"
