# Release output

Run `..\scripts\package.ps1 -Version 3.6.4` from the repository root to generate:

`NuclearOption-RussianLocalization-v3.6.4.zip`

The archive contains exactly 12 entries:

- four runtime files under `BepInEx/plugins/LocalizationPatch`;
- `Install.ps1` and `Install.cmd` at archive root;
- `LICENSE.md`, `LICENSE-CODE`, `LICENSE-TRANSLATION`, and `THIRD_PARTY_NOTICES.md` at archive root;
- `third_party/OFL-1.1.txt` and `localization/PROVENANCE.md` at matching archive paths.

For normal Windows installation, extract the archive and run `Install.cmd`. The installer locates Nuclear Option, requires an existing BepInEx 5 installation, creates a recoverable backup outside the BepInEx tree, relocates duplicate localization assemblies, and copies only the four runtime files into the active plugin directory. Legal/provenance documents and installer files remain package-level material and are never installed under `BepInEx/plugins`.

Generated ZIP files are intentionally ignored by git. The packaging script validates localization invariants, exact archive entry count and paths, and embedded file hashes before reporting SHA256.
