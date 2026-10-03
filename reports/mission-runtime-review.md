# Mission runtime review — 3.6.4 development candidate

Final verification date: 2026-10-04 (Europe/Moscow); the pass began on 2026-10-03.

Verdict: **MISSION_RUNTIME_READY_FOR_GAME_TEST**.

All required static/automated gates passed. This is readiness for user game testing, not a claim
that a live Unity/host/client session has been executed. No commit, push, publication or real-game
installation was performed. Join/leave and other deferred paths are deliberately not supported here.

## Recovered WIP and scope

Repository: `W:/inwork/NuclearOption-RussianLocalization`.
Branch: `fix/mission-messages-russian`.
HEAD/baseline: `fde844a62ed6b19e2c24d10931c0b54530a6d41b` (unchanged).

The current dirty tree was accepted and inventoried before resuming. Exactly 15 expected WIP paths
were present; no unexpected path was found. Nothing was cleaned/reset/stashed/checked out/discarded.

| Recovered file | Assessment |
| --- | --- |
| `config/localization-audit.json` | Only expected count 3716 → 3729; preserved during runtime pass. |
| `localization/ru.json` | Exactly 13 reviewed mission additions; byte-identical throughout runtime work. |
| `reports/localization-audit.md` | Only entry-count refresh against baseline; preserved. Fresh audits use ignored output paths. |
| `config/mission-messages.json` | Reviewed 13-message manifest and pinned provenance; preserved. |
| `reports/mission-messages-audit.md` | Complete earlier inventory; retained in full, with an additive current-status header/sign-off. |
| `tools/audit-mission-messages.py` | Original source discovery/data QA tool preserved; baseline runtime prose is historical. |
| `tools/test-mission-messages.py` | Existing 11 tests preserved, not weakened. |
| `CHANGELOG.md` | Intentional 3.6.4 candidate entry: 13 data additions, producer support, exclusions. |
| `README.md`, `README_RU.md` | Intentional candidate version/scope/package documentation. |
| `src/LocalizationPatch/LocalizationPatch.csproj` | Main candidate version 3.6.4 / assembly/file version 3.6.4.0. |
| `src/LocalizationPatch/Plugin.cs` | Reviewed allowlist, local display Prefix, isolated registration, three version strings. |
| `tools/inspect-mission-runtime.ps1` | Pinned read-only metadata/IL evidence and producer safety checks. |
| `tools/mission-runtime-fixtures.cs` | Offline fake producers/network routes; real production-method extracts are injected. |
| `tools/test-mission-runtime.py` | Builds/runs real Harmony fixtures, checks allowlist and exact old-logic regression boundary. |

Ignored recovery/checkpoints:

- `.verification/mission-messages-recovery-20261003-c751341ef391/`: original seven-file recovery.
- `.verification/mission-runtime-3.6.4-20261003/before/`: pre-runtime WIP, sources, DLLs, docs and 3.6.3 ZIP.
- `.verification/mission-runtime-3.6.4-20261003/resume-current/`: complete 15-file runtime WIP and intermediate DLLs at the latest resume.
- All final builds, fixtures and evidence remain under the same ignored runtime checkpoint.

## Safe producer and exact Harmony change

**SAFE_TO_PATCH, only for the reviewed allowlist:**

```text
declaring type: MissionMessages
private instance System.Void ShowMessgeLocal(System.String message,
                                            System.Boolean playsound,
                                            FactionHQ filterFaction)
Harmony Prefix: KoreanPatch.Plugin.MissionMessages_Local_Patch.Prefix(ref string __0)
```

The spelling `ShowMessgeLocal` is the actual game method. Reflection selects its exact declared,
private, instance three-argument signature and verifies a void return. An unavailable signature
causes a startup warning and skips this patch; no heuristic fallback is installed.

The Prefix replaces argument 0 only. It calls `TranslateMissionMessage`, which requires Enabled,
a live Plugin Instance, an exact ordinal match in the compiled 13-source allowlist, and an exact
dictionary key before calling the existing `Translate`. It does not Trim unknown messages, invoke
UI patterns on unknown mission text, change flags/faction, or mutate stored mission fields.
The compiled allowlist is checked against `config/mission-messages.json` by the runtime test runner.
No Russian text or alternate translations are hardcoded in the runtime hook.

The inspected local producer has only these calls: `IsLocalFaction`, `GameplayUI.GameMessage(string)`
and `PlaySound`. It contains no field/argument writes, callbacks, identifiers or serialization.
Its two callers are the original `ShowMessage` dispatcher and the non-server RPC receiver.

### Other traced producers — intentionally not patched

| Type / signature | Source, composition and execution context | Decision / safety reason |
| --- | --- | --- |
| `NuclearOption.SavedMission.Outcomes.ShowMessageOutcome.Complete(Objective)` | Reads its saved/copied literal Message field; computes faction and sound separately; calls the mission dispatcher with sendToClients=true. | No patch. Source fields, UniqueName and objective state retained. All 13 allowlisted strings are literal Reprisal ShowMessage outcomes. |
| `MissionMessages.ShowMessage(string message, bool playsound, FactionHQ faction, bool sendToClients)` | Original English dispatcher argument used for local display and later RPC transmission. | No patch: never localize the shared sender argument. |
| `MissionMessages.RpcShowMessage(string message, bool playsound, FactionHQ faction)` | Mirage-generated sender writes original string, boolean and faction into network payload. | No patch: serialization stays original. |
| `MissionMessages.UserCode_RpcShowMessage_-186615428(string, bool, FactionHQ)` | Received original values; returns when IsServer, otherwise invokes the private local display method. | No patch here; shared local callee covers non-server clients after deserialization. |
| `MessageManager.HQMessageInternal(FactionHQ HQ, string message)` | Local objective/escalation/status notification; calls delayed UI display, then reads message.Contains("Tactical") / Contains("Strategic") to select faction music. | MUST NOT PATCH: display string has a functional read-back. HQ RPC routes and other dynamic status messages are deferred. |
| `MessageManager.JoinMessage(NuclearOption.Networking.Player joinedPlayer)` | GetDisplayName(context=0) + literal " joined the game", then AddColor with ChatSystem color, then UI feed. Invoked by Player.ShowJoinMessage after name resolution. | Deferred. No separate display-string argument; no producer IL rewrite or final-feed suffix matching in 3.6.4. Names and colors remain original. |
| `MessageManager.DisconnectedMessage(NuclearOption.Networking.Player player)` | GetDisplayName(context=0) + literal " Disconnected"; invoked by Player.OnStopClient, then UI feed. | Deferred; dynamic names/control data untouched. |
| `ChatBox.SendChat()` → `NuclearOption.Chat.ChatManager.SendChatMessage(string, bool)` | User input, allies/all-chat control and network send. | No interception. User-generated text is not routed through the mission producer. |
| `NuclearOption.Chat.ChatManager.UserCode_TargetReceiveMessage_1307761090(INetworkPlayer, string message, Player player, bool allChat)` | Client receives user text; mute/filter/rich-text sanitization, colored name/header and UI feed; optional TTS. Server-message receiver similarly bypasses mission producer. | No patch; chat/tags/user names/TTS unchanged by this addition. |
| `GameplayUI.GameMessage(string)` / `MessageUI.GameMessage(string)` | Shared UI consumer; LF splitting and display expiry, then MessageFeed.Enqueue. | No patch: shared with chat/system text. |
| `MessageFeed.RefreshUI()` | Joins queued lines using LF; calls TMP_Text.SetText(StringBuilder). | No patch/regex/line matcher: producer translation happens before this shared composition. |

Display-field references in the entire inspected assembly are limited to feed construction and UI
writes; no localized TMP value is read back as a mission identifier, callback key or network state.
This conclusion applies to the pinned local build, not unreviewed future game versions.

## Exact network/value flow

Fresh Cecil evidence: `runtime-inspection/producer-evidence.json` and `producer-evidence.il.txt`
inside the ignored runtime checkpoint. Game assembly SHA256:
`EB3B93BDAEC37DD7B3BAB72F801A2C84E5BE2AE3C559F39251E2320AE6B11CCC`.

1. `ShowMessageOutcome.Load` copies `ShowMessageSavedOutcome.Message` into its original Message field.
   `Complete` loads that field at IL_0019, then calls `MissionMessages.ShowMessage` at IL_002b.
2. Static `MissionMessages.ShowMessage` keeps original message in **its own argument 0**.
   IL_000e loads it for the local call at **IL_0011**, along with sound/faction.
3. `ShowMessgeLocal` receives message **by value**, not `ref`/`out`. Harmony's `ref __0` rewrites only
   that callee invocation's local argument slot. The original immutable string in the dispatcher's
   slot/source field is not modified. Its UI call now receives Russian text before composition.
4. Back in `ShowMessage`, **IL_001e reloads original argument 0** and **IL_0021 calls RpcShowMessage**.
   This is a later original-value load, not serialization of the callee's replacement.
5. The sender loads `message` at **IL_0032** and calls `StringExtensions.WriteString` at **IL_0036**;
   the unaltered playsound and faction values are serialized separately.
6. The client skeleton reads original string at IL_000a plus bool/faction and dispatches to
   `UserCode_RpcShowMessage_-186615428`. That method returns on IsServer (IL_0001/IL_0008), otherwise
   calls ShowMessgeLocal at **IL_000d**. Each client applies its own local dictionary/Enabled policy.

Thus host local display can be Russian while the transmitted source remains English. There is no
localization-dependent mission/network identity. Faction routing and sound controls are unchanged.
Static IL and Harmony fixtures prove the value isolation; a real host/client session remains required.

## Exact 13-message allowlist and preserved Russian values

All are `13. Reprisal` literal `ShowMessage.Message` outcomes in the pinned local resource data.
Fresh source extraction verifies all 13; none is an identifier or variable-binding payload.
The five saved outcome fields are Message, PlaySound, ObjectiveFactionOnly, UniqueName and Type.

| Exact English source | Russian dictionary value |
| --- | --- |
| Enemy tanks cresting the ridge to the south! | Танки противника выходят на гребень хребта к югу! |
| Enemy tanks, south east, 3 kilometers out! | Танки противника на юго-востоке, в 3 километрах! |
| Enemy tanks to the east, 5 kilometers out! | Танки противника к востоку, в 5 километрах! |
| Enemy tanks to the north east! | Танки противника на северо-востоке! |
| They've got tanks approaching on all sides. We're going to pull out before we become encircled. | Танки противника подходят со всех сторон. Отходим, пока нас не окружили. |
| A large enemy force is preparing to seize this airport, approaching via K92. You are to support K92's defenders as they perform a fighting retreat, and attrit as many enemy vehicles as possible. | К этому аэропорту через K92 приближаются крупные силы противника, готовящиеся его захватить. Поддержите защитников K92, отходящих с боем, и выведите из строя как можно больше вражеской техники. |
| Enemy troop transports spotted on the highway to the south. | На шоссе к югу замечен транспорт противника для перевозки войск. |
| The enemy is now past K92. They're pushing straight through to the airport. Do not let them reach it! | Противник прошёл K92 и наступает прямо на аэропорт. Не дайте ему добраться до него! |
| Be advised, PALA is attempting to set up SAM sites in the southern hills overlooking Maris Airport. Find and destroy them before they lock down the airspace! | Внимание: PALA пытается развернуть ЗРК на южных холмах над Maris Airport. Найдите и уничтожьте их, пока они не перекрыли воздушное пространство! |
| Excellent work, enemy anti-air launchers are destroyed. | Отличная работа: вражеские пусковые установки ЗРК уничтожены. |
| PALA's forces are completely routed. Congratulations, you've managed to turn an imminent defeat into a decisive victory. | Силы PALA полностью обращены в бегство. Поздравляем: вы превратили надвигавшееся поражение в решительную победу. |
| The last of us are pulling out now. | Сейчас отходят последние наши подразделения. |
| PALA losses are heavy. Units are retreating. | PALA несёт тяжёлые потери. Подразделения отступают. |

Localization vs fde844a: **3716 → 3729**, added 13, removed 0, renamed 0, changed existing values 0.
No new data changes were made during the runtime pass; every Encyclopedia/stabilization value and
the current ru.json bytes were preserved. Both K92 tokens in the user example remain ASCII K92.

Current ru.json SHA256: `3D388BDB3EB5231884E17EBC2FFFC45D874905ADE124EEF6705A2EC72DE2D1D7`.

## Tests, idempotence and version

Final fresh results:

| Check | Result |
| --- | --- |
| Compiled production extracts with real Harmony against fake local/network/chat producers | **13/13 PASS**, exit 0 |
| Existing mission-message audit/data tests | **11/11 PASS**, exit 0; unchanged tests |
| Existing general localization QA tests | **11/11 PASS**, exit 0; unchanged tests |
| Normal localization audit | **PASS**, exit 0 |
| Strict localization audit | **PASS**, exit 0 |
| Entry count / JSON / duplicate exact keys | **PASS**, 3729 / valid / 0 |
| Protected identities / designations / proper names / placeholders / TMP tags | **PASS**, each violation count 0 |
| Existing installer regression scenarios | **7 result groups PASS**, repo-local mock games only |
| git diff --check | **PASS**, exit 0 |

The runtime fixture compiler extracts actual registration, Prefix, mission helper, Translate,
TryPatternMatch and JSON parser definitions from Plugin.cs. It does not hand-reimplement translation
logic in Python. All 13 Russian values are tested against actual Translate using the full current
dictionary: each is unchanged on a second pass. Reviewed values remain intact in a composed feed.
Unknown messages, whitespace variants and rich-text-wrapped variants are left unchanged by the
producer hook. Disabled/uninitialized/missing-dictionary paths fail open. No global guard/redesign
of Translate was necessary. Actual Harmony registration modifies only the private local method.

Fixture network/chat producers are mocked models of inspected IL, not execution of game code or a
live multiplayer test. The pre-existing generic TMP hooks are unchanged; their historical ability
to match a user string identical to a dictionary key is not fixed or expanded by this scoped pass.

Main active version: BepInPlugin **3.6.4**, startup/GUI **3.6.4**, project Version **3.6.4**,
AssemblyVersion/FileVersion **3.6.4.0**, genuine ProductVersion
`3.6.4+fde844a62ed6b19e2c24d10931c0b54530a6d41b`.
The independently versioned, functionally unchanged dropdown stays **1.0.0**.

Existing unrelated audit findings remain CRITICAL 0 / HIGH 116 / MEDIUM 49 / INFO 13.
Trim-unsafe 112, trim collisions 4, newline warnings 2 and all other stylistic counts are unchanged.

## Clean builds and accepted dropdown metadata difference

Both projects were built offline into a **new, empty isolated output tree** at
`.verification/mission-runtime-3.6.4-20261003/final-build/`; no deletion/working-tree cleanup was used.
Each build completed with **0 warnings and 0 errors**, warnings treated as errors.
No Git revision override or old-stamp reproduction was used for these final builds.
Both final DLLs were copied byte-for-byte to the canonical repository build-output locations.

| Artifact | Previous SHA256 | Final SHA256 |
| --- | --- | --- |
| LocalizationPatch.dll | `A23F92C8CA807962793DD0534FDE2A08452BBE975EBE036819BA2174551258CC` | `CBA51FB51BC5984DB8A46BAF10B4F142799F8FB33BCE44C48E6FE772F0F9ABEC` |
| LocalizationPatchDropdown.dll | `C63326A4FE4C05C4A46F6593224D4D43C3F24A47700C253E41F8D38AFE51C4A6` | `7D94BE72CD7652534640B73B74211812E9DD05CA6E8249EDB2452C6416AD62A7` |

Dropdown source and project are unchanged from fde844a (Git-normalized text); their bytes also match
the pre-runtime snapshot hashes. Source SHA256:
`5C673F1D5C21FB0E24D8D66EFC494CB6D9D3D85A1085818976937F2734EB1214`.
Project SHA256: `ABF6C6968E18E017CD341733C15E5A14AFE1D8BB0F9866B54EB9D802FD648B6B`.

**Dropdown IL/API equivalence PASS:** all **299 ordered comparison records** are identical:
type/member/parameter/access/API signatures, method IL, locals, exception handlers, non-build
attributes, assembly references and module runtime properties. No resources were present.
Only AssemblyInformationalVersion was excluded as explicit build metadata; MVID/debug identity
are separately recorded in `dropdown-equivalence.json` in the checkpoint.

Old informational version: `1.0.0+8594a28b36572b2393921bee26346bcdd4cc82a1`.
New genuine version: `1.0.0+fde844a62ed6b19e2c24d10931c0b54530a6d41b`.
The fresh isolated path also changes deterministic PDB/debug path/checksum/MVID. These explain
the binary difference without any functional change; accepted under the updated dropdown decision.
No dropdown source/project was edited. Earlier canonical/stamp-investigation binaries are retained
in ignored checkpoints and are **not** final/package inputs; no further stamp pinning was attempted.

## Package and exact contents

First validated isolated package: `isolated-package/NuclearOption-RussianLocalization-v3.6.4.zip`
inside the checkpoint. Then created final local release:
`release/NuclearOption-RussianLocalization-v3.6.4.zip`.

Both are byte-identical; SHA256:
`BE09E9CC57238D8A7E18EB9EB510F042F184B408429EC1E211B20DF5BB2DE745`.

Exact archive listing (four relative member paths, no directory entries):

```text
BepInEx/plugins/LocalizationPatch/LocalizationPatch.dll
BepInEx/plugins/LocalizationPatch/LocalizationPatchDropdown.dll
BepInEx/plugins/LocalizationPatch/ru.json
BepInEx/plugins/LocalizationPatch/Tektur-Reg.ttf
```

ZIP integrity and exact entry count/name/uniqueness checks passed programmatically. Each embedded
file was byte-compared to its final input; ru.json equals current canonical localization, and both
DLL hashes equal the final clean builds/canonical build outputs. No backups, logs, tests, reports,
QA configuration, dumps, bin/obj tree, game/BepInEx dependency assemblies, user config, absolute
archive paths or 3.6.1/3.6.2 artifacts are included. Normal DLL debug metadata is not a packaged PDB.
The existing 3.6.3 release is untouched: SHA256
`24427F0482BABFEE0B593B516F1362634BF0F1855C938DA8264989A9BF1C3628`.

## Static regression gates

The test runner strips only the exact new reviewed field/helper/registration/Prefix plus three
version substitutions, then compares all remaining Plugin.cs text to fde844a. It matches exactly.

| Forbidden regression / preservation check | Result |
| --- | --- |
| No parent RectTransform resizing | PASS |
| No global font-size reduction policy | PASS |
| No cockpit hierarchy scanning | PASS |
| No broad/new ancestry matching | PASS; existing DialogueBox title safeguard untouched |
| No final-feed regex/line translation | PASS |
| No arbitrary chat producer interception | PASS; no new chat translation path |
| No new per-frame work/hierarchy scans/FindObjectsOfTypeAll calls | PASS |
| No unconditional keypress debug logging | PASS; only one normal patch-registration startup info/warning path added |
| Encyclopedia AutoFit and parent panels unchanged | PASS |
| Existing OnEnable/periodic/fast TMP translation and logging cleanup retained | PASS |
| No activated 3.6.1/3.6.2 behavior | PASS |

## Deferred scope and live game-test limitations

- Join/leave: English, including `<color=#{RGBA8}>{PlayerDisplayName} joined the game</color>`;
  no name translation or suffix matcher.
- Chat/server chat/TTS: no producer hooks. Existing general TMP behavior retained, not redesigned.
- HQMessageInternal/escalation/status/counters: deferred because read-back/control semantics require separate review.
- Mission Editor, Did-you-know/tutorial hints and dialogue/glyph-binding expansion: deferred.
- Cockpit/HUD/MFD: incomplete, outside this pass.
- Other mission strings/briefing summaries: inventory only; no blanket translation or full coverage claim.
- A custom mission reusing an identical reviewed display literal will receive the same translation;
  this is exact display-text scope, not hierarchy/mission-name identification.
- MessageUI derives feed display expiry from character count; translating before it means Russian
  length now determines that UI lifetime. This is a display-only consequence, not a mission timer,
  objective identity, network value or sound/faction change. Verify queue clipping/readability in game.
- Confirm the startup producer-patch log, K92 alongside concurrent lines, font/glyphs, faction/sound,
  host/client English payload isolation and unchanged chat/join behavior in the pinned game build.

## Quality gates

| Required gate | Result |
| --- | --- |
| Safe producer isolated | PASS |
| 13-message allowlist only | PASS |
| K92 translated | PASS in real-Harmony production-method fixtures; live test pending |
| Callsigns preserved | PASS |
| Original RPC text unchanged | PASS: fresh IL + fixture argument isolation |
| No localization-dependent network state | PASS for inspected pinned path |
| No arbitrary chat translation added | PASS |
| Join/leave deferred | PASS |
| No double translation | PASS |
| Protected identities | PASS |
| Designation/proper-name checks | PASS |
| Placeholders/TMP tags | PASS |
| Strict QA | PASS |
| All automated tests | PASS: 35 tests + mock installer groups |
| Build | PASS: both 0 warnings / 0 errors |
| Dropdown functional equivalence | PASS |
| Package | PASS |
| Runtime regression scan | PASS |
| git diff --check | PASS |
| Real game untouched | PASS: read-only evidence/references; installer runs only in repo mocks |
| Nothing published | PASS; no commit/push/publish/install |

## Git handoff

`git diff --stat` (tracked paths only; new reports/tools remain untracked):

```text
 CHANGELOG.md                                   |  7 +++
 README.md                                      |  8 +--
 README_RU.md                                   |  2 +-
 config/localization-audit.json                 |  2 +-
 localization/ru.json                           |  2 +-
 reports/localization-audit.md                  |  2 +-
 src/LocalizationPatch/LocalizationPatch.csproj |  8 +--
 src/LocalizationPatch/Plugin.cs                | 72 ++++++++++++++++++++++++--
 8 files changed, 88 insertions(+), 15 deletions(-)
```

`git status --short`:

```text
 M CHANGELOG.md
 M README.md
 M README_RU.md
 M config/localization-audit.json
 M localization/ru.json
 M reports/localization-audit.md
 M src/LocalizationPatch/LocalizationPatch.csproj
 M src/LocalizationPatch/Plugin.cs
?? config/mission-messages.json
?? reports/mission-messages-audit.md
?? reports/mission-runtime-review.md
?? tools/audit-mission-messages.py
?? tools/inspect-mission-runtime.ps1
?? tools/mission-runtime-fixtures.cs
?? tools/test-mission-messages.py
?? tools/test-mission-runtime.py
```

Final verdict: **MISSION_RUNTIME_READY_FOR_GAME_TEST**
