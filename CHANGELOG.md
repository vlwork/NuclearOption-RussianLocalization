# Changelog

## 3.6.0 — 2026-08-26

- Restored the verified stable LocalizationPatch 3.6.0 implementation from the installed known-good DLL and upstream source.
- Preserved TMP setter interception and `OnEnable` prefix/postfix translation to avoid visible English flashes.
- Preserved the fast active-TMP translation pass and text-only selective AutoFit.
- Explicitly excluded the 3.6.1 parent-container resizing experiment.
- Explicitly excluded the 3.6.2 cockpit hierarchy scanner.
- Added canonical Russian `ru.json` with 3,716 entries and protected English countermeasure terms.
- Added reproducible build, package, validation, and backup-first local installation scripts.
- Added release-ready English and Russian documentation and third-party notices.
