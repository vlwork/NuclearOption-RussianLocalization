[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$GameAssembly,
    [Parameter(Mandatory = $true)][string]$CecilPath,
    [Parameter(Mandatory = $true)][string]$OutputDirectory
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
. (Join-Path $projectRoot 'scripts\common.ps1')
$outputRoot = Assert-PathUnderRoot -Path $OutputDirectory -Root (Join-Path $projectRoot '.verification')
Assert-NoReparsePoint $outputRoot
if (Test-Path -LiteralPath $outputRoot) { throw 'Use a new verification directory; existing evidence is never overwritten.' }
$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'config\mission-messages.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$assemblyHash = (Get-FileHash -LiteralPath $GameAssembly -Algorithm SHA256).Hash
if ($assemblyHash -cne $manifest.assemblySha256) { throw 'Game assembly differs from the reviewed provenance. Re-review before patching.' }

# Metadata/IL only: Cecil does NOT execute the game assembly / DLL игры не выполняется.
Add-Type -Path $CecilPath
$assembly = [Mono.Cecil.AssemblyDefinition]::ReadAssembly($GameAssembly)
function Get-MissionTypes($types) {
    foreach ($type in $types) { $type; Get-MissionTypes $type.NestedTypes }
}
try {
    $types = @(Get-MissionTypes $assembly.MainModule.Types)
    $selected = @{
        'MissionMessages' = @('ShowMessage', 'ShowMessgeLocal', 'RpcShowMessage', 'IsLocalFaction', 'UserCode_RpcShowMessage_-186615428', 'Skeleton_RpcShowMessage_-186615428')
        'MessageManager' = @('JoinMessage', 'DisconnectedMessage', 'HQMessageInternal', 'UserCode_RpcAllHQMessage_913698537', 'UserCode_RpcHQMessage_324162117')
        'NuclearOption.Networking.Player' = @('ShowJoinMessage', 'OnStopClient')
        'NuclearOption.Chat.ChatManager' = @('SendChatMessage', 'UserCode_TargetReceiveMessage_1307761090', 'UserCode_RpcServerMessage_1244201393')
        'ChatBox' = @('SendChat')
        'GameplayUI' = @('GameMessage')
        'MessageUI' = @('GameMessage')
        'MessageFeed' = @('Enqueue', 'RefreshUI')
        'NuclearOption.SavedMission.Outcomes.ShowMessageOutcome' = @('Load', 'Complete')
    }
    $methods = @()
    $callers = @()
    $displayReferences = @()
    foreach ($type in $types) {
        foreach ($method in $type.Methods | Where-Object HasBody) {
            if ($selected.ContainsKey($type.FullName) -and $method.Name -in $selected[$type.FullName]) {
                $methods += [ordered]@{
                    type = $type.FullName; name = $method.Name; signature = $method.FullName
                    attributes = $method.Attributes.ToString()
                    parameters = @($method.Parameters | ForEach-Object { [ordered]@{ name = $_.Name; type = $_.ParameterType.FullName } })
                    il = @($method.Body.Instructions | ForEach-Object { $_.ToString() })
                }
            }
            foreach ($instruction in $method.Body.Instructions) {
                $operand = $instruction.Operand
                if ($operand -is [Mono.Cecil.MethodReference] -and (
                    ($operand.DeclaringType.FullName -eq 'MissionMessages' -and $operand.Name -in @('ShowMessage', 'ShowMessgeLocal')) -or
                    ($operand.DeclaringType.FullName -eq 'GameplayUI' -and $operand.Name -eq 'GameMessage'))) {
                    $callers += [ordered]@{ caller = $method.FullName; instruction = $instruction.ToString() }
                }
                if ($operand -is [Mono.Cecil.FieldReference] -and (
                    ($operand.DeclaringType.FullName -eq 'MessageFeed' -and $operand.Name -eq '_display') -or
                    ($operand.DeclaringType.FullName -eq 'MessageUI' -and $operand.Name -eq 'messageText'))) {
                    $displayReferences += [ordered]@{ method = $method.FullName; instruction = $instruction.ToString() }
                }
            }
        }
    }
    $localType = $types | Where-Object FullName -ceq 'MissionMessages'
    $local = @($localType.Methods | Where-Object Name -ceq 'ShowMessgeLocal')
    if ($local.Count -ne 1 -or -not $local[0].IsPrivate -or $local[0].IsStatic -or
        $local[0].ReturnType.FullName -cne 'System.Void' -or
        (($local[0].Parameters | ForEach-Object { $_.ParameterType.FullName }) -join ',') -cne 'System.String,System.Boolean,FactionHQ') {
        throw 'The exact private local display-producer signature is not proven.'
    }
    $allowedCalls = @('MissionMessages::IsLocalFaction', 'GameplayUI::GameMessage', 'MissionMessages::PlaySound')
    foreach ($instruction in $local[0].Body.Instructions) {
        if ($instruction.OpCode.Name -match '^(stfld|stsfld|starg|stobj|stind|calli)') { throw 'Unexpected state/argument write in local producer.' }
        if ($instruction.Operand -is [Mono.Cecil.MethodReference]) {
            $called = $instruction.Operand.DeclaringType.FullName + '::' + $instruction.Operand.Name
            if ($called -cnotin $allowedCalls) { throw "Unexpected local producer call: $called" }
        }
    }
    $localCallers = @($callers | Where-Object { $_.instruction -match 'call.*MissionMessages::ShowMessgeLocal\(' })
    if ($localCallers.Count -ne 2 -or
        -not ($localCallers.caller -match '^System.Void MissionMessages::ShowMessage\(') -or
        -not ($localCallers.caller -match '^System.Void MissionMessages::UserCode_RpcShowMessage_')) {
        throw 'Local producer is shared by an unreviewed caller.'
    }
    $result = [ordered]@{
        assemblySha256 = $assemblyHash
        decision = 'SAFE_TO_PATCH_REVIEWED_LOCAL_MISSION_DISPLAY_ARGUMENT_ONLY'
        methods = $methods; callers = $callers; displayFieldReferences = $displayReferences
        limits = @('Pinned local build only; no Unity/game code executed.', 'Chat/HQ/join/leave/final feed are NOT patched.', 'Host/client IL is static evidence; live multiplayer testing remains required.')
    }
    New-Item -ItemType Directory -Path $outputRoot | Out-Null
    $result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $outputRoot 'producer-evidence.json') -Encoding UTF8
    $lines = foreach ($method in $methods) { 'METHOD ' + $method.signature; $method.il; '' }
    $lines | Set-Content -LiteralPath (Join-Path $outputRoot 'producer-evidence.il.txt') -Encoding UTF8
    Write-Output ('PASS: exact private local producer and its two callers verified; ' + $methods.Count + ' method bodies recorded.')
    Write-Output $outputRoot
} finally { $assembly.Dispose() }
