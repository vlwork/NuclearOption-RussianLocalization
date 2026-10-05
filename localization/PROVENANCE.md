# Russian localization provenance

This document records the known provenance and current licensing boundary for `localization/ru.json`.

## Known sources and contributors

- Historical upstream repository: https://github.com/9138noms/NuclearOption-RussianPatch
- Credited inherited translation contributors:
  - Shumatsu [UMA]
  - Jonyx2
  - хомяк
- Current local entry count: 3,729

The English keys include interface text, mission messages, Encyclopedia descriptions, lore, and other source strings originating from Nuclear Option. Those strings remain the property of Shockfront Studios Pty Ltd or its licensors and are not licensed by this repository.

## Mixed historical authorship

The Russian values combine inherited translations with later corrections and additions made in this repository. A complete per-entry historical authorship boundary is not currently available. In particular, the local import does not identify a reliable upstream `NuclearOption-RussianPatch` commit for every inherited entry, so no upstream commit hash is asserted here.

The Creative Commons Attribution 4.0 International license in `../LICENSE-TRANSLATION` applies only where repository authorship of a Russian translation contribution can be established. It does not relicense inherited translations or English game text. Clarification from the upstream translation contributors is pending.

## Verifiable local boundaries

- `0becbf1` introduced the local 3,716-entry canonical `ru.json` together with the stable 3.6.0 release preparation. The file was already of mixed historical provenance at import.
- `8594a28` added localization safeguards and trim-safety work, including reviewed localization changes.
- `fde844a` recorded the 3.6.3 stabilization: 16 reviewed boundary-whitespace key normalizations and 23 reviewed value corrections while retaining 3,716 entries.
- `8046c91` added 13 reviewed Russian mission-message translations, increasing the count from 3,716 to 3,729.

These commit boundaries document local changes, not ownership of unchanged or previously imported entries.

## Attribution and future updates

Redistributions should preserve attribution to 9138noms, Shumatsu [UMA], Jonyx2, and хомяк, identify modifications where practical, and retain `../THIRD_PARTY_NOTICES.md`. Future externally sourced translations must record their source, author, and permission before inclusion.
