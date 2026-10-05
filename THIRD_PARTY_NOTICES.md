# Third-party notices

This repository contains inherited and third-party material that is not covered by the repository's MIT or CC BY 4.0 grants except where explicitly stated.

## LocalizationPatch and LocalizationPatchDropdown

- Upstream source: https://github.com/9138noms/NuclearOption-LocalizationPatch
- Original author/maintainer: 9138noms
- Local paths: `src/LocalizationPatch` and `src/LocalizationPatchDropdown`
- Distributed binaries: `LocalizationPatch.dll` and `LocalizationPatchDropdown.dll`
- Upstream licensing status: the upstream repository currently has no standard `LICENSE` file. Its README welcomes reuse and adaptation for Nuclear Option mods with credit to the original.

That README permission is informal and is **not** represented here as MIT. Repository-authored modifications do not relicense the inherited source. Clarification of the upstream reuse terms is pending.

## Russian translation

- Upstream source: https://github.com/9138noms/NuclearOption-RussianPatch
- Local file: `localization/ru.json`
- Current entry count: 3,729
- Credited inherited translation contributors:
  - Shumatsu [UMA]
  - Jonyx2
  - хомяк

The historical Russian translation has mixed provenance, and a complete per-entry authorship boundary has not been established. The repository's CC BY 4.0 grant applies only to identifiable repository-authored Russian contributions, not to every entry. Clarification of the inherited translation reuse terms is pending. See `localization/PROVENANCE.md`.

## Tektur

- Bundled file: `fonts/Tektur-Reg.ttf`
- Upstream project: https://github.com/hyvyys/Tektur
- Copyright: Copyright 2023 The Tektur Project Authors (https://www.github.com/hyvyys/Tektur)
- Designer: Adam Jagosz
- License: SIL Open Font License 1.1
- License text: `third_party/OFL-1.1.txt`

The font is not covered by this repository's MIT or CC BY 4.0 grants.

## Nuclear Option

Nuclear Option, including English interface keys, mission messages, Encyclopedia and lore text, and other game-originating material, remains the property of Shockfront Studios Pty Ltd or its licensors. This repository does not license that material under MIT or CC BY 4.0 and does not claim ownership of it.

## Build-time and runtime dependencies not redistributed

The project references BepInEx, Harmony, Unity, TextMesh Pro, and Nuclear Option assemblies from the local game installation through `NuclearOptionDir`. Those dependency DLLs are not committed or included in release archives by this repository.
