# Release output

Run `..\scripts\package.ps1 -Version 3.6.4` from the repository root to generate:

`NuclearOption-RussianLocalization-v3.6.4.zip`

The archive contains:

- exactly four runtime files under `BepInEx/plugins/LocalizationPatch`;
- `LICENSE.md`, `LICENSE-CODE`, `LICENSE-TRANSLATION`, and `THIRD_PARTY_NOTICES.md` at archive root;
- `third_party/OFL-1.1.txt` and `localization/PROVENANCE.md` at matching archive paths.

The installer continues to copy only the four runtime files into the active plugin directory. Legal documentation remains package-level material.

Generated ZIP files are intentionally ignored by git. The packaging script validates localization invariants, active DLL count, forbidden backup files, forbidden experimental version filenames, exact archive paths, and embedded file hashes before reporting SHA256.
