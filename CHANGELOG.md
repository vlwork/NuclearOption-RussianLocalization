# Changelog

## 3.6.4 — 2026-10-03 (development candidate)

- Added 13 reviewed static Reprisal mission messages (3,716 → 3,729 entries), preserving all existing values and K92/PALA/proper names.
- Localize those exact messages at `MissionMessages.ShowMessgeLocal` before feed composition; leave mission identifiers, original network text, sound and faction filtering untouched.
- Player join/leave notifications remain English; no chat interception, final-feed matching, new scans or AutoFit/layout changes. Mission Editor, hints and cockpit/HUD/MFD coverage remain outside this pass.
- Requires in-game host/client testing; not published or installed into the real game.

## 3.6.3 — 2026-10-03

- Normalized only 16 reviewed boundary-whitespace keys; preserved their values, all 3,716 entries, and all four trim collision groups.
- Corrected 23 reviewed values: restored `T9K41 Boltstrike`, clarified loadout/AAA/naval/launcher terminology, and corrected ordinary Encyclopedia unit typography. Ambiguous and deferred editor/mission/avionics findings remain.
- Removed unconditional FrameHelper keypress diagnostics only; preserved 3.6.0 translation timing, shortcuts, OnEnable hooks and selective text-only AutoFit.
- Added shared deterministic offline localization QA and regression tests; refreshed the remaining 112-key trim analysis.
- Made build/package verification offline and repository-isolated; validate the exact four-file production archive and source/DLL version.
- Moved installer backups outside all BepInEx, identify duplicates by assembly metadata, preserve user files, and support `-WhatIf`; verified only against repository-local mock games.
- No publication or real-game installation performed; in-game user testing remains required.

## 3.6.0 — 2026-08-26

- Restored the verified stable LocalizationPatch 3.6.0 implementation from the installed known-good DLL and upstream source.
- Preserved TMP setter interception and `OnEnable` prefix/postfix translation to avoid visible English flashes.
- Preserved the fast active-TMP translation pass and text-only selective AutoFit.
- Explicitly excluded the 3.6.1 parent-container resizing experiment.
- Explicitly excluded the 3.6.2 cockpit hierarchy scanner.
- Added canonical Russian `ru.json` with 3,716 entries and protected English countermeasure terms.
- Continue left untranslated because translating it can break/delay dismissal of an in-mission UI overlay.
- Preserved the ASCII `A-19`, `M12 Jackknife`, and `T/A-30` designations in Russian localization entries.
- Added reproducible build, package, validation, and backup-first local installation scripts.
- Added release-ready English and Russian documentation and third-party notices.
