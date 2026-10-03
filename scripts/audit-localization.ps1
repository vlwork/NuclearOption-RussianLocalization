[CmdletBinding()]
param(
    [switch]$Strict,
    [string]$LocalizationPath,
    [string]$ReportPath,
    [string]$JsonReportPath,
    [string]$ExtractedGameDataPath,
    [string]$UntranslatedPath
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$arguments = @((Join-Path $projectRoot 'tools\audit-localization.py'))
if ($Strict) { $arguments += '--strict' }
foreach ($pair in @(
    @('--localization', $LocalizationPath), @('--report', $ReportPath),
    @('--json-report', $JsonReportPath), @('--extracted', $ExtractedGameDataPath),
    @('--untranslated', $UntranslatedPath)
)) {
    if ($pair[1]) { $arguments += $pair }
}
# Python's standard library only: offline / только стандартная библиотека, без сети.
& python @arguments
exit $LASTEXITCODE
