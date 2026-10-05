# Nuclear Option Russian Localization

A standalone, maintainable BepInEx 5 localization mod for **Nuclear Option**. This repository contains `LocalizationPatch` 3.6.4 development-candidate source, the Russian translation data, the Cyrillic font, offline build/package scripts, and no game binaries. It preserves the 3.6.3 stabilization and adds producer-scoped localization of 13 reviewed mission messages before feed composition. Join/leave notices and chat are not intercepted; in-game host/client testing is required.

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
- `localization/ru.json` — canonical Russian translation, exactly 3,729 entries
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
.\scripts\package.ps1 -Version 3.6.4
```

This creates `release/NuclearOption-RussianLocalization-v3.6.4.zip`. The archive contains exactly four runtime files under `BepInEx/plugins/LocalizationPatch` plus six license, attribution, and provenance documents at archive level. Packaging runs the same strict QA as the build, checks the source/DLL version, and validates every archived file by path and hash. Previous local packages are retained under ignored `.verification/previous-packages` rather than deleted.

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

## Licensing and attribution

This is a mixed-license repository.

- Eligible repository-authored scripts, QA tools, runtime modifications, and documentation are offered under the [MIT License](LICENSE-CODE). MIT does not relicense inherited plugin code.
- Identifiable repository-authored Russian translation contributions are offered under [Creative Commons Attribution 4.0 International](LICENSE-TRANSLATION). This does not license the complete `ru.json`, inherited translations, or English game text.
- `LocalizationPatch` and `LocalizationPatchDropdown` are derived from [9138noms/NuclearOption-LocalizationPatch](https://github.com/9138noms/NuclearOption-LocalizationPatch). Its upstream permission and pending clarification are documented without describing the inherited code as MIT.
- The Russian translation is historically based on [9138noms/NuclearOption-RussianPatch](https://github.com/9138noms/NuclearOption-RussianPatch). Preserve credit to Shumatsu [UMA], Jonyx2, and хомяк.
- Tektur is Copyright 2023 The Tektur Project Authors, was designed by Adam Jagosz, and remains under the SIL Open Font License 1.1.
- Nuclear Option game text and other game-originating material remain the property of Shockfront Studios Pty Ltd or its licensors and are not licensed by this repository.

See the [license scope](LICENSE.md), [third-party notices](THIRD_PARTY_NOTICES.md), and [translation provenance](localization/PROVENANCE.md) for the exact boundaries and pending questions.

## Release policy

The repository is prepared for a GitHub Release, but scripts do not publish, upload, create a GitHub release, or create a Steam Workshop item.
