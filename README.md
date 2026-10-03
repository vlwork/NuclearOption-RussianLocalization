# Nuclear Option Russian Localization

A standalone, maintainable BepInEx 5 localization mod for **Nuclear Option**. This repository contains `LocalizationPatch` 3.6.3 source, the Russian translation data, the Cyrillic font, offline build/package scripts, and no game binaries. Version 3.6.3 preserves the stable 3.6.0 translation behavior and removes only unconditional keypress diagnostic logging; it requires an in-game user test.

The runtime plugin is based on [9138noms/NuclearOption-LocalizationPatch](https://github.com/9138noms/NuclearOption-LocalizationPatch). Stable 3.6.0 behavior is intentionally preserved:

- TMP text is translated before it visibly flashes in English;
- both prefix and postfix hooks cover `OnEnable`;
- a fast active-TMP pass supplements the slower safety sweep;
- selective AutoFit changes only TMP text sizing;
- parent `RectTransform` and layout containers are never resized or repositioned.

The experimental 3.6.1/3.6.2 binaries and the 3.6.2 cockpit hierarchy scanner are not used.

## Repository layout

- `src/LocalizationPatch` — main BepInEx plugin (`com.noms.localizationpatch`)
- `src/LocalizationPatchDropdown` — dropdown translation addon
- `localization/ru.json` — canonical Russian translation, exactly 3,716 entries
- `fonts/Tektur-Reg.ttf` — Cyrillic fallback font
- `scripts` — build, package, and local installation scripts
- `release` — generated GitHub Release ZIP location

## Build

Requirements: Windows PowerShell 5.1+, Python 3.10+ (standard library only), a .NET SDK with locally available .NET Framework 4.7.2 targeting support, Nuclear Option, and BepInEx 5 installed in the game directory. Restore uses an empty local feed and disables NuGet auditing: missing build dependencies fail rather than being downloaded.

```powershell
.\scripts\build.ps1
```

If local execution policy blocks scripts, run `powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1`.

The script searches Steam libraries automatically. An explicit path can be supplied:

```powershell
.\scripts\build.ps1 -GameDir 'G:\SteamLibrary\steamapps\common\Nuclear Option'
```

All game references flow through the MSBuild `NuclearOptionDir` property. Game DLLs are never copied into the repository or release.

## Package

```powershell
.\scripts\package.ps1 -Version 3.6.3
```

This creates `release/NuclearOption-RussianLocalization-v3.6.3.zip` with the `BepInEx/plugins/LocalizationPatch` layout. Packaging runs the same strict QA as the build, checks the source/DLL version, and validates exactly four archive entries (two plugin DLLs, `ru.json`, and Tektur), including their hashes. Previous local packages are retained under ignored `.verification/previous-packages` rather than deleted.

For isolated verification, pass a repository-local absolute path to `build.ps1 -OutputRoot`, then use that same path with `package.ps1 -SkipBuild -BuildRoot` and a repository-local `-OutputDirectory`.

## Offline QA and installer tests

```powershell
.\scripts\audit-localization.ps1
.\scripts\audit-localization.ps1 -Strict
python .\tools\test-localization-qa.py
.\scripts\install-local.ps1 -GameDir '<game folder>' -WhatIf
```

QA is read-only toward localization and runtime files. `config/localization-audit.json` contains identities, designation rules, contextual proper names and review candidates. Strict mode fails objective invariants, not trim/style/context warnings. See `reports/localization-audit.md`, `reports/trim-safety-analysis.md`, and `reports/stabilization-report.md` for reviewed and remaining findings. Coverage is unknown without a local extracted source snapshot.

`scripts/test-installer.ps1 -BuildRoot '<isolated build root>'` exercises only newly created repository-local mock games. Verification trees, recovery snapshots and binaries are ignored; intended reports and configuration are not.

For player-facing installation and limitations, see [README_RU.md](README_RU.md).

## Translation policy

Model designations and proper vehicle/aircraft/weapon/unit names and codenames remain in their original English spelling, including inside descriptions. Generic nouns such as vessel types and launchers may be translated naturally. `IR Flares`, `Radar Countermeasures`, `Continue`, and `M12 Jackknife` are exact protected identities. General menus, Encyclopedia content, and ordinary UI are translated through `ru.json`. Mission Editor, mission hints, and cockpit/HUD/MFD remain intentionally incomplete; this pass does not expand those areas.

## Release policy

The repository is prepared for a GitHub Release, but scripts do not publish, upload, create a GitHub release, or create a Steam Workshop item.
