# Third-party notices

## LocalizationPatch

- Source: https://github.com/9138noms/NuclearOption-LocalizationPatch
- Author/maintainer: 9138noms
- Use: basis of `LocalizationPatch.dll` and `LocalizationPatchDropdown.dll`
- Notice: upstream permits reuse and adaptation for Nuclear Option mods with attribution. No formal license file was present when this project was prepared.

## Russian translation

- Upstream patch: https://github.com/9138noms/NuclearOption-RussianPatch
- Credited translation contributors: Shumatsu [UMA], Jonyx2, and хомяк
- This repository preserves the current local 3,716-entry `ru.json` as the canonical translation file.

## Tektur

- File: `fonts/Tektur-Reg.ttf`
- Project: https://github.com/hyvyys/Tektur
- License: SIL Open Font License 1.1
- License text: https://openfontlicense.org/open-font-license-official-text/

## Build-time/runtime dependencies not redistributed

The project references BepInEx, Harmony, Unity, TextMesh Pro, and Nuclear Option assemblies from the local game installation through `NuclearOptionDir`. None of those DLLs is committed or packaged by this repository.
