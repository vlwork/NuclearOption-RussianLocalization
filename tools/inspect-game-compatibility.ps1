[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$GameDir,
    [Parameter(Mandatory = $true)][string]$OutputDirectory
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
. (Join-Path $projectRoot 'scripts\common.ps1')
$outputRoot = Assert-PathUnderRoot -Path $OutputDirectory -Root (Join-Path $projectRoot '.verification')
Assert-NoReparsePoint $outputRoot
if (Test-Path -LiteralPath $outputRoot) { throw 'Use a new evidence directory; no overwriting.' }
$gameRoot = [IO.Path]::GetFullPath($GameDir)
$managed = Join-Path $gameRoot 'NuclearOption_Data\Managed'
$core = Join-Path $gameRoot 'BepInEx\core'

# Metadata only; never load/execute a game assembly. / Только метаданные, без запуска DLL игры.
Add-Type -Path (Join-Path $core 'Mono.Cecil.dll')
function Get-AuditTypes($types) {
    foreach ($type in $types) { $type; Get-AuditTypes $type.NestedTypes }
}
$hashes = @()
$methods = @()
$fields = @()
$literals = @()
$pluginMetadata = @()
$selection = '^(MissionMessages|MessageFeed|MessageUI|GameplayUI|ChatBox|LeaderboardPlayerEntry|EncyclopediaBrowser|DevelopmentVersionText|MissionSelectGroupButtons|MissionSelectPanel|MissionSelectListItem|MissionTagListItem|TagFilterListItem|MissionPicker|NuclearOption\.Chat\.(ChatAutocompleteUI|ChatSuggestionItemUI|ChatHoverCardUI|AllowBanListItem|ChatManager|BuiltInChatCommands)|NuclearOption\.SavedMission\.(MissionTag|MissionGroup|RecentGroup)|NuclearOption\.Networking\.Lobbies\.(LobbyListItem|LobbyDetailsModal|DedicatedServerKeyValues))(/|$)'
foreach ($name in @('Assembly-CSharp.dll', 'Unity.TextMeshPro.dll', 'UnityEngine.UI.dll', 'UnityEngine.TextCoreFontEngineModule.dll')) {
    $path = Join-Path $managed $name
    $hashes += [ordered]@{ file = "NuclearOption_Data/Managed/$name"; sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash }
    $assembly = [Mono.Cecil.AssemblyDefinition]::ReadAssembly($path)
    try {
        foreach ($type in @(Get-AuditTypes $assembly.MainModule.Types)) {
            $gameType = $name -eq 'Assembly-CSharp.dll' -and $type.FullName -match $selection
            $uiType = $type.FullName -in @('TMPro.TMP_Text', 'TMPro.TextMeshProUGUI', 'TMPro.TextMeshPro', 'TMPro.TMP_Dropdown', 'UnityEngine.UI.Text', 'UnityEngine.UI.Dropdown', 'UnityEngine.TextCore.LowLevel.FontEngine')
            if (-not ($gameType -or $uiType)) { continue }
            foreach ($field in $type.Fields) {
                $fields += [ordered]@{ type = $type.FullName; name = $field.Name; fieldType = $field.FieldType.FullName }
            }
            foreach ($method in $type.Methods) {
                if ($uiType -and $method.Name -notin @('set_text', 'SetText', 'OnEnable', 'AddOptions', 'LoadFontFace')) { continue }
                $methods += [ordered]@{
                    signature = $method.FullName; attributes = $method.Attributes.ToString()
                    il = @(if ($gameType -and $method.HasBody) { $method.Body.Instructions | ForEach-Object { $_.ToString() } })
                }
                if ($gameType -and $method.HasBody) {
                    foreach ($instruction in $method.Body.Instructions) {
                        if ($instruction.OpCode.Name -eq 'ldstr') {
                            $literals += [ordered]@{ method = $method.FullName; text = [string]$instruction.Operand }
                        }
                    }
                }
            }
        }
    } finally { $assembly.Dispose() }
}
foreach ($relative in @('NuclearOption.exe', 'NuclearOption_Data/globalgamemanagers', 'NuclearOption_Data/resources.assets', 'BepInEx/core/0Harmony.dll', 'BepInEx/core/Mono.Cecil.dll')) {
    $path = Join-Path $gameRoot $relative
    $hashes += [ordered]@{ file = $relative; sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash }
}
foreach ($path in Get-ChildItem -LiteralPath (Join-Path $gameRoot 'BepInEx\plugins') -Recurse -File -Filter '*.dll') {
    $hashes += [ordered]@{ file = $path.FullName.Substring($gameRoot.Length + 1).Replace('\', '/'); sha256 = (Get-FileHash -LiteralPath $path.FullName -Algorithm SHA256).Hash }
    $assembly = [Mono.Cecil.AssemblyDefinition]::ReadAssembly($path.FullName)
    try {
        $pluginMetadata += [ordered]@{ file = $path.Name; identity = $assembly.Name.FullName }
    } finally { $assembly.Dispose() }
}
# Never copy private logs; retain counts and known patch identifiers only. / Личные строки лога не сохраняются.
$logPath = Join-Path $gameRoot 'BepInEx\LogOutput.log'
$logSummary = $null
if (Test-Path -LiteralPath $logPath) {
    $log = [IO.File]::ReadAllText($logPath)
    $logSummary = [ordered]@{
        modifiedUtc = (Get-Item -LiteralPath $logPath).LastWriteTimeUtc.ToString('o')
        warnings = [regex]::Matches($log, '(?im)^\[Warning').Count
        errors = [regex]::Matches($log, '(?im)^\[Error').Count
        patchExceptions = [regex]::Matches($log, '(?i)(patch failed|MissingMethodException|TypeLoadException|HarmonyException)').Count
        mainPluginLoads = [regex]::Matches($log, 'Loading \[Localization Patch [0-9.]+\]').Count
        dropdownPluginLoads = [regex]::Matches($log, 'Loading \[LocalizationPatch Dropdown Addon [0-9.]+\]').Count
        successfulPatchCount = @([regex]::Matches($log, 'Harmony: ([0-9]+) patches applied successfully') | ForEach-Object { [int]$_.Groups[1].Value })
        fastScanErrors = [regex]::Matches($log, 'Fast TMP scan error:').Count
        textScanErrors = [regex]::Matches($log, 'Text scan error:').Count
    }
}
$manifestPath = Join-Path (Split-Path (Split-Path $gameRoot -Parent) -Parent) 'appmanifest_2168680.acf'
$build = $null
if (Test-Path -LiteralPath $manifestPath) {
    $match = [regex]::Match([IO.File]::ReadAllText($manifestPath), '"buildid"\s+"(\d+)"')
    if ($match.Success) { $build = $match.Groups[1].Value }
}
New-Item -ItemType Directory -Path $outputRoot | Out-Null
[ordered]@{
    build = $build; hashes = $hashes; plugins = $pluginMetadata; log = $logSummary
    fields = $fields; methods = $methods; literals = $literals
} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $outputRoot 'metadata.json') -Encoding UTF8
Write-Output "Read-only evidence: $outputRoot; build=$build; methods=$($methods.Count); literals=$($literals.Count)"
