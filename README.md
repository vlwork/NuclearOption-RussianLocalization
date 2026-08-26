# Nuclear Option Russian Localization

A standalone, maintainable BepInEx 5 localization mod for **Nuclear Option**. This repository contains the stable `LocalizationPatch` 3.6.0 source, the Russian translation data, the Cyrillic font, reproducible build/package scripts, and no game binaries.

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

Requirements: Windows PowerShell 5.1+, a .NET SDK capable of targeting `net472`, Nuclear Option, and BepInEx 5 installed in the game directory.

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
.\scripts\package.ps1 -Version 3.6.0
```

This creates `release/NuclearOption-RussianLocalization-v3.6.0.zip` with the ready-to-install `BepInEx/plugins/LocalizationPatch` layout. Packaging validates `ru.json`, protected English countermeasure/unit names and model designations, the active DLL count, and the absence of backups or experimental files.

For player-facing installation and limitations, see [README_RU.md](README_RU.md).

## Translation policy

Vehicle, aircraft, weapon, and unit names remain in their original English spelling, including inside descriptions. `IR Flares` and `Radar Countermeasures` are protected identity translations. General menus, Encyclopedia content, and ordinary UI are translated through `ru.json`. The mod does not attempt to translate every cockpit/HUD/MFD element automatically.

## Release policy

The repository is prepared for a GitHub Release, but scripts do not publish, upload, create a GitHub release, or create a Steam Workshop item.
