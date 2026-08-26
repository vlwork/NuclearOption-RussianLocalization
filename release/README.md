# Release output

Run `..\scripts\package.ps1 -Version 3.6.0` from the repository root to generate:

`NuclearOption-RussianLocalization-v3.6.0.zip`

Generated ZIP files are intentionally ignored by git. The packaging script validates translation invariants, active DLL count, forbidden backup files, and forbidden experimental version filenames before reporting SHA256.
