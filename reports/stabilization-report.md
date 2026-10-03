# Full localization stabilization / recovery report

## Recovery

Original and current HEAD: `8594a28b36572b2393921bee26346bcdd4cc82a1`. Local branch: `fix/full-localization-stabilization`. HEAD equals baseline `8594a28b36572b2393921bee26346bcdd4cc82a1`. No reset, checkout, stash, commit, push or publication occurred.

Current dirty work was preserved in ignored `.verification/recovery-20261003-132301` before further edits. No localization value/key was changed during the resume; its recovery and final SHA256 are identical. The rejected package/trim patches were confirmed absent before targeted fixes.

### Initial dirty-file inventory

| Path | Status | Existed at baseline | Purpose / initial completeness |
|---|---|---|---|
| .gitignore |  M | True | Complete: ignore recovery/verification and Python caches only. |
| localization/ru.json |  M | True | Complete: 16 reviewed renames / 23 reviewed values; independently reverified. |
| scripts/build.ps1 |  M | True | Present: offline restore and isolated source-only build; needed fresh validation. |
| scripts/common.ps1 |  M | True | Present: one shared QA validator, version/file manifest and path safety; needed review. |
| scripts/install-local.ps1 |  M | True | In progress: external backups, duplicate metadata, dry-run and rollback; not yet mock-tested. |
| scripts/package.ps1 |  M | True | Interrupted: exact manifest/hash validation, but missing compression assembly and incompatible timestamp-after-write ordering. |
| src/LocalizationPatch/LocalizationPatch.csproj |  M | True | Complete: 3.6.3 assembly/package metadata. |
| src/LocalizationPatch/Plugin.cs |  M | True | Complete: four diagnostic guards removed, three version labels updated; behavior proof rerun. |
| config/localization-audit.json | ?? | False | Present: maintainable invariants/glossary/context configuration. |
| config/stabilization-changes.json | ?? | False | Complete: explicitly reviewed value-change manifest and reasons. |
| scripts/audit-localization.ps1 | ?? | False | Present: Windows entry point into one Python QA engine. |
| tools/audit-localization.py | ?? | False | Present: deterministic stdlib QA; runtime-export parser/regression tests still needed. |
| tools/stabilize-localization.py | ?? | False | Complete: guarded reviewed-phase mechanics / structured verifier; no reapplication on resume. |

At recovery, README/README_RU/CHANGELOG and the existing trim report/tool were unchanged; trim reporting was stale and failed with `Expected 128 ... found 112`. They were then updated only to reflect verified behavior/current findings.

### Recovery-time SHA256

| Path | SHA256 |
|---|---|
| localization\ru.json | `878E1B61CC21A11BE6D4D18DDE0DCD7394A3D9622E82A7ED6AD375B750DBD1A7` |
| src\LocalizationPatch\Plugin.cs | `646D262BEE2EEAAD2CB4A3CB1AEF7660B526379EFE7A9F3CC92EC0F0D20BE789` |
| src\LocalizationPatchDropdown\Plugin.cs | `5C673F1D5C21FB0E24D8D66EFC494CB6D9D3D85A1085818976937F2734EB1214` |
| scripts\install-local.ps1 | `9A7399AE62B79585C3A552A067AEEC987D458B8BA09E5FF62C1DF7B0E7AA8968` |
| scripts\package.ps1 | `2BE876FA8D7C819983B5884497443A755E809581D3B5AE7F8F6A78432C0FBB65` |
| tools\analyze-trim-safety.py | `B098F796CF58E908109945900E7588577C6E8FF14356521F64E7C79D0AC81A44` |
| src\LocalizationPatch\bin\Release\net472\LocalizationPatch.dll | `5151D80A92179F9A3CF8C923CC049C91A3D17DCFA722F872D3E8865568FB21ED` |
| src\LocalizationPatchDropdown\bin\Release\net472\LocalizationPatchDropdown.dll | `A25EE2670B1F2699B0702A90FEC2241E99A5CA4F4E27A2EAC26257CF8B84122A` |
| release\NuclearOption-RussianLocalization-v3.6.0.zip | `BD2A38F976D60865CB38D3A98923181CA84B44E64BCE39A9280A4EEB9CD0FF30` |
| .verification\isolated build\src\LocalizationPatch\bin\Release\net472\LocalizationPatch.dll | `88B4980D2A0591F7BB2FED8B93433CEC1296DA2253D515A8B3A49A2816BD9795` |
| .verification\isolated build\src\LocalizationPatchDropdown\bin\Release\net472\LocalizationPatchDropdown.dll | `C9F02C68A7106CFBF9711C7BB483DB1096B5B2BFF1BDE74A8EA85F8432A1DB26` |

## Localization / independent Git comparison

Entries: 3716 → 3716. Key renames: 16. Logical additions/removals: 0/0. Changed values: 23. Unchanged exact-key/value entries: 3677. A raw set difference contains 16 old names and 16 new names, all accounted for as renames. Unexplained differences: 0.

All 23 existing changes passed second-pass linguistic/technical review: 1 OBJECTIVE_FIX and 22 CLEAR_RUSSIAN_IMPROVEMENT. None was QUESTIONABLE or OUT_OF_SCOPE; no individual reversion or further translation change was needed.

### Complete changed-value table

| Source | Baseline Russian value | Current Russian value | Second-pass classification / reason |
|---|---|---|---|
| "T9K41 Boltstrike" | "Т9К41 Болтстрайк" | "T9K41 Boltstrike" | OBJECTIVE_FIX: Restore exact ASCII model code and proper name, including in deferred areas. |
| "1 FORWARD BAY" | "1 ПЕРЕДНИЙ ОТКРЫТЫЙ" | "1 ПЕРЕДНИЙ ОТСЕК" | CLEAR_RUSSIAN_IMPROVEMENT: Bay is a compartment, not the adjective open; existing Forward Weapon Bay confirms terminology. |
| "3 HEATER BAYS" | "3 ОТСЕКА НАГРЕВАТЕЛЯ" | "3 ОТСЕКА ДЛЯ ИК-РАКЕТ" | CLEAR_RUSSIAN_IMPROVEMENT: Existing KR-67 Ifrit description explicitly defines heater bays as IRM-S2 compartments. |
| "Forward Bay" | "Форвард Бэй" | "Передний отсек" | CLEAR_RUSSIAN_IMPROVEMENT: Generic loadout compartment; existing Forward Weapon Bay provides context, not a codename. |
| "Rear Bay" | "Задний залив" | "Задний отсек" | CLEAR_RUSSIAN_IMPROVEMENT: Generic loadout compartment, not a geographical bay; existing Rear Weapon Bay provides context. |
| "Heater Bays" | "Нагревательные отсеки" | "Отсеки для ИК-ракет" | CLEAR_RUSSIAN_IMPROVEMENT: Existing Ifrit description explicitly explains the same heater-bay term. |
| "23mm AAA Emplacement" | "расположение 23мм ПВО" | "23-мм зенитная установка" | CLEAR_RUSSIAN_IMPROVEMENT: AAA is anti-aircraft artillery; emplacement names the installation, not its location. Adjectival calibre typography. |
| "Dynamo Class Destroyer" | "Dynamo Class Destroyer" | "Эсминец класса Dynamo" | CLEAR_RUSSIAN_IMPROVEMENT: Translate generic vessel type and class wording; preserve Dynamo. |
| "MSV R9 Stratolance Launcher" | "MSV R9 Stratolance Launcher" | "Пусковая установка MSV R9 Stratolance" | CLEAR_RUSSIAN_IMPROVEMENT: Translate generic launcher noun; preserve MSV, R9 and Stratolance. |
| "20mm cannon firing explosive shells at a lower rate of fire than its rotary counterpart." | "20мм пушка, стреляющая осколочно-фугасными снарядами с более низкой скорострельностью, чем её роторный аналог." | "20-мм пушка, стреляющая осколочно-фугасными снарядами с более низкой скорострельностью, чем её роторный аналог." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre in ordinary Encyclopedia prose; no code or telemetry changed. |
| "A heavy forward fixed cannon, firing 57mm multi-purpose warheads at 250rpm. Automatically adjusts fuzing type and timing according to target parameters." | "Тяжёлое неподвижное носовое орудие, стреляющее 57мм многоцелевыми боеголовками со скоростью 250 выстр./мин. Автоматически настраивает тип и время срабатывания взрывателя в соответствии с параметрами цели." | "Тяжёлое неподвижное носовое орудие, стреляющее 57-мм многоцелевыми снарядами со скоростью 250 выстр./мин. Автоматически настраивает тип и время срабатывания взрывателя в соответствии с параметрами цели." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre and correct cannon projectile terminology; fuzing and rate unchanged. |
| "Allowing a traverse range from -10 to +10 degrees and an elevation range from -20 to +5 degrees, this aimable cannon pod is effective against light armor or aircraft at distances of up to 2000m." | "С углами горизонтальной наводки от -10 до +10 градусов и вертикальной от -20 до +5 градусов, эта наводимая пушечная гондола эффективна против лёгкой брони или самолётов на дальностях до 2000м." | "С углами горизонтальной наводки от -10 до +10 градусов и вертикальной от -20 до +5 градусов, эта наводимая пушечная гондола эффективна против лёгкой брони или самолётов на дальностях до 2000 м." | CLEAR_RUSSIAN_IMPROVEMENT: Separate numeric distance and unit in ordinary prose. |
| "An autoloaded 76mm gun, firing fin-stabilised guided projectiles. The gun requires airflow for cooling. It has a maximum firerate of 60RPM for 10 seconds, and can sustain a constant firerate of at least 40 RPM while moving at 500kph" | "Автоматическое 76мм орудие, стреляющее оперёнными управляемыми снарядами. Для охлаждения требуется воздушный поток. Максимальная скорострельность — 60 выстр./мин в течение 10 секунд, устойчивая — не менее 40 выстр./мин при скорости 500 км/ч" | "Автоматическое 76-мм орудие, стреляющее оперёнными управляемыми снарядами. Для охлаждения требуется воздушный поток. Максимальная скорострельность — 60 выстр./мин в течение 10 секунд, устойчивая — не менее 40 выстр./мин при скорости 500 км/ч" | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre typography in ordinary prose. |
| "An fast firing, autoloaded 57mm gun, firing high velocity unguided shells. When fired against air targets, the shells use a proximity fuse to deal fragmentation damage." | "Скорострельное автоматическое 57мм орудие, стреляющее высокоскоростными неуправляемыми снарядами. При стрельбе по воздушным целям снаряды используют неконтактный взрыватель для нанесения осколочного урона." | "Скорострельное автоматическое 57-мм орудие, стреляющее высокоскоростными неуправляемыми снарядами. При стрельбе по воздушным целям снаряды используют неконтактный взрыватель для нанесения осколочного урона." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre typography in ordinary prose. |
| "Firing .50 caliber ammunition, the 12.7mm machine gun is effective against aircraft and lightly armored surface targets at ranges of up to 1km (0.61 miles)." | "Стреляя патронами .50 калибра, 12,7мм пулемёт эффективен против самолётов и легкобронированных наземных целей на дальностях до 1км (0,61 мили)." | "Стреляя патронами .50 калибра, 12,7-мм пулемёт эффективен против самолётов и легкобронированных наземных целей на дальностях до 1 км (0,61 мили)." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre and distance spacing; no numeric values changed. |
| "Occupying three structural hardpoints and weighing in at 1.6 tons loaded, this seven-barrelled, twin motor behemoth fires a mixed belt of 30mm armour piercing incendiary &amp; HE rounds at 3000rpm. Can be made effective against the majority of enemy vehicles, buildings, and slow moving aircraft." | "Занимая три силовых узла подвески и весом 1,6 тонны в снаряжённом состоянии, этот семиствольный двухмоторный гигант стреляет смешанной лентой из 30мм бронебойно-зажигательных и осколочно-фугасных снарядов со скоростью 3000 выстр./мин. Эффективен против большинства вражеской техники, зданий и тихоходных самолётов." | "Занимая три силовых узла подвески и весом 1,6 тонны в снаряжённом состоянии, этот семиствольный двухмоторный гигант стреляет смешанной лентой из 30-мм бронебойно-зажигательных и осколочно-фугасных снарядов со скоростью 3000 выстр./мин. Эффективен против большинства вражеской техники, зданий и тихоходных самолётов." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre typography in ordinary prose. |
| "Slower firing than its rotary counterparts, the 27mm Autocannon packs a heavier punch and is effective against both aircraft and moderately armored surface targets." | "Стреляя медленнее своих роторных аналогов, 27мм автопушка обладает большей мощностью и эффективна как против самолётов, так и против умеренно бронированных наземных целей." | "Стреляя медленнее своих роторных аналогов, 27-мм автопушка обладает большей мощностью и эффективна как против самолётов, так и против умеренно бронированных наземных целей." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre typography in ordinary prose. |
| "The 20mm rotary cannon fires dual purpose explosive shells, effective against aircraft or moderately armored surface targets." | "20мм роторная пушка стреляет осколочно-фугасными снарядами двойного назначения, эффективными против самолётов или умеренно бронированных наземных целей." | "20-мм роторная пушка стреляет осколочно-фугасными снарядами двойного назначения, эффективными против самолётов или умеренно бронированных наземных целей." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre typography in ordinary prose. |
| "The 25mm rotary cannon fires dual purpose explosive shells, effective against aircraft or moderately armored surface targets." | "25мм роторная пушка стреляет осколочно-фугасными снарядами двойного назначения, эффективными против самолётов или умеренно бронированных наземных целей." | "25-мм роторная пушка стреляет осколочно-фугасными снарядами двойного назначения, эффективными против самолётов или умеренно бронированных наземных целей." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre typography in ordinary prose. |
| "The 30mm rotary cannon fires large, dual purpose explosive shells, effective against armored surface targets." | "30мм роторная пушка стреляет крупными осколочно-фугасными снарядами двойного назначения, эффективными против бронированных наземных целей." | "30-мм роторная пушка стреляет крупными осколочно-фугасными снарядами двойного назначения, эффективными против бронированных наземных целей." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre typography in ordinary prose. |
| "The 35mm Autocannon packs a heavier punch than other aerial guns and is effective against many armored surface targets. Its superior ballistics allow it to remain effective at ranges exceeding 3000m." | "35мм автопушка обладает большей мощностью, чем другие авиапушки, и эффективна против многих бронированных наземных целей. Превосходная баллистика позволяет сохранять эффективность на дальностях свыше 3000м." | "35-мм автопушка обладает большей мощностью, чем другие авиапушки, и эффективна против многих бронированных наземных целей. Превосходная баллистика позволяет сохранять эффективность на дальностях свыше 3000 м." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre and distance spacing in ordinary prose. |
| "This gun shoots 30mm explosive shells effective against armored ground vehicles and buildings at ranges of over 2km (1.3m)." | "Эта пушка стреляет 30мм осколочно-фугасными снарядами, эффективными против бронированной наземной техники и зданий на дальностях свыше 2км (1,3 мили)." | "Эта пушка стреляет 30-мм осколочно-фугасными снарядами, эффективными против бронированной наземной техники и зданий на дальностях свыше 2 км (1,3 мили)." | CLEAR_RUSSIAN_IMPROVEMENT: Calibre/distance typography only; ambiguous source imperial-unit suffix is not reinterpreted. |
| "This rotary cannon fires 20mm explosive shells at 6000 rounds per minute, making it highly effective against aerial targets." | "Эта роторная пушка стреляет 20мм осколочно-фугасными снарядами со скоростью 6000 выстрелов в минуту, что делает её высокоэффективной против воздушных целей." | "Эта роторная пушка стреляет 20-мм осколочно-фугасными снарядами со скоростью 6000 выстрелов в минуту, что делает её высокоэффективной против воздушных целей." | CLEAR_RUSSIAN_IMPROVEMENT: Adjectival calibre typography in ordinary prose. |

### Complete key-rename list

Every row preserves the original translation exactly; only U+0020 boundary padding was removed, as authorized by the reviewed allowlist.

| Raw key (JSON) | New key (JSON) |
|---|---|
| " Objective needs a faction" | "Objective needs a faction" |
| " This text uses emojis, which have a different byte count." | "This text uses emojis, which have a different byte count." |
| "BUILDING REPAIRS COMPLETE " | "BUILDING REPAIRS COMPLETE" |
| "Can't multiselect " | "Can't multiselect" |
| "Custom Airbase " | "Custom Airbase" |
| "Hello, world! " | "Hello, world!" |
| "Mission Failed, no spawn points available " | "Mission Failed, no spawn points available" |
| "No reserve " | "No reserve" |
| "Test 1a Passed: Short string handled correctly. " | "Test 1a Passed: Short string handled correctly." |
| "Test 1b Passed: Short string handled correctly. " | "Test 1b Passed: Short string handled correctly." |
| "Test 2 Passed: Long string split into multiple chunks correctly. " | "Test 2 Passed: Long string split into multiple chunks correctly." |
| "Test 3 Passed: Long string correctly truncated to max length. " | "Test 3 Passed: Long string correctly truncated to max length." |
| "Test 4 Passed: String with special characters handled correctly. " | "Test 4 Passed: String with special characters handled correctly." |
| "Test 5 Passed: Japanese text correctly split into chunks under the 255-byte limit. " | "Test 5 Passed: Japanese text correctly split into chunks under the 255-byte limit." |
| "Test 6 Passed: Empty string handled correctly. " | "Test 6 Passed: Empty string handled correctly." |
| "WRECK REMOVAL " | "WRECK REMOVAL" |

### QA before / after

Both columns use the same final QA engine/configuration; they are not silently compared with historical, weaker scripts.

| Metric | Baseline | Final |
|---|---:|---:|
| EntryCount | 3716 | 3716 |
| DuplicateExactKeys | 0 | 0 |
| ProtectedIdentityViolations | 0 | 0 |
| TrimUnsafeKeys | 128 | 112 |
| TrimCollisions | 4 | 4 |
| DesignationViolations | 1 | 0 |
| ProperNameViolations | 1 | 0 |
| PlaceholderMismatches | 0 | 0 |
| TmpTagMismatches | 0 | 0 |
| NewlineMismatches | 2 | 2 |
| CaseVariantGroups | 189 | 189 |
| InconsistentCaseVariantGroups | 34 | 34 |
| TypographyWarnings | 18 | 3 |
| DynamicNoiseEntries | 12 | 12 |
| CRITICAL | 2 | 0 |
| HIGH | 132 | 116 |
| MEDIUM | 64 | 49 |
| INFO | 13 | 13 |

Normal audit exit: 0. Strict audit exit: 0. Invalid JSON, duplicates, count, protected identities, designations, proper names, placeholders and TMP all pass. Two baseline newline warnings remain unchanged; valid JSON decoding and the structured proof establish no new escaping/newline corruption.

The 49 MEDIUM rows include 34 case groups, 2 newline cautions, 3 deferred typography warnings and 10 curated review reminders (including correctly preserved names). HIGH=116 comprises 112 trim keys plus 4 collisions. INFO=13 comprises 12 dynamic literals and unavailable coverage. Coverage source/exact/normalized/missing counts are n/a because no real local extracted snapshot exists; test fixtures are excluded.

All protected identities remain exact. `A-19 factory` = `завод A-19`; `T/A-30 factory` = `завод T/A-30`; `T9K41 Boltstrike` and `M12 Jackknife` retain ASCII identity. A2A/A2G are documented mode abbreviations, not model-designation exemptions added to conceal a corruption. Vortex ring state is an aerodynamic exception, not the aircraft codename.

Trim: 128 → 112 unsafe; 4 → 4 collisions; 110 manual entries untouched, 2 redundant entries retained. Saved Mission conflict remains unresolved and unchanged: `Миссия сохранена:` versus `Сохраненная миссия:`. Other collision translations are equivalent and retained; static pattern sub-probes prevent a universal deadness claim. See [trim analysis](trim-safety-analysis.md) and [full finding review](localization-review.md).

Baseline finding review classes: `{'OBJECTIVE_ERROR': 18, 'INTENTIONAL': 12, 'CONTEXT_REQUIRED': 145, 'CLEAR_LANGUAGE_IMPROVEMENT': 23}`. Dynamic/noise entries are report-only; no new runtime patterns, machine translation or deferred coverage were introduced.

## Runtime / build-system review

Exact normalized-source equivalence after only three version-label substitutions and removal of four diagnostic log guards, their comment and blank line.

Plugin.cs changed; active runtime and main project metadata are 3.6.3. Dropdown source is baseline-identical and remains 1.0.0. F9/F10 UI toggle, Ctrl+F10 reload, Ctrl+F11 extraction, DoPerFrameLogic timing, periodic scans, OnEnable prefix/postfix and selective Encyclopedia text-only AutoFit remain source-identical. No parent geometry mutation, new global font shrink, cockpit hierarchy scanner or added Resources.FindObjectsOfTypeAll call exists. One-time FrameHelper startup and actual UI-toggle logs are retained; unconditional per-key diagnostics are absent.

Build/common changes have concrete purposes: source-only isolated output, local-only restore/no NuGet audit traffic, warnings-as-errors, one shared QA/config instead of conflicting duplicated validators, production manifest/source-DLL version checks and reparse-point safety. No translation hot-path refactor was retained.

## Installer

Backup destination: `<GameRoot>/LocalizationPatchBackups/LocalizationPatch_<timestamp>_<unique-id>/`, outside all BepInEx. Existing target is backed up before mutation. Conflicting DLLs are identified by assembly metadata even when renamed; only identified duplicates are moved, preserving their relative paths. Exact old targets are backed up and overwritten, not rescanned/moved after installation. Legacy `BepInEx/LocalizationPatchBackups` is relocated. Unrelated files/config are retained; ambiguous candidates or unrelated exact target assemblies block installation before replacement. Rollback retains recoverable partial files rather than deleting them. Previous backups are never deleted.

Mock scenarios A clean install, B upgrade/user preservation, C old plugins backup, D renamed duplicate elsewhere, E path with spaces, F no-mutation WhatIf, G repeated invocation , H ambiguous read-only failure and I unrelated exact-target refusal all pass. No real-game installation was run.

## Build / package

Fresh isolated Release build: LocalizationPatch 0 warnings / 0 errors; LocalizationPatchDropdown 0 warnings / 0 errors; warnings treated as errors. QA regression suite: 11/11 PASS. Isolated packaging succeeded before the release ZIP was created. Exact-entry whitelist and embedded SHA256 verification exclude all backups, debug/build trees, logs, snapshots, configurations, absolute paths and experimental artifacts.

Archive listing:

```text
BepInEx/plugins/LocalizationPatch/LocalizationPatch.dll
BepInEx/plugins/LocalizationPatch/LocalizationPatchDropdown.dll
BepInEx/plugins/LocalizationPatch/ru.json
BepInEx/plugins/LocalizationPatch/Tektur-Reg.ttf
```

### Baseline / final hashes

| File | Baseline SHA256 | Final SHA256 |
|---|---|---|
| localization/ru.json | `B0C5554DC3C0945EB29DBAD7E0D7D6FF2414B809A72899D7CAD7A564A43382B4` | `878E1B61CC21A11BE6D4D18DDE0DCD7394A3D9622E82A7ED6AD375B750DBD1A7` |
| src/LocalizationPatch/Plugin.cs | `5172C9F930F20EF1DBA7A31B30D0F57EE78FC507BF32BB150EEE7383DF1FF7EA` | `646D262BEE2EEAAD2CB4A3CB1AEF7660B526379EFE7A9F3CC92EC0F0D20BE789` |
| src/LocalizationPatchDropdown/Plugin.cs | `5C673F1D5C21FB0E24D8D66EFC494CB6D9D3D85A1085818976937F2734EB1214` | `5C673F1D5C21FB0E24D8D66EFC494CB6D9D3D85A1085818976937F2734EB1214` |
| src/LocalizationPatch/bin/Release/net472/LocalizationPatch.dll | `5151D80A92179F9A3CF8C923CC049C91A3D17DCFA722F872D3E8865568FB21ED` | `A23F92C8CA807962793DD0534FDE2A08452BBE975EBE036819BA2174551258CC` |
| src/LocalizationPatchDropdown/bin/Release/net472/LocalizationPatchDropdown.dll | `A25EE2670B1F2699B0702A90FEC2241E99A5CA4F4E27A2EAC26257CF8B84122A` | `C63326A4FE4C05C4A46F6593224D4D43C3F24A47700C253E41F8D38AFE51C4A6` |
| Release ZIP (3.6.0 → 3.6.3) | `BD2A38F976D60865CB38D3A98923181CA84B44E64BCE39A9280A4EEB9CD0FF30` | `C6D2C24FDC085129415FEC300E3FF8E003171D4FDA512D74AC7D499B76DE17E2` |

Main DLL hash is expected to change for logging/version. Dropdown source is unchanged; rebuilt DLL bytes can differ because deterministic compiler inputs include source/build paths. The old 3.6.0 ZIP remains unchanged and is not the active test artifact.

## Git / changed files

No staging or commit performed. Generated ZIPs, DLLs, mock games and recovery evidence are ignored; intended report/config/source files are visible.

### git diff --stat

```text
 .gitignore                                     |   4 +
 CHANGELOG.md                                   |  10 +
 README.md                                      |  25 +-
 README_RU.md                                   |  14 +-
 localization/ru.json                           |   2 +-
 reports/trim-safety-analysis.md                | 506 ++++++++++++-------------
 scripts/build.ps1                              |  85 +++--
 scripts/common.ps1                             |  98 ++---
 scripts/install-local.ps1                      | 135 ++++---
 scripts/package.ps1                            | 110 +++---
 src/LocalizationPatch/LocalizationPatch.csproj |   6 +-
 src/LocalizationPatch/Plugin.cs                |  12 +-
 tools/analyze-trim-safety.py                   |  30 +-
 13 files changed, 524 insertions(+), 513 deletions(-)
```

### git status --short (including new files)

```text
 M .gitignore
 M CHANGELOG.md
 M README.md
 M README_RU.md
 M localization/ru.json
 M reports/trim-safety-analysis.md
 M scripts/build.ps1
 M scripts/common.ps1
 M scripts/install-local.ps1
 M scripts/package.ps1
 M src/LocalizationPatch/LocalizationPatch.csproj
 M src/LocalizationPatch/Plugin.cs
 M tools/analyze-trim-safety.py
?? config/localization-audit.json
?? config/stabilization-changes.json
?? reports/localization-audit.md
?? reports/localization-review.md
?? reports/stabilization-report.md
?? scripts/audit-localization.ps1
?? scripts/test-installer.ps1
?? tools/audit-localization.py
?? tools/report-stabilization.py
?? tools/stabilize-localization.py
?? tools/test-localization-qa.py
```

Runtime: Plugin.cs and main csproj. Localization: ru.json. Audit/tools: config files, audit entry/engine, trim analyzer, guarded phase verifier, QA tests and this report generator. Build/package: build.ps1/common.ps1/package.ps1. Installer: install-local.ps1 and mock-test script. Documentation: README/README_RU/CHANGELOG plus audit/review/trim/stabilization reports. .gitignore protects only generated verification/binary state.

## Quality gates

| Gate | Result |
|---|---|
| JSON valid | PASS |
| Expected entry count | PASS |
| Structured diff fully explained | PASS |
| Protected identities | PASS |
| Model/designation preservation | PASS |
| Proper-name preservation | PASS |
| Placeholders | PASS |
| TMP tags | PASS |
| Trim pass | PASS |
| Strict QA | PASS |
| Runtime regression scan | PASS |
| Build | PASS |
| Installer mock tests | PASS |
| Package | PASS |
| Version consistency | PASS |
| git diff --check | PASS |
| Nothing published | PASS |
| Real game untouched | PASS |

## Final verdict

READY_FOR_USER_TESTING

In-game behavior/layout remains untested by this agent; this is a user-testing handoff, not a production-readiness claim. Known ambiguous/deferred findings remain documented.
