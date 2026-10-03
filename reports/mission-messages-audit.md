# Mission messages audit

## Current 3.6.4 status — verified 2026-10-04

**MISSION_RUNTIME_READY_FOR_GAME_TEST** — automated/static gates passed; no live game test performed.

The recovered 13-message data set is unchanged: **3716 → 3729**, 13 additions, no removed/renamed
keys and no changed existing values. Version 3.6.4 adds one exact Harmony Prefix on the private
`MissionMessages.ShowMessgeLocal(string, bool, FactionHQ)` local display producer, restricted to
those 13 reviewed sources. Each message is translated before LF splitting/feed composition.
The caller's original English RPC argument, sound/faction controls and mission identifiers are unchanged.

Player join/leave notices remain English. Chat, HQMessageInternal and the final combined TMP feed
are not patched. Normal/strict audits exit 0; runtime fixtures 13/13, mission tests 11/11 and general
QA 11/11 pass. Both clean isolated builds have 0 warnings/errors; the newly built dropdown is
IL/API-equivalent to the known-good artifact, with only build/revision metadata differences accepted.

Final ZIP: `release/NuclearOption-RussianLocalization-v3.6.4.zip`.
SHA256: `BE09E9CC57238D8A7E18EB9EB510F042F184B408429EC1E211B20DF5BB2DE745`.
See [mission-runtime-review.md](mission-runtime-review.md) for exact producer/network evidence,
allowlist, final DLL hashes, archive listing, regression/quality gates and deferred coverage.

### Preserved historical 3.6.3 discovery/data-only checkpoint

The original inventory and handoff below are retained in full. Their whole-feed limitations and
NOT IMPLEMENTED/runtime-review verdict describe **3.6.3 before the authorized producer hook**,
not the current 3.6.4 candidate. The source extractor's baseline runtime prose remains a historical
snapshot; the current runtime sign-off is maintained in the separate review linked above.

## Discovery

Recognized named mission TextAssets: **34**. Recognized field occurrences: **480**.
Mission-message candidate rows (excluding identifiers/tutorials): **124**. Generic join notice is counted separately from narrative and is included as one dynamic candidate.

| Category | Distinct exact-source rows |
| --- | ---: |
| STATIC_MISSION_MESSAGE | 123 |
| DYNAMIC_MISSION_MESSAGE | 1 |
| GAMEPLAY_IDENTIFIER | 133 |
| MISSION_EDITOR | 0 |
| MISSION_HINT | 102 |
| UNKNOWN | 0 |

resources.assets SHA256: `88CB99EA168DE540FA1406AC6D12942BD3CAC634597616E8E5EB057C95205D7D`.
Assembly-CSharp.dll SHA256: `EB3B93BDAEC37DD7B3BAB72F801A2C84E5BE2AE3C559F39251E2320AE6B11CCC`.
Read-only inputs: `G:/SteamLibrary/steamapps/common/Nuclear Option/NuclearOption_Data/`.

Scope: recognized named, length-prefixed version-6 mission JSON in resources.assets; not exhaustive across custom/downloaded missions or other Unity formats.

## Runtime safety and reachability

Local metadata/IL was read with the installed Mono.Cecil; no game assembly was executed.
`MissionGroup.ResourceGroup.TryGetJson` reads named `TextAsset.text`. The inventory extracts only
validated version-6 mission JSON, not arbitrary printable strings or editor labels.

`ShowMessageSavedOutcome.Message` -> `ShowMessageOutcome.Load` copies the source into the runtime
Message field. `Complete` passes it to `MissionMessages.ShowMessage`; faction filtering and sound
flags remain separate. `ShowMessgeLocal` (game spelling), and the RPC client path, call
`GameplayUI.GameMessage` -> `MessageUI.GameMessage`. The latter splits on LF and enqueues original
lines plus expiry times in `MessageFeed`. It computes duration from the original source length.
`RefreshUI` joins queued lines with LF and calls `TMP_Text.SetText(StringBuilder)`.

An exhaustive field-reference scan of Assembly-CSharp (including nested types) found `_display`
only in MessageFeed construction and RefreshUI writes; `MessageUI.messageText` is only passed to
the feed constructor. Neither consumer reads localized TMP text back into objectives, callbacks,
IDs, expiry or faction logic. Source fields are saved/copied independently. The selected Reprisal
outcomes have only the five literal fields Message, PlaySound, ObjectiveFactionOnly, UniqueName,
Type; no variable-binding/override payload. Static data translations do not change these fields.
This is evidence for this pinned local build, not a blanket guarantee for arbitrary custom missions.

The 3.6.3 plugin hooks TMP `.text`, `SetText(string)` and OnEnable; legacy `UI.Text.text` calls
`Translate()` and is also scanned. `TranslateTmpComponent`/`Translate` trim the whole displayed
string, perform exact lookup, then existing UI-oriented patterns. The actual mission feed uses
the unhooked StringBuilder overload: existing active TMP sweeps catch it, rather than guaranteed
setter-time interception. Legacy Text is not the traced mission feed. No new sweep is added.

**Important limitation:** one unformatted message alone can match its complete dictionary key.
Two messages, a concurrent player/chat notice, clipped LF lines, or color wrappers normally cannot.
There is no line-by-line or suffix localization in the current lookup. Newline-count preservation
is necessary but does not solve concatenation. No literal combinations/player-name variants are added.

Dialogue objectives use `ShowDialogue` -> `DialogueBox.Show`, with title/body/button routed through
`ReplaceBindTags` and `UnityUITextMeshProGlyphHelper`. The inspected current build's button callback
uses integer CurrentId, not displayed title/button text; objective completion sets a separate bool.
Nevertheless titles/buttons remain unchanged, particularly protected Continue, because of the
previous read-back regression and the plugin's existing title policy. Glyph/binding substitutions
and tutorial dialogue are deferred. No dialogue translations are added in this pass.

## Unsupported dynamic/composed formats — intermediate runtime review

The join notice is proven: `Player.GetDisplayName(context=0) + " joined the game"`, wrapped by
`StringHelper.AddColor` as `<color=#{eight-digit RGBA}>{display name} joined the game</color>`,
then placed in the same feed as narrative/chat. The existing exact lookup cannot handle arbitrary
names, colors or feed combinations. No suffix matcher is added: arbitrary chat can contain the same
words and must not be mistaken for a system notice. Existing exact matching is itself not
context-aware; user text equal to a full dictionary key can still match, a pre-existing limitation.

Proposed future narrow solution (NOT IMPLEMENTED): translate each proven authored ShowMessage
argument locally before feed composition, without mutating mission data/network serialization;
handle JoinMessage only at its proven producer and preserve display-name/tag bytes. Restrict the
authored hook to built-in reviewed outcomes if custom missions must not be affected. Tests would
need to prove queue composition, LF clipping, host/client paths, unchanged identifiers, no chat
interception, exact name preservation and intact color/glyph tags. Risks include Harmony signature
drift, producer call sharing, double translation, client/server divergence and user-generated mission
content. This needs user review before any Plugin.cs edit. No runtime or hierarchy changes made.

## Inventory interpretation and exclusions

Rows are distinct (category, exact source) pairs; a shared literal may appear in multiple categories.
Provenance lists every occurrence in the recognized local TextAssets. Identifiers and tutorial
material are separate exclusion rows, never included in mission-message candidate totals. The
manifest intentionally reviews only Reprisal's 13 literal outcomes; proposed translations for other
rows are absent, not silently machine-generated. Empty fields are not candidates. Mission summaries
are listed but their picker/briefing display path has not been cleared for new translation.

Mission Editor is deferred. Did-you-know hints and tutorial guidance are deferred. Cockpit/HUD/MFD
localization remains incomplete and outside scope. Encyclopedia corrections are retained byte-for-byte
as part of the untouched existing values. The current untranslated.txt and extracted_gamedata.txt
exports contain no exact K92 sentence; resources.assets does, with a single-space sentence separator
(the request's line wrapping is not a separate source).
No copied game files, installed-game writes, network access, commit, push or publishing.


## Pre-flight and completed validation

The named main repository began clean on `fix/mission-messages-russian`, HEAD
`fde844a62ed6b19e2c24d10931c0b54530a6d41b`. Branch and HEAD are unchanged; no commit was made.
Pre-pass hashes, ru.json and QA config are retained in `.verification/mission-messages-fde844a/`.
Textual local IL evidence is `runtime-il.txt`; the full inventory is `inventory-after.json`.
The structured addition list (`source`, `before: null`, `after`, category/provenance) is `changes.json`.

**Applied:** 13 reviewed static Reprisal message additions; **3716 → 3729** entries.
No existing value was changed, removed or overwritten. Existing key order and all Encyclopedia
corrections were independently compared to the pre-pass snapshot and retained. Only the configured
expected entry count changed in the existing QA configuration.

**Exact K92 example:** its single-line source is now present with the reviewed Russian value in
the table below. Both K92 occurrences are unchanged. A model of whole-string lookup passes for
the standalone message and deliberately fails to match a combined feed. No live game test was run:
the important limitation is not solved by data alone.

Validation results:

- Valid JSON; 3729 distinct keys; duplicate exact keys 0.
- Normal audit exit **0**, strict audit exit **0**.
- Designation, proper-name, placeholder, TMP and protected-identity violations: all **0**.
- `IR Flares`, `Radar Countermeasures`, `Continue`, `M12 Jackknife`: all exact identity mappings.
- Existing QA: **11/11 Python tests passed**. New mission fixtures: **11/11 passed**.
- All existing installer test scenarios passed **only in repository-local mocks**, with `-SkipBuild`.
  Evidence: `.verification/installer-tests-0c359db3e9ae49d79085a7f63e6f781d/results.json`.
- `git diff --check`: exit **0**. Inventory generated twice with identical output before this
  handoff section was added. No network, real-game installation or runtime modifications.
- Other audit counts unchanged: CRITICAL 0, HIGH 116, MEDIUM 49, INFO 13. Trim unsafe 112,
  collisions 4, case groups 189/inconsistent 34, typography 3, newline warnings 2, dynamic noise 12.

Protected file hashes and package:

| File | Before SHA256 | After SHA256 |
| --- | --- | --- |
| ru.json | `70A2F55DB890BA5F3D195BCA6CD511526AB13E9A06D3DFBA23722897B2E8F018` | `3D388BDB3EB5231884E17EBC2FFFC45D874905ADE124EEF6705A2EC72DE2D1D7` |
| Plugin.cs | `646D262BEE2EEAAD2CB4A3CB1AEF7660B526379EFE7A9F3CC92EC0F0D20BE789` | Same; unchanged |
| Dropdown Plugin.cs | `5C673F1D5C21FB0E24D8D66EFC494CB6D9D3D85A1085818976937F2734EB1214` | Same; unchanged |
| LocalizationPatch.dll | `A23F92C8CA807962793DD0534FDE2A08452BBE975EBE036819BA2174551258CC` | Same; unchanged |
| LocalizationPatchDropdown.dll | `C63326A4FE4C05C4A46F6593224D4D43C3F24A47700C253E41F8D38AFE51C4A6` | Same; unchanged |
| ZIP v3.6.3 | `92A75750D6F19B55F8FAA6F740324DD4F903A08F775D5D9093724D9EE6E74701` | `24427F0482BABFEE0B593B516F1362634BF0F1855C938DA8264989A9BF1C3628` |

`scripts/package.ps1 -Version 3.6.3 -SkipBuild` exited **0**, validating four exact payload files.
Version remains 3.6.3; no compilation or DLL replacement. Independent comparison of old/new ZIPs
proves only embedded ru.json changed; both DLLs and the font are identical. Output is
`release/NuclearOption-RussianLocalization-v3.6.3.zip`. The previous ZIP was moved recoverably to
`.verification/previous-packages/b471f200148c4a6abd76c022443ad320-NuclearOption-RussianLocalization-v3.6.3.zip`;
nothing was deleted.

Reproduce the inventory (read-only game inputs; generated report only):

```powershell
python -X utf8 tools/audit-mission-messages.py --resources 'G:\SteamLibrary\steamapps\common\Nuclear Option\NuclearOption_Data\resources.assets' --assembly 'G:\SteamLibrary\steamapps\common\Nuclear Option\NuclearOption_Data\Managed\Assembly-CSharp.dll' --baseline .verification/mission-messages-fde844a/ru-before.json --json-report .verification/mission-messages-fde844a/inventory-after.json
```

Regeneration replaces this report with the deterministic discovery inventory; this handoff section
records the completed pass, rather than pretending the read-only inventory runs validation itself.

## Git handoff and final verdict

`git diff --stat` (tracked files only; four new untracked deliverables are listed in status):

```text
 config/localization-audit.json | 2 +-
 localization/ru.json           | 2 +-
 reports/localization-audit.md  | 2 +-
 3 files changed, 3 insertions(+), 3 deletions(-)
```

`git status --short`:

```text
 M config/localization-audit.json
 M localization/ru.json
 M reports/localization-audit.md
?? config/mission-messages.json
?? reports/mission-messages-audit.md
?? tools/audit-mission-messages.py
?? tools/test-mission-messages.py
```

**MISSION_MESSAGES_NEED_RUNTIME_REVIEW**

The data-only subset passes QA and is packaged, but reliable translation of an authored message
inside a combined feed, and of generic player join notices, needs the separate narrow runtime
review described above. Plugin.cs was not edited. The remaining 110 static candidate rows are not
newly translated: they await language/context review, and some are dialogue controls or summaries
whose route is intentionally outside this approved subset. Mission Editor remains deferred;
Did-you-know/tutorial guidance remains deferred; cockpit/HUD/MFD localization remains incomplete.

## Complete reviewed English → Russian additions

| Exact English source | Reviewed Russian |
| --- | --- |
| `"Enemy tanks cresting the ridge to the south!"` | `"Танки противника выходят на гребень хребта к югу!"` |
| `"Enemy tanks, south east, 3 kilometers out!"` | `"Танки противника на юго-востоке, в 3 километрах!"` |
| `"Enemy tanks to the east, 5 kilometers out!"` | `"Танки противника к востоку, в 5 километрах!"` |
| `"Enemy tanks to the north east!"` | `"Танки противника на северо-востоке!"` |
| `"They've got tanks approaching on all sides. We're going to pull out before we become encircled."` | `"Танки противника подходят со всех сторон. Отходим, пока нас не окружили."` |
| `"A large enemy force is preparing to seize this airport, approaching via K92. You are to support K92's defenders as they perform a fighting retreat, and attrit as many enemy vehicles as possible."` | `"К этому аэропорту через K92 приближаются крупные силы противника, готовящиеся его захватить. Поддержите защитников K92, отходящих с боем, и выведите из строя как можно больше вражеской техники."` |
| `"Enemy troop transports spotted on the highway to the south."` | `"На шоссе к югу замечен транспорт противника для перевозки войск."` |
| `"The enemy is now past K92. They're pushing straight through to the airport. Do not let them reach it!"` | `"Противник прошёл K92 и наступает прямо на аэропорт. Не дайте ему добраться до него!"` |
| `"Be advised, PALA is attempting to set up SAM sites in the southern hills overlooking Maris Airport. Find and destroy them before they lock down the airspace!"` | `"Внимание: PALA пытается развернуть ЗРК на южных холмах над Maris Airport. Найдите и уничтожьте их, пока они не перекрыли воздушное пространство!"` |
| `"Excellent work, enemy anti-air launchers are destroyed."` | `"Отличная работа: вражеские пусковые установки ЗРК уничтожены."` |
| `"PALA's forces are completely routed. Congratulations, you've managed to turn an imminent defeat into a decisive victory."` | `"Силы PALA полностью обращены в бегство. Поздравляем: вы превратили надвигавшееся поражение в решительную победу."` |
| `"The last of us are pulling out now."` | `"Сейчас отходят последние наши подразделения."` |
| `"PALA losses are heavy. Units are retreating."` | `"PALA несёт тяжёлые потери. Подразделения отступают."` |

## Complete source inventory

Each section preserves exact source spelling and whitespace via JSON escaping. Sources are not modified.

### 1. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Airbase"`
- Already in ru.json before this pass: yes
- Before Russian: `"Авиабаза"`
- Current Russian: `"Авиабаза"`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[0].UniqueName`; TextAsset JSON offset 112122504

### 2. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Aircraft Takeoff Alert"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[65].UniqueName`; TextAsset JSON offset 112122504

### 3. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"All Objectives Complete"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[2].UniqueName`; TextAsset JSON offset 112122504

### 4. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"AttacksRepelledMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[23].UniqueName`; TextAsset JSON offset 113336044

### 5. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"BDF Victory message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[20].UniqueName`; TextAsset JSON offset 112122504

### 6. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"BDF Win Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Terminal Control Co-op as BDF"`; `$.outcomes[3].UniqueName`; TextAsset JSON offset 111643176
  - `"Terminal Control Co-op as PALA"`; `$.outcomes[3].UniqueName`; TextAsset JSON offset 115525280
  - `"Terminal Control"`; `$.outcomes[3].UniqueName`; TextAsset JSON offset 117316552

### 7. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"BDFCarrierSunkMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[43].UniqueName`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[43].UniqueName`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[43].UniqueName`; TextAsset JSON offset 115979848

### 8. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"BDFRetreatMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[25].UniqueName`; TextAsset JSON offset 113336044

### 9. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"BDFSinksMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Carrier Duel"`; `$.outcomes[8].UniqueName`; TextAsset JSON offset 116854308

### 10. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Bombing Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[25].UniqueName`; TextAsset JSON offset 116745336

### 11. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 1 - Prepare for Landing"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[1].UniqueName`; TextAsset JSON offset 115400852

### 12. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 1 - Throttle"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[2].UniqueName`; TextAsset JSON offset 117284696

### 13. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 2 - Deploy Gear"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[3].UniqueName`; TextAsset JSON offset 115400852

### 14. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 2 - Use Brakes"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[4].UniqueName`; TextAsset JSON offset 117284696

### 15. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 3 - Landing Assist"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[5].UniqueName`; TextAsset JSON offset 115400852

### 16. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 3 - Steering"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[6].UniqueName`; TextAsset JSON offset 117284696

### 17. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 3.1 - Landing Assist Pt1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[6].UniqueName`; TextAsset JSON offset 115400852

### 18. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 3.2 - Landing Assist Pt2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[7].UniqueName`; TextAsset JSON offset 115400852

### 19. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 4 - Brake"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[10].UniqueName`; TextAsset JSON offset 115400852

### 20. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 4 - Keep plane centered"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[8].UniqueName`; TextAsset JSON offset 117284696

### 21. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 5 - Full throttle"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[10].UniqueName`; TextAsset JSON offset 117284696

### 22. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 5 - Taxi"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[12].UniqueName`; TextAsset JSON offset 115400852

### 23. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 6"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[14].UniqueName`; TextAsset JSON offset 115400852

### 24. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Box 6 - Well done"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[12].UniqueName`; TextAsset JSON offset 117284696

### 25. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Briefing 1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[7].UniqueName`; TextAsset JSON offset 112122504

### 26. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Commander Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[73].UniqueName`; TextAsset JSON offset 112122504

### 27. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"DamageAlertMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Breakout"`; `$.outcomes[17].UniqueName`; TextAsset JSON offset 114927384

### 28. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"DefeatMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Breakout"`; `$.outcomes[10].UniqueName`; TextAsset JSON offset 114927384
  - `"04. Cruise Missile Interception"`; `$.outcomes[6].UniqueName`; TextAsset JSON offset 117801024

### 29. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"DefendMessagePt1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Breakout"`; `$.outcomes[2].UniqueName`; TextAsset JSON offset 114927384

### 30. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"DefendMessagePt2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Breakout"`; `$.outcomes[6].UniqueName`; TextAsset JSON offset 114927384

### 31. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"EndMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[20].UniqueName`; TextAsset JSON offset 113616164
  - `"03. Point Blank"`; `$.outcomes[26].UniqueName`; TextAsset JSON offset 116745336

### 32. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"EnemyCAPSpottedMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[30].UniqueName`; TextAsset JSON offset 113616164

### 33. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Fail Condition Warning - Destroy BDF Facility"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[67].UniqueName`; TextAsset JSON offset 112122504

### 34. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"FighterWarning"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[8].UniqueName`; TextAsset JSON offset 117198832

### 35. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Final Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[11].UniqueName`; TextAsset JSON offset 112122504

### 36. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"FinalVictoryMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Breakout"`; `$.outcomes[15].UniqueName`; TextAsset JSON offset 114927384

### 37. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"FirstSAMMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[8].UniqueName`; TextAsset JSON offset 116745336

### 38. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"FirstTargetMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 116745336

### 39. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"FlightMessage1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[15].UniqueName`; TextAsset JSON offset 113616164

### 40. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"FlightMessage2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[16].UniqueName`; TextAsset JSON offset 113616164

### 41. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"FlightMessage3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[17].UniqueName`; TextAsset JSON offset 113616164

### 42. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"HitMessage1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[18].UniqueName`; TextAsset JSON offset 113616164

### 43. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"HitMessage2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[19].UniqueName`; TextAsset JSON offset 113616164

### 44. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"K92FallMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[12].UniqueName`; TextAsset JSON offset 113336044

### 45. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"LaserWarning"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[14].UniqueName`; TextAsset JSON offset 115418932

### 46. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[9].UniqueName`; TextAsset JSON offset 117198832

### 47. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[10].UniqueName`; TextAsset JSON offset 117198832

### 48. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[11].UniqueName`; TextAsset JSON offset 117198832

### 49. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[15].UniqueName`; TextAsset JSON offset 117198832

### 50. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[1].UniqueName`; TextAsset JSON offset 115473564

### 51. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[2].UniqueName`; TextAsset JSON offset 115473564

### 52. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[3].UniqueName`; TextAsset JSON offset 115473564

### 53. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Defend bridge"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 115418932

### 54. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Destroy Convoy"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[4].UniqueName`; TextAsset JSON offset 115473564

### 55. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Destroy Depot"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[8].UniqueName`; TextAsset JSON offset 115497696

### 56. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Eliminate Depot"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[7].UniqueName`; TextAsset JSON offset 115418932

### 57. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Find Target Waypoint"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[6].UniqueName`; TextAsset JSON offset 115497696

### 58. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Intercept Bomber"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"04. Cruise Missile Interception"`; `$.outcomes[1].UniqueName`; TextAsset JSON offset 117801024

### 59. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Land at Naval Base"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[10].UniqueName`; TextAsset JSON offset 115497696

### 60. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Mission Start"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[2].UniqueName`; TextAsset JSON offset 115418932
  - `"09. Depot Strike"`; `$.outcomes[15].UniqueName`; TextAsset JSON offset 115497696
  - `"04. Cruise Missile Interception"`; `$.outcomes[10].UniqueName`; TextAsset JSON offset 117801024

### 61. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Spotted"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[7].UniqueName`; TextAsset JSON offset 115473564

### 62. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Message_Take Off"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 115497696

### 63. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"NavalIncomingMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[48].UniqueName`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[48].UniqueName`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[48].UniqueName`; TextAsset JSON offset 115979848

### 64. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"ObjectiveWinMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[14].UniqueName`; TextAsset JSON offset 117198832

### 65. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"OrbitEndMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[28].UniqueName`; TextAsset JSON offset 113616164

### 66. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"PALA Win"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[31].UniqueName`; TextAsset JSON offset 112122504

### 67. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"PALA Win Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Terminal Control Co-op as BDF"`; `$.outcomes[4].UniqueName`; TextAsset JSON offset 111643176
  - `"Terminal Control Co-op as PALA"`; `$.outcomes[4].UniqueName`; TextAsset JSON offset 115525280
  - `"Terminal Control"`; `$.outcomes[4].UniqueName`; TextAsset JSON offset 117316552

### 68. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"PALACarrierSunkMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[44].UniqueName`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[44].UniqueName`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[44].UniqueName`; TextAsset JSON offset 115979848

### 69. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"PALAScrambleWarning"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[14].UniqueName`; TextAsset JSON offset 116745336

### 70. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"PALASinksMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Carrier Duel"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 116854308

### 71. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"RendevouzMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[17].UniqueName`; TextAsset JSON offset 116745336

### 72. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"ResupplyMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[20].UniqueName`; TextAsset JSON offset 116745336

### 73. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"RoutMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[29].UniqueName`; TextAsset JSON offset 113336044

### 74. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SAMDestroyedMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[15].UniqueName`; TextAsset JSON offset 113336044

### 75. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SAMSitesMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[7].UniqueName`; TextAsset JSON offset 116745336

### 76. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SAMWarning"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[13].UniqueName`; TextAsset JSON offset 115418932

### 77. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SAMWarningMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[13].UniqueName`; TextAsset JSON offset 113336044

### 78. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SecondSAMSiteMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[9].UniqueName`; TextAsset JSON offset 116745336

### 79. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Shard 1 Down"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[57].UniqueName`; TextAsset JSON offset 112122504

### 80. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Shard 1 Failed"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[36].UniqueName`; TextAsset JSON offset 112122504

### 81. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Shard 2 Down"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[59].UniqueName`; TextAsset JSON offset 112122504

### 82. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Shard 2 Failed"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[55].UniqueName`; TextAsset JSON offset 112122504

### 83. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Shoot Down Commander Fail"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[77].UniqueName`; TextAsset JSON offset 112122504

### 84. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SpawnFleetsMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[51].UniqueName`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[51].UniqueName`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[51].UniqueName`; TextAsset JSON offset 115979848

### 85. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SpotCarrier"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Carrier Duel"`; `$.outcomes[3].UniqueName`; TextAsset JSON offset 116854308

### 86. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SpotMRAPsMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[10].UniqueName`; TextAsset JSON offset 113336044

### 87. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SpotTanks1Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[4].UniqueName`; TextAsset JSON offset 113336044

### 88. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SpotTanks2Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 113336044

### 89. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SpotTanks3Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[6].UniqueName`; TextAsset JSON offset 113336044

### 90. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SpotTanks4Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[7].UniqueName`; TextAsset JSON offset 113336044

### 91. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"SpottedAllTanksMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[8].UniqueName`; TextAsset JSON offset 113336044

### 92. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"StartMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Terminal Control Co-op as BDF"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 111643176
  - `"13. Reprisal"`; `$.outcomes[9].UniqueName`; TextAsset JSON offset 113336044
  - `"02. Round Up"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 113616164
  - `"Breakout"`; `$.outcomes[1].UniqueName`; TextAsset JSON offset 114927384
  - `"Terminal Control Co-op as PALA"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 115525280
  - `"Terminal Control"`; `$.outcomes[5].UniqueName`; TextAsset JSON offset 117316552

### 93. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"StartMessage2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[6].UniqueName`; TextAsset JSON offset 113616164

### 94. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"StartMessagePt1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[29].UniqueName`; TextAsset JSON offset 116745336

### 95. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"StartMessagePt2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[30].UniqueName`; TextAsset JSON offset 116745336

### 96. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"StartMessagePt3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[31].UniqueName`; TextAsset JSON offset 116745336

### 97. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"StartMessagePt4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[32].UniqueName`; TextAsset JSON offset 116745336

### 98. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"TakeOffMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[8].UniqueName`; TextAsset JSON offset 113616164

### 99. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Uploaded targets"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[69].UniqueName`; TextAsset JSON offset 112122504

### 100. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"VictoryMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Breakout"`; `$.outcomes[7].UniqueName`; TextAsset JSON offset 114927384

### 101. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Victory_Message"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[46].UniqueName`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[46].UniqueName`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[46].UniqueName`; TextAsset JSON offset 115979848

### 102. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"Waypoint 2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[46].UniqueName`; TextAsset JSON offset 112122504

### 103. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"WinMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Altercation Co-op as BDF"`; `$.outcomes[2].UniqueName`; TextAsset JSON offset 111545216
  - `"Confrontation"`; `$.outcomes[4].UniqueName`; TextAsset JSON offset 112425048
  - `"Altercation Co-op as PALA"`; `$.outcomes[2].UniqueName`; TextAsset JSON offset 113732596
  - `"Domination Co-op as PALA"`; `$.outcomes[1].UniqueName`; TextAsset JSON offset 113851520
  - `"Altercation"`; `$.outcomes[2].UniqueName`; TextAsset JSON offset 113918420
  - `"Confrontation Co-op as BDF"`; `$.outcomes[4].UniqueName`; TextAsset JSON offset 114781868
  - `"Confrontation Co-op as PALA"`; `$.outcomes[4].UniqueName`; TextAsset JSON offset 115163468
  - `"Domination"`; `$.outcomes[1].UniqueName`; TextAsset JSON offset 115308988
  - `"Domination Co-op as BDF"`; `$.outcomes[1].UniqueName`; TextAsset JSON offset 117856920

### 104. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"WingmanDeathMessage"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"02. Round Up"`; `$.outcomes[23].UniqueName`; TextAsset JSON offset 113616164

### 105. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 0"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[1].UniqueName`; TextAsset JSON offset 117771140

### 106. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[1].UniqueName`; TextAsset JSON offset 111406688
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[1].UniqueName`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[3].UniqueName`; TextAsset JSON offset 117771140

### 107. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 10"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[14].UniqueName`; TextAsset JSON offset 117299116

### 108. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 11"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[15].UniqueName`; TextAsset JSON offset 117299116

### 109. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[2].UniqueName`; TextAsset JSON offset 111406688
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[2].UniqueName`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[4].UniqueName`; TextAsset JSON offset 117771140

### 110. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[3].UniqueName`; TextAsset JSON offset 111406688
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[4].UniqueName`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[5].UniqueName`; TextAsset JSON offset 117771140

### 111. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 3.5"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[6].UniqueName`; TextAsset JSON offset 117771140

### 112. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 3_1"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[5].UniqueName`; TextAsset JSON offset 117299116

### 113. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[5].UniqueName`; TextAsset JSON offset 111406688
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[6].UniqueName`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[8].UniqueName`; TextAsset JSON offset 117771140

### 114. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 4.5"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[9].UniqueName`; TextAsset JSON offset 117771140

### 115. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 5"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[6].UniqueName`; TextAsset JSON offset 111406688
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[8].UniqueName`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[13].UniqueName`; TextAsset JSON offset 117771140

### 116. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 6"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[7].UniqueName`; TextAsset JSON offset 111406688
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[9].UniqueName`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[14].UniqueName`; TextAsset JSON offset 117771140

### 117. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 7"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[10].UniqueName`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[16].UniqueName`; TextAsset JSON offset 117771140

### 118. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 8"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[12].UniqueName`; TextAsset JSON offset 117299116

### 119. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box 9"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[13].UniqueName`; TextAsset JSON offset 117299116

### 120. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"box final"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[17].UniqueName`; TextAsset JSON offset 117299116

### 121. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"close enough box"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[11].UniqueName`; TextAsset JSON offset 111406688

### 122. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_12"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[17].UniqueName`; TextAsset JSON offset 112122504

### 123. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_13"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[18].UniqueName`; TextAsset JSON offset 112122504

### 124. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_14"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[19].UniqueName`; TextAsset JSON offset 112122504

### 125. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_19"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[24].UniqueName`; TextAsset JSON offset 112122504

### 126. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[9].UniqueName`; TextAsset JSON offset 112122504

### 127. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_21"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[74].UniqueName`; TextAsset JSON offset 112122504

### 128. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[10].UniqueName`; TextAsset JSON offset 112122504

### 129. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_5"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[12].UniqueName`; TextAsset JSON offset 112122504

### 130. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"empty_8"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[14].UniqueName`; TextAsset JSON offset 112122504

### 131. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"final box"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[13].UniqueName`; TextAsset JSON offset 111406688

### 132. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"fratricide box"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[19].UniqueName`; TextAsset JSON offset 117771140

### 133. GAMEPLAY_IDENTIFIER — KEEP_ENGLISH

- Exact English: `"not close enough box"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[9].UniqueName`; TextAsset JSON offset 111406688

### 134. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"A single trigger pull <bind=Fire> will release one munition per designated target.\nShoot when TGT is within MIN and MAX on the range indicator.\nAll your current weapons are fire and forget."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[9].body`; TextAsset JSON offset 117771140

### 135. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Aerial Targets                              1/2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[13].title`; TextAsset JSON offset 117771140

### 136. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Aerial Targets                              2/2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[14].title`; TextAsset JSON offset 117771140

### 137. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Anchored to the center of your view, there is a target designator diamond, which will become visible when you look around.\nYou can select targets by looking at a unit, and pressing the Target Select button <bind=Select>"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[3].body`; TextAsset JSON offset 117771140

### 138. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Angle of Attack Indexer     3/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[7].title`; TextAsset JSON offset 115400852

### 139. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"As we approach the runway threshold, we will make another left turn to line up the plane on the runway."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[6].body`; TextAsset JSON offset 117284696

### 140. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Brakes"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[4].title`; TextAsset JSON offset 117284696

### 141. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Centered on runway"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[8].title`; TextAsset JSON offset 117284696

### 142. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Complete"`
- Already in ru.json before this pass: yes
- Before Russian: `"Полный"`
- Current Russian: `"Полный"`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[16].title`; TextAsset JSON offset 117771140

### 143. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Congratulations - you've successfully avoided radar missiles in a worst case scenario.\nIdeally, you can avoid these missiles by breaking line of sight of the radar, or by hugging the surface as tightly as possible to stay within ground clutter. Feel free to resume and practice this."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[17].body`; TextAsset JSON offset 117299116

### 144. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Defending                                    1/4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[12].title`; TextAsset JSON offset 117299116

### 145. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Defending                                    2/4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[13].title`; TextAsset JSON offset 117299116

### 146. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Defending                                    3/4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[14].title`; TextAsset JSON offset 117299116

### 147. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Defending                                    4/4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[15].title`; TextAsset JSON offset 117299116

### 148. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Deploy Gear"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[3].title`; TextAsset JSON offset 115400852

### 149. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Different weapons have different intended targets. If targets are ever overlapping, target selection will be biased towards suitable targets for the currently selected weapon. \nSwitch weapons to your MMR-S3s, and find and destroy the plane approaching from bearing 180."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[14].body`; TextAsset JSON offset 117771140

### 150. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Enemy Radar                             1/2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[1].title`; TextAsset JSON offset 117299116

### 151. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Enemy Radar                             2/2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[2].title`; TextAsset JSON offset 117299116

### 152. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Escape"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[11].title`; TextAsset JSON offset 111406688

### 153. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Escaped Successfully"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[17].title`; TextAsset JSON offset 117299116

### 154. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Evasion Complete"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[13].title`; TextAsset JSON offset 111406688

### 155. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Excellent work. This concludes Targeting and Weapons."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[16].body`; TextAsset JSON offset 117771140

### 156. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Flare Usage                                 1/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[5].title`; TextAsset JSON offset 111406688

### 157. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Flare Usage                                 2/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[6].title`; TextAsset JSON offset 111406688

### 158. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Flare Usage                                 3/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[7].title`; TextAsset JSON offset 111406688

### 159. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Flare effectiveness is determined by your aspect to the missile, as well as your engine output. Lower your throttle and turn the plane side-on to the threat to get the most out of your flares. If you get fired on from behind at full throttle, or you may need to expend the whole cartridge."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[6].body`; TextAsset JSON offset 111406688

### 160. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Four new contacts - enemy trucks - are present at bearing 060.\u000bPress the Next Weapon button <bind=Next Weapon> or the weapon wheel <bind=Weapon Wheel> + <bind=Radial Menu Horizontal> until your AGM-48s are selected, and then designate the four enemy trucks as targets and fire on them."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[8].body`; TextAsset JSON offset 117771140

### 161. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Fratricide"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[19].title`; TextAsset JSON offset 117771140

### 162. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Full Throttle"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[10].title`; TextAsset JSON offset 117284696

### 163. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Glideslope indicator          2/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[6].title`; TextAsset JSON offset 115400852

### 164. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Good job - the trucks are destroyed.\n\nThe process for targeting and firing on aerial targets is the same, however, you should make sure you have the right weapon selected."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[13].body`; TextAsset JSON offset 117771140

### 165. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Good, now tap the wheelbrake <bind=Brake> to keep your plane from exceeding 50km/h. We are approaching a turn which will require you stay slow.\u000bUse the rudder to steer <bind=Yaw>"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[4].body`; TextAsset JSON offset 117284696

### 166. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Great job, we're in the air! If you haven't already, you should now retract your landing gear using <bind=Gear> \u000bor the radial menu <bind=Radial Menu> + <bind=Radial Menu Horizontal>"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[12].body`; TextAsset JSON offset 117284696

### 167. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Having received an emission doesn't necessarily mean you have been spotted - it just means you have detected that a radar is being used.\u000b"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[4].body`; TextAsset JSON offset 117299116

### 168. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Helmet Mounted Display"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[1].title`; TextAsset JSON offset 117771140

### 169. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Hold down the wheelbrake button <bind=Brake> to bring the plane to a stop."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[10].body`; TextAsset JSON offset 115400852

### 170. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"If you are using virtual joystick (mouse flight), you will need to hold the freelook button <bind=Free Look> to look around.\nIf you are using a controller, you should make sure virtual joystick is disabled in options, and use the right stick <bind=Pan View> to look around."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[4].body`; TextAsset JSON offset 117771140

### 171. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"In front of you is an enemy SAM launcher which fires IRM-S2s. It has an effective range of 8km (5 miles).\n\nTo pass the training, you will have to fly within half that distance from it, and then return to this point alive."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[3].body`; TextAsset JSON offset 111406688

### 172. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"In this instance, however, you have definitely been spotted. The radar has a range of approximately 40km, and is only 15km away.\u000b\nThe radar will now be used to guide a Stratolance missile into you."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[6].body`; TextAsset JSON offset 117299116

### 173. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Increase throttle to 100%, and when speed is above 180km/h, gradually pull back on the stick to lift off. <bind=Pitch:neg>"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[10].body`; TextAsset JSON offset 117284696

### 174. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Infrared Countermeasures          1/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[1].title`; TextAsset JSON offset 111406688

### 175. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Infrared Countermeasures          2/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[2].title`; TextAsset JSON offset 111406688

### 176. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Infrared Countermeasures          3/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[3].title`; TextAsset JSON offset 111406688

### 177. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Landing Assist                   1/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[5].title`; TextAsset JSON offset 115400852

### 178. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Landing Complete"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[14].title`; TextAsset JSON offset 115400852

### 179. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Learn how to defeat semi-active radar homing missiles. For this lesson you will be piloting the T/A-30 Compass trainer aircraft."`
- Already in ru.json before this pass: yes
- Before Russian: `"Узнайте, как нейтрализовать ракеты с полуактивным радиолокационным наведением. На этом уроке вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Current Russian: `"Узнайте, как нейтрализовать ракеты с полуактивным радиолокационным наведением. На этом уроке вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.missionSettings.description`; TextAsset JSON offset 117299116

### 180. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Learn how to designate targets and use missiles to destroy them. For this lesson you will be piloting the T/A-30 Compass trainer aircraft."`
- Already in ru.json before this pass: yes
- Before Russian: `"Научитесь поражать цели и использовать ракеты для их уничтожения. На этом уроке вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Current Russian: `"Научитесь поражать цели и использовать ракеты для их уничтожения. На этом уроке вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.missionSettings.description`; TextAsset JSON offset 117771140

### 181. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Learn how to manage throttle, brake and rudder to safely taxi to the runway, before conducting your first take off. For this lesson you will be piloting the T/A-30 Compass trainer aircraft."`
- Already in ru.json before this pass: yes
- Before Russian: `"Перед первым взлетом научитесь управлять тягой, тормозом и рулем направления для безопасного руления на ВВП. На этом занятии вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Current Russian: `"Перед первым взлетом научитесь управлять тягой, тормозом и рулем направления для безопасного руления на ВВП. На этом занятии вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.missionSettings.description`; TextAsset JSON offset 117284696

### 182. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Learn how to prepare for and perform a landing. For this lesson you will be piloting the T/A-30 Compass trainer aircraft."`
- Already in ru.json before this pass: yes
- Before Russian: `"Научитесь готовиться к посадке и выполнять её. На этом занятии вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Current Russian: `"Научитесь готовиться к посадке и выполнять её. На этом занятии вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.missionSettings.description`; TextAsset JSON offset 115400852

### 183. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Learn how to use flares to defeat IR missiles. For this lesson you will be piloting the T/A-30 Compass trainer aircraft."`
- Already in ru.json before this pass: yes
- Before Russian: `"Научитесь использовать ЛТЦ для нейтрализации ракет с инфракрасным излучением. На этом уроке вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Current Russian: `"Научитесь использовать ЛТЦ для нейтрализации ракет с инфракрасным излучением. На этом уроке вы будете пилотировать тренировочный самолет T/A-30 Compass."`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.missionSettings.description`; TextAsset JSON offset 111406688

### 184. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Lower your landing gear using <bind=Gear> or the radial menu <bind=Radial Menu> + <bind=Radial Menu Horizontal>\n\nYour flaps will automatically lower to landing position at slower speeds - you will notice a change in handling."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[3].body`; TextAsset JSON offset 115400852

### 185. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Lowering your gear has also activated the landing assist on the HUD.\u000b\u000bIt has two features: The Glideslope indicator, and the Angle of Attack (AoA) Indexer"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[5].body`; TextAsset JSON offset 115400852

### 186. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Make sure flares are selected and visible in the top right of the HMD <bind=Next Countermeasure>\n\nWhen fired on, press and hold the Countermeasure button. <bind=Countermeasures>"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[5].body`; TextAsset JSON offset 111406688

### 187. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Missiles that see via the infrared spectral band are a common battlefield threat.\n\nThe signature of your aircraft is provided to them by the heat that operating it produces."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[1].body`; TextAsset JSON offset 111406688

### 188. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Next"`
- Already in ru.json before this pass: yes
- Before Russian: `"Следующий"`
- Current Russian: `"Следующий"`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[1].button`; TextAsset JSON offset 111406688
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[2].button`; TextAsset JSON offset 111406688
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[5].button`; TextAsset JSON offset 111406688
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[6].button`; TextAsset JSON offset 111406688
  - `"Tutorial 2 - Landing"`; `$.objectives[5].button`; TextAsset JSON offset 115400852
  - `"Tutorial 2 - Landing"`; `$.objectives[6].button`; TextAsset JSON offset 115400852
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[1].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[4].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[5].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[8].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[9].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[12].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[13].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[14].button`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[3].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[4].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[5].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[8].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[13].button`; TextAsset JSON offset 117771140

### 189. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Not dangerous enough"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[9].title`; TextAsset JSON offset 111406688

### 190. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Notching                                      1/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[8].title`; TextAsset JSON offset 117299116

### 191. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Notching                                      2/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[9].title`; TextAsset JSON offset 117299116

### 192. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Notching                                      3/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[10].title`; TextAsset JSON offset 117299116

### 193. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Notching alone is rarely enough to defeat a missile, especially in less stealthy aircraft.\nWhile in the notch envelope however, is the ideal time to use your ECM. The lack of doppler shifted returns, combined with the radar ECM, should mask you from the radar."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[13].body`; TextAsset JSON offset 117299116

### 194. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Notching, in short, can be described as flying perpendicular to the enemy radar.\n\nDoing this removes the doppler shift from your return frequencies, making it harder for the radar to track you."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[9].body`; TextAsset JSON offset 117299116

### 195. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Now leave the SAM's area of effect and return to where you started. Because you'll be showing it your exhaust as you fly away, it is especially important that you reduce your throttle to reduce your signature compared to that of your flares."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[11].body`; TextAsset JSON offset 111406688

### 196. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Now that the missile is close enough to be picked up and analysed by your sensors, a notch guide is provided both on the HUD and minimap.\n\nThe yellow dotted line indicates the ideal heading to maintain in order to perform a notch."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[12].body`; TextAsset JSON offset 117299116

### 197. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Now turn left and keep the plane centered on the runway."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[8].body`; TextAsset JSON offset 117284696

### 198. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Oh."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[3].button`; TextAsset JSON offset 111406688
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[6].button`; TextAsset JSON offset 117299116

### 199. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Ok"`
- Already in ru.json before this pass: yes
- Before Russian: `"ОК"`
- Current Russian: `"ОК"`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[7].button`; TextAsset JSON offset 111406688
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[9].button`; TextAsset JSON offset 111406688
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[11].button`; TextAsset JSON offset 111406688
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[13].button`; TextAsset JSON offset 111406688
  - `"Tutorial 2 - Landing"`; `$.objectives[1].button`; TextAsset JSON offset 115400852
  - `"Tutorial 2 - Landing"`; `$.objectives[3].button`; TextAsset JSON offset 115400852
  - `"Tutorial 2 - Landing"`; `$.objectives[7].button`; TextAsset JSON offset 115400852
  - `"Tutorial 2 - Landing"`; `$.objectives[10].button`; TextAsset JSON offset 115400852
  - `"Tutorial 2 - Landing"`; `$.objectives[12].button`; TextAsset JSON offset 115400852
  - `"Tutorial 2 - Landing"`; `$.objectives[14].button`; TextAsset JSON offset 115400852
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[2].button`; TextAsset JSON offset 117284696
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[4].button`; TextAsset JSON offset 117284696
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[6].button`; TextAsset JSON offset 117284696
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[8].button`; TextAsset JSON offset 117284696
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[10].button`; TextAsset JSON offset 117284696
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[12].button`; TextAsset JSON offset 117284696
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[2].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[10].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[15].button`; TextAsset JSON offset 117299116
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[17].button`; TextAsset JSON offset 117299116
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[1].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[6].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[9].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[14].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[16].button`; TextAsset JSON offset 117771140
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[19].button`; TextAsset JSON offset 117771140

### 200. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"On the left side of the HUD is your angle of attack indexer. Green is too slow, yellow is on speed, and red is too fast.\u000bWhile steering, adjust the throttle to keep the AoA indexer showing a yellow circle. Continue until you touch down."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[7].body`; TextAsset JSON offset 115400852

### 201. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Our goal will be to get to cover behind the mountains. Start by breaking right, diving toward the water's surface, and getting the incoming radar line to stay at your 9 o'clock.\nYou should also select your Radar ECM by pressing Next Countermeasures <bind=Next Countermeasure>"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[10].body`; TextAsset JSON offset 117299116

### 202. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Positioned on a small island 20km (12 miles) in front of you are two trucks.\n\nOne tows a launch system for R9 Stratolance missiles, while the other carries a connected radar that provides guidance for them."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[1].body`; TextAsset JSON offset 117299116

### 203. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Pre-flaring (releasing flares if you suspect you're about to be fired on) is the most effective use of flares, as it can prevent the launching platform from obtaining a lock.\nTry releasing flares periodically (once or twice a second) when in danger."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[7].body`; TextAsset JSON offset 111406688

### 204. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Prepare for Landing"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[1].title`; TextAsset JSON offset 115400852

### 205. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Radar Range                              1/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[4].title`; TextAsset JSON offset 117299116

### 206. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Radar Range                              2/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[5].title`; TextAsset JSON offset 117299116

### 207. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Radar Range                              3/3"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[6].title`; TextAsset JSON offset 117299116

### 208. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Radar pings appear as lines on your minimap\n\r\nGrey = this radar has probably not detected you\r\nYellow = this radar has probably detected you\r\nRed = this radar is actively targeting you"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[5].body`; TextAsset JSON offset 117299116

### 209. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Red icons denote enemy units.\n\nBlue icons denote friendly units.\n\n\nDo not fire on the blue icons."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[19].body`; TextAsset JSON offset 117771140

### 210. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Successful Landing"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[12].title`; TextAsset JSON offset 115400852

### 211. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Successful Takeoff"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[12].title`; TextAsset JSON offset 117284696

### 212. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Take some time to practice selecting and deselecting targets. You will need to be proficient at this, and be able to do it quickly under pressure in order to be truly effective in combat.\nWhen you are ready to start shooting, fly to the marked waypoint."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[6].body`; TextAsset JSON offset 117771140

### 213. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Target Designation                     1/4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[3].title`; TextAsset JSON offset 117771140

### 214. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Target Designation                     2/4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[4].title`; TextAsset JSON offset 117771140

### 215. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Target Designation                     3/4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[5].title`; TextAsset JSON offset 117771140

### 216. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Target Designation                     4/4"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[6].title`; TextAsset JSON offset 117771140

### 217. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Taxi"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[6].title`; TextAsset JSON offset 117284696

### 218. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"The airstrip you'll be landing at is directly infront of you. Start by reducing your throttle <bind=Throttle:neg> to zero - this will deploy the airbrake.\n\u000bTry to bring your speed down to at most 375kph (200 knots) before the next waypoint."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[1].body`; TextAsset JSON offset 115400852

### 219. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"The bright light rising up off of the island is a Stratolance missile. You have been fired at.\n\nAs you are high in the air and well within the range of the missile, the only way to survive this encounter is by executing a notch."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[8].body`; TextAsset JSON offset 117299116

### 220. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"The emission from the radar is detectable by your radar receiver, and the direction to the radar is indicated by an orange line on the minimap. As radar based detection relies on bouncing a signal off of something, you can detect radar emissions at approximately double the range of a radar system."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[2].body`; TextAsset JSON offset 117299116

### 221. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"The jammer's effectiveness is proportional to remaining capacitor charge. It is best used in 3 second bursts per missile.\n\nUse the jammer <bind=Countermeasures> while notching to escape toward the coast."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[15].body`; TextAsset JSON offset 117299116

### 222. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"The line coming out of the runway with a small circle at the end is your glideslope indicator.\n\nAs you glide, steer so that your velocity vector envelops the small circle at the end of the glideslope."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[6].body`; TextAsset JSON offset 115400852

### 223. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"The tracking must be broken for at least 3 seconds for the missile to not re-acquire.\nNote that even when the missile loses track, it will still head for the last calculated intercept point. You must take care to evade whilst not exiting the notch."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 5 - Radar Countermeasures"`; `$.objectives[14].body`; TextAsset JSON offset 117299116

### 224. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Throttle"`
- Already in ru.json before this pass: yes
- Before Russian: `"Тяга"`
- Current Russian: `"Тяга"`
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[2].title`; TextAsset JSON offset 117284696

### 225. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Today we're going to be practicing taxiing to the runway threshold and taking off. To begin, increase the throttle to 20% using <bind=Throttle:pos>"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 1 - Taxi and Takeoff"`; `$.objectives[2].body`; TextAsset JSON offset 117284696

### 226. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Today you will learn how to target and fire on enemy units.\nYour HMD will highlight all units known to either your aircraft's sensors or the datalink system.\n\nObserve the various units highlighted in front of you."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[1].body`; TextAsset JSON offset 117771140

### 227. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Weapon Usage                            1/2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[8].title`; TextAsset JSON offset 117771140

### 228. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Weapon Usage                            2/2"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[9].title`; TextAsset JSON offset 117771140

### 229. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Well done, you've entered the IR SAM's area of effect and come back alive.\n\nThis completes the training, but if you still have flares left, feel free to resume and continue tempting fate."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[13].body`; TextAsset JSON offset 111406688

### 230. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Well done. Normally, you wouldn't come to a complete stop, as it is important to keep the runway clear.\u000b\u000bUse one of the two marked ramps to exit the runway."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[12].body`; TextAsset JSON offset 115400852

### 231. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"Wheel Brakes"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[10].title`; TextAsset JSON offset 115400852

### 232. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"When you come to a stop at an airbase, you can disembark the plane using the Eject key <bind=Eject>\u000b\u000bThis will return your plane to your inventory. This will be important later."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 2 - Landing"`; `$.objectives[14].body`; TextAsset JSON offset 115400852

### 233. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"You are pulling away too soon. While the best and most obvious survival method is to avoid the SAM in the first place, for the sake of this demonstration, please take unreasonable risk."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[9].body`; TextAsset JSON offset 111406688

### 234. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"You can add multiple targets to your designation.\n\nTo remove the last selected target, press Target Cancel <bind=Cancel>\nTo clear the designation entirely, hold the button down."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 3 - Targeting and Weapons"`; `$.objectives[5].body`; TextAsset JSON offset 117771140

### 235. MISSION_HINT — KEEP_ENGLISH

- Exact English: `"You can defeat IR missiles by using flares - intense heat signatures - that can either distract or dazzle the seeker head.\n\nEvery aircraft in the arsenal has flares."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Excluded from new translations; any pre-existing mapping is left untouched
- Action: KEEP_ENGLISH
- Provenance:
  - `"Tutorial 4 - Infrared Countermeasures"`; `$.objectives[2].body`; TextAsset JSON offset 111406688

### 236. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"\"War? No. This is merely a peacekeeping initiative.\"\n\nLow intensity fighting over the disputed zone. Each side operates from a single forward airbase and must destroy the other's. Aircraft are restricted to counter-insurgency platforms, trainers, helicopters, and transports. No medium or long range air-to-air missiles are available. Air battles are resolved either with guns, or the relatively short ranged IRM-S1."`
- Already in ru.json before this pass: yes
- Before Russian: `"«Война? Нет. Это всего лишь миротворческая инициатива».\n\nБои низкой интенсивности за спорную зону. Каждая сторона действует с одной передовой авиабазы ​​и должна уничтожить авиабазу другой стороны. Воздушные суда ограничены платформами для борьбы с повстанцами, учебно-тренировочными самолетами, вертолетами и транспортными средствами. Ракет средней и большой дальности «воздух-воздух» нет. Воздушные бои решаются либо с помощью пушек, либо с помощью IRM-S1 относительно малой дальности."`
- Current Russian: `"«Война? Нет. Это всего лишь миротворческая инициатива».\n\nБои низкой интенсивности за спорную зону. Каждая сторона действует с одной передовой авиабазы ​​и должна уничтожить авиабазу другой стороны. Воздушные суда ограничены платформами для борьбы с повстанцами, учебно-тренировочными самолетами, вертолетами и транспортными средствами. Ракет средней и большой дальности «воздух-воздух» нет. Воздушные бои решаются либо с помощью пушек, либо с помощью IRM-S1 относительно малой дальности."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"Altercation Co-op as BDF"`; `$.missionSettings.description`; TextAsset JSON offset 111545216
  - `"Altercation Co-op as PALA"`; `$.missionSettings.description`; TextAsset JSON offset 113732596
  - `"Altercation"`; `$.missionSettings.description`; TextAsset JSON offset 113918420

### 237. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"... and remember, they can still shoot back. Don't make it easy for them."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[19].Message`; TextAsset JSON offset 113616164

### 238. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"A BDF engineer team is currently trying to recover a pair of tanks that were immobilised in yesterday's fighting."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[5].Message`; TextAsset JSON offset 113616164

### 239. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"A battle for air superiority fought between two large airbases, using high-end assets. Rank 3 aircraft available at start."`
- Already in ru.json before this pass: yes
- Before Russian: `"Битва за воздушное превосходство между двумя огромными базами, используя высокотехнологичные технологии. 3 ранг доступен с начала игры."`
- Current Russian: `"Битва за воздушное превосходство между двумя огромными базами, используя высокотехнологичные технологии. 3 ранг доступен с начала игры."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"Domination Co-op as PALA"`; `$.missionSettings.description`; TextAsset JSON offset 113851520
  - `"Domination"`; `$.missionSettings.description`; TextAsset JSON offset 115308988
  - `"Domination Co-op as BDF"`; `$.missionSettings.description`; TextAsset JSON offset 117856920

### 240. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"A campaign of island hopping, in which BDF and PALA fight for control of the Ignus Archipelago.\u000b\u000bYour mission is to take and hold the Feldspar International Airport and surrounding smaller airstrips, and to sufficiently degrade the enemy's ability to launch further attacks."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"Terminal Control Co-op as BDF"`; `$.missionSettings.description`; TextAsset JSON offset 111643176
  - `"Terminal Control Co-op as PALA"`; `$.missionSettings.description`; TextAsset JSON offset 115525280
  - `"Terminal Control"`; `$.missionSettings.description`; TextAsset JSON offset 117316552

### 241. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"A column of enemy vehicles is approaching the bridge to Boscali Island. Prevent them from crossing and doing damage to BDF facilities. This civilian airstrip has been commandeered as forward arming and refueling point."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[2].Message`; TextAsset JSON offset 115418932

### 242. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"A combined-arms battle on the eastern half of the map, limited to smaller aircraft. Each side has one main airbase and one forward airbase, with naval assets watching the flanks."`
- Already in ru.json before this pass: yes
- Before Russian: `"Малая битва на восточной части карты, ограниченная малыми воздушными средствами. Каждая сторона имеет одну основную базу и одну наступающую базу, также на флангах расположены морские средства."`
- Current Russian: `"Малая битва на восточной части карты, ограниченная малыми воздушными средствами. Каждая сторона имеет одну основную базу и одну наступающую базу, также на флангах расположены морские средства."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"Confrontation"`; `$.missionSettings.description`; TextAsset JSON offset 112425048
  - `"Confrontation Co-op as BDF"`; `$.missionSettings.description`; TextAsset JSON offset 114781868
  - `"Confrontation Co-op as PALA"`; `$.missionSettings.description`; TextAsset JSON offset 115163468

### 243. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"A large convoy of fuel trucks was last spotted about 5km north of Dustbowl. We're headed to the convoy's last known position."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[2].Message`; TextAsset JSON offset 115473564

### 244. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"A large enemy force is preparing to seize this airport, approaching via K92. You are to support K92's defenders as they perform a fighting retreat, and attrit as many enemy vehicles as possible."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"К этому аэропорту через K92 приближаются крупные силы противника, готовящиеся его захватить. Поддержите защитников K92, отходящих с боем, и выведите из строя как можно больше вражеской техники."`
- Proposed Russian: `"К этому аэропорту через K92 приближаются крупные силы противника, готовящиеся его захватить. Поддержите защитников K92, отходящих с боем, и выведите из строя как можно больше вражеской техники."`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[9].Message`; TextAsset JSON offset 113336044

### 245. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"A pure air & sea battle between two carrier groups. Boscali's Annex Class Assault Carrier vs Primeva's Hyperion Class Fleet Carrier, with their respective compliments of aircraft.\u000b\u000bThe first side to sink the other's carrier wins. All 36 carrier aircraft are available immediately, and cannot be replaced easily if shot down. Fly, fight, and land with care."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"Carrier Duel"`; `$.missionSettings.description`; TextAsset JSON offset 116854308

### 246. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"A ship has been sunk. The Boscali Navy is moving to attack the island."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Breakout"`; `$.outcomes[2].Message`; TextAsset JSON offset 114927384

### 247. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"AAAHGRPL-%^$*&"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[23].Message`; TextAsset JSON offset 113616164

### 248. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Additionally, be warned that the enemy has an Argus Class air defence frigate, which requires its missiles be jammed directly."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[15].Message`; TextAsset JSON offset 117198832

### 249. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"All BDF ships are headed to the bottom of the strait - now we can take back South Boscali!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Breakout"`; `$.outcomes[7].Message`; TextAsset JSON offset 114927384

### 250. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"All Objectives are complete! Leave the area and RTB."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[2].Message`; TextAsset JSON offset 112122504

### 251. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"All enemy R9 systems are neutralised. Head back to the ships to re-arm."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[17].Message`; TextAsset JSON offset 116745336

### 252. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"An enormous, high intensity war of attrition with all airbases active and using all available assets.\u000b\u000bSuccessively more powerful aircraft, and eventually thermonuclear weapons, are unlocked by increasing individual and team point score respectively.\n\nVictory is acheived when all enemy aircraft factories are destroyed and the enemy side's aircraft carrier, which will arrive midway through the battle, is sunk."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.missionSettings.description`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.missionSettings.description`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.missionSettings.description`; TextAsset JSON offset 115979848

### 253. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"BDF forces have been removed from the mainland and PALA holds the surrounding airstrips. PALA Is Victorious."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Terminal Control Co-op as BDF"`; `$.outcomes[4].Message`; TextAsset JSON offset 111643176
  - `"Terminal Control Co-op as PALA"`; `$.outcomes[4].Message`; TextAsset JSON offset 115525280
  - `"Terminal Control"`; `$.outcomes[4].Message`; TextAsset JSON offset 117316552

### 254. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"BDF special forces have set charges to take out PALA's heavy air defences, you'll be hitting the island as they detonate."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[12].Message`; TextAsset JSON offset 112122504

### 255. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"BDF's carrier is sinking. PALA is victorious!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Carrier Duel"`; `$.outcomes[8].Message`; TextAsset JSON offset 116854308

### 256. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Back to basics with bombs & guns on a CI-22 Cricket in a low-intensity engagement."`
- Already in ru.json before this pass: yes
- Before Russian: `"Возвращаемся к истокам c бомбами и оружием на самолете CI-22 Cricket в условиях боя низкой интенсивности."`
- Current Russian: `"Возвращаемся к истокам c бомбами и оружием на самолете CI-22 Cricket в условиях боя низкой интенсивности."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.missionSettings.description`; TextAsset JSON offset 113616164

### 257. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"Be advised, PALA is attempting to set up SAM sites in the southern hills overlooking Maris Airport. Find and destroy them before they lock down the airspace!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Внимание: PALA пытается развернуть ЗРК на южных холмах над Maris Airport. Найдите и уничтожьте их, пока они не перекрыли воздушное пространство!"`
- Proposed Russian: `"Внимание: PALA пытается развернуть ЗРК на южных холмах над Maris Airport. Найдите и уничтожьте их, пока они не перекрыли воздушное пространство!"`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[13].Message`; TextAsset JSON offset 113336044

### 258. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Be advised, enemy fighters have been spotted approaching from Feldspar"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[8].Message`; TextAsset JSON offset 117198832

### 259. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Challenging co-op mission where PALA provokes the BDF navy, and must defend Vigil Cay airbase from a naval attack."`
- Already in ru.json before this pass: yes
- Before Russian: `"Сложная ко-оп миссия, в ходе которой Primeva провоцирует военно-морской флот Boscali и должна защитить авиабазу Виджил Кей от морской атаки."`
- Current Russian: `"Сложная ко-оп миссия, в ходе которой Primeva провоцирует военно-морской флот Boscali и должна защитить авиабазу Виджил Кей от морской атаки."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"Breakout"`; `$.missionSettings.description`; TextAsset JSON offset 114927384

### 260. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Convoy has been spotted. Lets get to work."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[7].Message`; TextAsset JSON offset 115473564

### 261. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Drop the bombs when the countdown reaches zero and the arrows on your HUD converge."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[17].Message`; TextAsset JSON offset 113616164

### 262. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Due to terrain, it cannot be seen unless approaching from the south. You can either destroy the blockade, or attack via the mountains."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[10].Message`; TextAsset JSON offset 117198832

### 263. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Enemy aircraft production facilities are destroyed. Mission accomplished."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Confrontation"`; `$.outcomes[4].Message`; TextAsset JSON offset 112425048
  - `"Confrontation Co-op as BDF"`; `$.outcomes[4].Message`; TextAsset JSON offset 114781868
  - `"Confrontation Co-op as PALA"`; `$.outcomes[4].Message`; TextAsset JSON offset 115163468

### 264. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Enemy aircraft production is destroyed - mission accomplished."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Domination Co-op as PALA"`; `$.outcomes[1].Message`; TextAsset JSON offset 113851520
  - `"Domination"`; `$.outcomes[1].Message`; TextAsset JSON offset 115308988
  - `"Domination Co-op as BDF"`; `$.outcomes[1].Message`; TextAsset JSON offset 117856920

### 265. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Enemy carrier spotted."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Carrier Duel"`; `$.outcomes[3].Message`; TextAsset JSON offset 116854308

### 266. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Enemy planes are after us! Stay near our base, our anti-air will protect us!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[30].Message`; TextAsset JSON offset 113616164

### 267. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"Enemy tanks cresting the ridge to the south!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Танки противника выходят на гребень хребта к югу!"`
- Proposed Russian: `"Танки противника выходят на гребень хребта к югу!"`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[4].Message`; TextAsset JSON offset 113336044

### 268. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"Enemy tanks to the east, 5 kilometers out!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Танки противника к востоку, в 5 километрах!"`
- Proposed Russian: `"Танки противника к востоку, в 5 километрах!"`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[6].Message`; TextAsset JSON offset 113336044

### 269. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"Enemy tanks to the north east!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Танки противника на северо-востоке!"`
- Proposed Russian: `"Танки противника на северо-востоке!"`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[7].Message`; TextAsset JSON offset 113336044

### 270. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"Enemy tanks, south east, 3 kilometers out!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Танки противника на юго-востоке, в 3 километрах!"`
- Proposed Russian: `"Танки противника на юго-востоке, в 3 километрах!"`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[5].Message`; TextAsset JSON offset 113336044

### 271. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"Enemy troop transports spotted on the highway to the south."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"На шоссе к югу замечен транспорт противника для перевозки войск."`
- Proposed Russian: `"На шоссе к югу замечен транспорт противника для перевозки войск."`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[10].Message`; TextAsset JSON offset 113336044

### 272. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Excellent work! Return safely to base to complete the mission."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[8].Message`; TextAsset JSON offset 115497696

### 273. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"Excellent work, enemy anti-air launchers are destroyed."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Отличная работа: вражеские пусковые установки ЗРК уничтожены."`
- Proposed Russian: `"Отличная работа: вражеские пусковые установки ЗРК уничтожены."`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[15].Message`; TextAsset JSON offset 113336044

### 274. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Excellent work, every convoy vehicle has been destroyed."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[4].Message`; TextAsset JSON offset 115473564

### 275. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Excellent work, the enemy column has been neutralized. Now we need to locate and destroy the enemy's vehicle depot to prevent further attacks."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[5].Message`; TextAsset JSON offset 115418932

### 276. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Excellent work. The enemy airfield has been razed once again."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[26].Message`; TextAsset JSON offset 116745336

### 277. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Fly a T/A-30 Compass on a ground attack mission. Use missiles, rockets, bombs and guns to destroy a BDF convoy of lightly defended vehicles."`
- Already in ru.json before this pass: yes
- Before Russian: `"Управляйте самолётом T/A-30 Compass во время выполнения задачи по нанесению удара по наземным целям. Используйте ракеты, снаряды, бомбы и орудия, чтобы уничтожить колонну слабозащищённой техники Boscali."`
- Current Russian: `"Управляйте самолётом T/A-30 Compass во время выполнения задачи по нанесению удара по наземным целям. Используйте ракеты, снаряды, бомбы и орудия, чтобы уничтожить колонну слабозащищённой техники Boscali."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"01. Convoy Attack"`; `$.missionSettings.description`; TextAsset JSON offset 115473564

### 278. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Fly the A-19 Brawler in a demanding, high tempo close air support mission as BDF narrowly defend Maris Airport against a massive PALA armoured assault."`
- Already in ru.json before this pass: yes
- Before Russian: `"Управляйте штурмовиком A-19 Brawler в сложной, высокотемповой миссии авиационной поддержки, когда Boscali с трудом защищают аэропорт Марис от массированного бронетанкового наступления Примевы."`
- Current Russian: `"Управляйте штурмовиком A-19 Brawler в сложной, высокотемповой миссии авиационной поддержки, когда Boscali с трудом защищают аэропорт Марис от массированного бронетанкового наступления Примевы."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"13. Reprisal"`; `$.missionSettings.description`; TextAsset JSON offset 113336044

### 279. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Fly the SFB-81 Darkreach on a bombing mission to destroy a PALA vehicle depot on a heavily defended airbase."`
- Already in ru.json before this pass: yes
- Before Russian: `"Управляйте Бомбардировщиком SFB-81 Darkreach во время бомбардировочной миссии по уничтожению склада техники Примевы на хорошо защищенной авиабазе."`
- Current Russian: `"Управляйте Бомбардировщиком SFB-81 Darkreach во время бомбардировочной миссии по уничтожению склада техники Примевы на хорошо защищенной авиабазе."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"09. Depot Strike"`; `$.missionSettings.description`; TextAsset JSON offset 115497696

### 280. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Fly the T/A-30 Compass in an intense dogfight - your side is outnumbered 8 to 5."`
- Already in ru.json before this pass: yes
- Before Russian: `"Управляйте самолетом T/A-30 Compass в напряженном воздушном бою — ваша сторона в 8 раз слабее."`
- Current Russian: `"Управляйте самолетом T/A-30 Compass в напряженном воздушном бою — ваша сторона в 8 раз слабее."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"05. Furball"`; `$.missionSettings.description`; TextAsset JSON offset 113830540

### 281. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Form up on me and I'll lead us to the target."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[8].Message`; TextAsset JSON offset 113616164

### 282. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Good hits. We'll finish off any remaining vehicles with our guns. Remember to pull up. Don't get so fixated on shooting that you forget the terrain exists."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[18].Message`; TextAsset JSON offset 113616164

### 283. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Good shooting. Now get back to friendly territory intact."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[14].Message`; TextAsset JSON offset 117198832

### 284. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Good shooting. That's the last of them. We should clear out before any response comes our way."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[20].Message`; TextAsset JSON offset 113616164

### 285. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Good work. Next up is the dangerous bit. Continue along the highway south, use the foothills as cover."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[7].Message`; TextAsset JSON offset 116745336

### 286. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Headed to the target now."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[28].Message`; TextAsset JSON offset 113616164

### 287. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"In preparation for a large air raid, use the SAH-46 Chicane to neutralise several long range SAM systems."`
- Already in ru.json before this pass: yes
- Before Russian: `"В рамках подготовки к крупному воздушному налету используйте вертолет SAH-46 Chicane для нейтрализации нескольких ЗРК."`
- Current Russian: `"В рамках подготовки к крупному воздушному налету используйте вертолет SAH-46 Chicane для нейтрализации нескольких ЗРК."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.missionSettings.description`; TextAsset JSON offset 116745336

### 288. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Infiltrate and destroy a PALA island stronghold under the cover of a raging storm, using the the VT-7 Vagrant."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.missionSettings.description`; TextAsset JSON offset 112122504

### 289. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Land on the back of one of the ships to re-arm. You will be assisting the attack on the airfield."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[20].Message`; TextAsset JSON offset 116745336

### 290. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Mission Complete!"`
- Already in ru.json before this pass: yes
- Before Russian: `"Миссия выполнена!"`
- Current Russian: `"Миссия выполнена!"`
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[20].Message`; TextAsset JSON offset 112122504

### 291. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Mission Successful! The vehicle depot has been neutralized and your aircraft has returned to base."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[10].Message`; TextAsset JSON offset 115497696

### 292. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Naval reinforcements are enroute. ETA 10 minutes."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[48].Message`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[48].Message`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[48].Message`; TextAsset JSON offset 115979848

### 293. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Naval reinforcements have arrived."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[51].Message`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[51].Message`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[51].Message`; TextAsset JSON offset 115979848

### 294. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Once the airport is under our control, mobile AA will begin to take up positions around it."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Terminal Control Co-op as BDF"`; `$.outcomes[5].Message`; TextAsset JSON offset 111643176
  - `"Terminal Control Co-op as PALA"`; `$.outcomes[5].Message`; TextAsset JSON offset 115525280
  - `"Terminal Control"`; `$.outcomes[5].Message`; TextAsset JSON offset 117316552

### 295. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Once you've taken off, follow the highway south through the mountains."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[31].Message`; TextAsset JSON offset 116745336

### 296. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"One of the Shards has come online!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[36].Message`; TextAsset JSON offset 112122504
  - `"15. Breaking the Atoll"`; `$.outcomes[55].Message`; TextAsset JSON offset 112122504

### 297. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Our task is to interrupt them. They are without any air defence, and should be easy pickings."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[6].Message`; TextAsset JSON offset 113616164

### 298. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"PALA forces have been removed from the mainland and BDF holds the surrounding airstrips. BDF Is Victorious."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Terminal Control Co-op as BDF"`; `$.outcomes[3].Message`; TextAsset JSON offset 111643176
  - `"Terminal Control Co-op as PALA"`; `$.outcomes[3].Message`; TextAsset JSON offset 115525280
  - `"Terminal Control"`; `$.outcomes[3].Message`; TextAsset JSON offset 117316552

### 299. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"PALA forces have fortified Broken Atoll, using it as a staging ground.\nThey are directly threatening our operations. We end that threat today.\u000b--"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[9].Message`; TextAsset JSON offset 112122504

### 300. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"PALA has recently taken receipt of several R9 Stratolance batteries to prevent us from carrying out bombing raids."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[29].Message`; TextAsset JSON offset 116745336

### 301. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"PALA losses are heavy. Units are retreating."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"PALA несёт тяжёлые потери. Подразделения отступают."`
- Proposed Russian: `"PALA несёт тяжёлые потери. Подразделения отступают."`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[29].Message`; TextAsset JSON offset 113336044

### 302. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"PALA's carrier is sinking. BDF is victorious!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Carrier Duel"`; `$.outcomes[5].Message`; TextAsset JSON offset 116854308

### 303. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"PALA's forces are completely routed. Congratulations, you've managed to turn an imminent defeat into a decisive victory."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Силы PALA полностью обращены в бегство. Поздравляем: вы превратили надвигавшееся поражение в решительную победу."`
- Proposed Russian: `"Силы PALA полностью обращены в бегство. Поздравляем: вы превратили надвигавшееся поражение в решительную победу."`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[23].Message`; TextAsset JSON offset 113336044

### 304. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Prevent a column of vehicles from crossing the bridge to Boscali Island, before neutralizing the attack at its source."`
- Already in ru.json before this pass: yes
- Before Russian: `" Предотвратите коллону транспорта от пересечения моста Острова Boscali, перед тем как нейтрализововать аттаку в ее источнике"`
- Current Russian: `" Предотвратите коллону транспорта от пересечения моста Острова Boscali, перед тем как нейтрализововать аттаку в ее источнике"`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"06. Bridge Defense"`; `$.missionSettings.description`; TextAsset JSON offset 115418932

### 305. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Priority targets have been added to your HUD."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[69].Message`; TextAsset JSON offset 112122504

### 306. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Recon says there are Radar SAMs scattered throughout the surrounding valley. Stay alert for radar warnings."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[5].Message`; TextAsset JSON offset 115497696

### 307. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Remember, If you need to rearm, our special forces left behind supplies on the southern island."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[24].Message`; TextAsset JSON offset 112122504

### 308. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"SAM Site 1 is neutralised."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[8].Message`; TextAsset JSON offset 116745336

### 309. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"SAM Site 2 is neutralised."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[9].Message`; TextAsset JSON offset 116745336

### 310. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Scramble! A pair of enemy bombers has been spotted releasing cruise missiles, targeting North Boscali Airbase. Shoot the missiles down before they destroy friendly facilities."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"04. Cruise Missile Interception"`; `$.outcomes[10].Message`; TextAsset JSON offset 117801024

### 311. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Sink the ships before they get within firing range of the island!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Breakout"`; `$.outcomes[6].Message`; TextAsset JSON offset 114927384

### 312. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Special forces have scouted the island and set charges to take out the heavy air defenses.\nThey've also taken control of a resupply point, use it to if you need to!\n--"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[10].Message`; TextAsset JSON offset 112122504

### 313. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Stand down. We're surrendering Vigil Cay to the BDF."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Breakout"`; `$.outcomes[10].Message`; TextAsset JSON offset 114927384

### 314. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Stay on guard for enemy aircraft in the area. If you spot any, let your wingmen deal with them."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[6].Message`; TextAsset JSON offset 115497696

### 315. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Targets marked. Bombers are now inbound."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[25].Message`; TextAsset JSON offset 116745336

### 316. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"That Shard is out of action."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[57].Message`; TextAsset JSON offset 112122504
  - `"15. Breaking the Atoll"`; `$.outcomes[59].Message`; TextAsset JSON offset 112122504

### 317. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The Atoll's commander is taking off in an Ibis north of the island.\nThey are moving to the airfield to take cover.\nTake them out and some of the troops might lose the will to fight!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[73].Message`; TextAsset JSON offset 112122504

### 318. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The BDF Fleet Carrier has been sunk."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[43].Message`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[43].Message`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[43].Message`; TextAsset JSON offset 115979848

### 319. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The BDF is on the run, and trying to evacuate as much fuel from the area as they can."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[1].Message`; TextAsset JSON offset 115473564

### 320. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The MLRS battery is out of action. Our base should be safe!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[17].Message`; TextAsset JSON offset 112122504

### 321. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The PALA Fleet Carrier has been sunk."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[44].Message`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[44].Message`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[44].Message`; TextAsset JSON offset 115979848

### 322. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The PALA artillery have destroyed out port on Ignus. You didn't stop them in time. Mission Failed."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[31].Message`; TextAsset JSON offset 112122504

### 323. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The PALA has fortified Broken Atoll, using it as a staging ground.\n\u000bThere are three primary targets: \u000b1) the airbase in the west.\u000b2) the artillery base in the east.\u000b3) the naval garrison near the central inlet."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[46].Message`; TextAsset JSON offset 112122504

### 324. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The airbase's supplies have been destroyed.\nPALA forces won't be able to launch aircraft!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[18].Message`; TextAsset JSON offset 112122504

### 325. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The base has been hit!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"04. Cruise Missile Interception"`; `$.outcomes[6].Message`; TextAsset JSON offset 117801024

### 326. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The commander is down. It looks like some PALA forces are retreating!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[74].Message`; TextAsset JSON offset 112122504

### 327. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The commander was able to RTB and get to a secure location. \nTheir troops will keep fighting."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[77].Message`; TextAsset JSON offset 112122504

### 328. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The enemy aircraft have had time to fuel up and are taking off from the airfield!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[65].Message`; TextAsset JSON offset 112122504

### 329. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The enemy has an anti-air laser shielding the depot, although it looks to have a blind spot in the low ground to its east."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[14].Message`; TextAsset JSON offset 115418932

### 330. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The enemy has capitulated. We are victorious!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Escalation Co-op as PALA"`; `$.outcomes[46].Message`; TextAsset JSON offset 112570560
  - `"Escalation"`; `$.outcomes[46].Message`; TextAsset JSON offset 114016364
  - `"Escalation Co-op as BDF"`; `$.outcomes[46].Message`; TextAsset JSON offset 115979848

### 331. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The enemy installation has been removed, mission accomplished!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Altercation Co-op as BDF"`; `$.outcomes[2].Message`; TextAsset JSON offset 111545216
  - `"Altercation Co-op as PALA"`; `$.outcomes[2].Message`; TextAsset JSON offset 113732596
  - `"Altercation"`; `$.outcomes[2].Message`; TextAsset JSON offset 113918420

### 332. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"The enemy is now past K92. They're pushing straight through to the airport. Do not let them reach it!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Противник прошёл K92 и наступает прямо на аэропорт. Не дайте ему добраться до него!"`
- Proposed Russian: `"Противник прошёл K92 и наступает прямо на аэропорт. Не дайте ему добраться до него!"`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[12].Message`; TextAsset JSON offset 113336044

### 333. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The first target area is the supply depot just over this crest. We expect no significant resistance here."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[5].Message`; TextAsset JSON offset 116745336

### 334. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"The last of us are pulling out now."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Сейчас отходят последние наши подразделения."`
- Proposed Russian: `"Сейчас отходят последние наши подразделения."`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[25].Message`; TextAsset JSON offset 113336044

### 335. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The naval base is down, good work!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[19].Message`; TextAsset JSON offset 112122504

### 336. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The storm is starting to lift. Move fast and take out the targets before they can react.\u000b\u000bGood Luck!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[11].Message`; TextAsset JSON offset 112122504

### 337. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"The vehicles should be targetable now. Select them as targets."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[16].Message`; TextAsset JSON offset 113616164

### 338. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"There are three primary targets:\r\nAirbase: Destroy fuel and supplies to ground enemy fighters.\r\nCentral Inlet: Strike the base before the Shards come online.\nEast: Neutralize the MLRS battery before it destroys our base.\u000b--"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[0].Message`; TextAsset JSON offset 112122504

### 339. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"There's an enemy SAM site watching the valley on the other side. Best keep out of its sight. Follow the coast if needed."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[13].Message`; TextAsset JSON offset 115418932

### 340. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"They are currently powered down, but not for long. \nAttack the depot there to prevent them from launching."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[14].Message`; TextAsset JSON offset 112122504

### 341. STATIC_MISSION_MESSAGE — TRANSLATE

- Exact English: `"They've got tanks approaching on all sides. We're going to pull out before we become encircled."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: `"Танки противника подходят со всех сторон. Отходим, пока нас не окружили."`
- Proposed Russian: `"Танки противника подходят со всех сторон. Отходим, пока нас не окружили."`
- Runtime safety: Display-only proven; exact lookup only when feed content matches the whole source
- Action: TRANSLATE
- Provenance:
  - `"13. Reprisal"`; `$.outcomes[8].Message`; TextAsset JSON offset 113336044

### 342. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Today we'll be destroying all of them, and carrying out a bombing raid."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[30].Message`; TextAsset JSON offset 116745336

### 343. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Today we're striking a vehicle depot located on the enemy's airbase."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"09. Depot Strike"`; `$.outcomes[15].Message`; TextAsset JSON offset 115497696

### 344. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Use the Alkyon AB-4 to penetrate heavy enemy air defences and strike a BDF naval base."`
- Already in ru.json before this pass: yes
- Before Russian: `"Используйте Alkyon AB-4, чтобы прорвать мощную противовоздушную оборону противника и нанести удар по военно-морской базе BDF."`
- Current Russian: `"Используйте Alkyon AB-4, чтобы прорвать мощную противовоздушную оборону противника и нанести удар по военно-морской базе BDF."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"14. To Sink a Carrier"`; `$.missionSettings.description`; TextAsset JSON offset 117198832

### 345. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Use the FS-12 Revoker to intercept a volley of cruise missiles launched at your base from Primeva."`
- Already in ru.json before this pass: yes
- Before Russian: `"Используйте истребитель FS-12 Revoker для перехвата залпа крылатых ракет, запущенных по вашей базе с Примевы."`
- Current Russian: `"Используйте истребитель FS-12 Revoker для перехвата залпа крылатых ракет, запущенных по вашей базе с Примевы."`
- Proposed Russian: —
- Runtime safety: Not selected; display route/context requires separate review
- Action: MANUAL_REVIEW
- Provenance:
  - `"04. Cruise Missile Interception"`; `$.missionSettings.description`; TextAsset JSON offset 117801024

### 346. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Warning! Our base has taken heavy damage from the PALA artillery. \u000bTake out that site ASAP or our base will be destroyed!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[67].Message`; TextAsset JSON offset 112122504

### 347. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"We need to re-establish control of the strait. Sink some BDF ships!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Breakout"`; `$.outcomes[1].Message`; TextAsset JSON offset 114927384

### 348. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"We'll be targeting a supply point for the R9 systems as well as several active batteries. Staying low and fast will be key."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[32].Message`; TextAsset JSON offset 116745336

### 349. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"We're back on the offensive - excellent work!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Breakout"`; `$.outcomes[15].Message`; TextAsset JSON offset 114927384

### 350. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"We're going to open with bombs. Switch weapons to your PAB-250s, and start a shallow climb to 600m (2000ft)."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"02. Round Up"`; `$.outcomes[15].Message`; TextAsset JSON offset 113616164

### 351. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"We're losing factories! If this keeps up we're done for!"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"Breakout"`; `$.outcomes[17].Message`; TextAsset JSON offset 114927384

### 352. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Well done, the threat has been neutralized."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"04. Cruise Missile Interception"`; `$.outcomes[1].Message`; TextAsset JSON offset 117801024

### 353. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Well done, we won't be seeing more vehicle threats any time soon."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"06. Bridge Defense"`; `$.outcomes[7].Message`; TextAsset JSON offset 115418932

### 354. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Whichever route you choose, you should support your allies by jamming the blockade while on approach."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[11].Message`; TextAsset JSON offset 117198832

### 355. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Work quickly - it looks like PALA is scrambling jets from the target airfield."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"03. Point Blank"`; `$.outcomes[14].Message`; TextAsset JSON offset 116745336

### 356. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"You are cleared for launch. We're pushing you right into the teeth of this storm. \nVisibility is near zero, but it is the only thing masking your approach. \nGet airborne and push to the first waypoint.\r\u000b--"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"15. Breaking the Atoll"`; `$.outcomes[7].Message`; TextAsset JSON offset 112122504

### 357. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Your aircraft's visual sensors can detect ground vehicles within a range of 6km. We are to locate and destroy the convoy."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"01. Convoy Attack"`; `$.outcomes[3].Message`; TextAsset JSON offset 115473564

### 358. STATIC_MISSION_MESSAGE — MANUAL_REVIEW

- Exact English: `"Your primary target is an Annex Class Carrier currently situated inside a cove on the westmost point of Ignus Major."`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only path traced; translation not language-reviewed; aggregated-feed limitation
- Action: MANUAL_REVIEW
- Provenance:
  - `"14. To Sink a Carrier"`; `$.outcomes[9].Message`; TextAsset JSON offset 117198832

### 359. DYNAMIC_MISSION_MESSAGE — NEEDS_RUNTIME_SUPPORT

- Symbolic producer format (not a literal dictionary key): `"<color=#{RGBA8}>{PlayerDisplayName} joined the game</color>"`
- Already in ru.json before this pass: no
- Before Russian: —
- Current Russian: —
- Proposed Russian: —
- Runtime safety: Display-only; GetDisplayName + literal suffix + RGBA color; user/chat isolation not available to generic lookup
- Action: NEEDS_RUNTIME_SUPPORT
- Provenance:
  - `"Generic multiplayer notice (not narrative)"`; `MessageManager.JoinMessage; StringHelper.AddColor`

## Final 3.6.4 sign-off

The dynamic join row above is still deferred. Only the 13 reviewed authored mission literals gained
producer-level support. The exact K92 source now translates independently before other feed lines
are appended; final TMP translation leaves all reviewed Russian values intact in compiled fixtures.
All current quality gates passed, with live host/client testing still required.
No commit, push, publication or real-game installation/modification was performed.

**MISSION_RUNTIME_READY_FOR_GAME_TEST**
