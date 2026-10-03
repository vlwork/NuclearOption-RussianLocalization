# Encyclopedia description shortening

## Scope

This pass changes only ten Russian Encyclopedia description values: both stored A-19 Brawler descriptions, FS-20 Vortex, SFB-81 Darkreach, HLT Mobile Artillery, and five other long equipment descriptions. Source keys and all 3716 entries remain intact. English names/designations, specifications and operational roles are preserved. No hints, mission messages, UI labels or Mission Editor strings are edited.

Overflow selection is based on the user's observations and a static length review, not measured panel dimensions. No extracted Encyclopedia source export or in-game rendering is available in this repository. Equipment-description prose is distinguishable from the adjacent hints and mission text; those other contexts are excluded. Shorter text reduces likely overflow but needs in-game confirmation at the user's resolution and UI scale.

## Exact reviewed changes

### 1. A-19 Brawler — current description

Source key:
```text
The Brawler is a reliable and rugged platform built to carry large quantities of precision weapons. Advanced propfan engines combine endurance with respectable speed, while redundant control surfaces, isolated engines, and heavy cockpit armor provide excellent survivability. The A-19 is in its element when attacking convoys of vehicles, distributed short-range air defenses, or vessels operating in coastal waters.
```

Before:
```text
Brawler — надёжная и прочная платформа, созданная для несения большого количества высокоточного вооружения. Перспективные винтовентиляторные двигатели сочетают выносливость с достойной скоростью, а дублированные рулевые поверхности, изолированные двигатели и тяжёлая бронезащита кабины обеспечивают отличную живучесть. A-19 в своей стихии при атаке колонн техники, рассредоточенных зенитных комплексов малой дальности или кораблей, действующих в прибрежных водах.
```

After:
```text
A-19 Brawler надёжен, прочен и несёт много высокоточного оружия. Современные винтовентиляторные двигатели дают длительный полёт и хорошую скорость. Дублированные рули, изолированные двигатели и тяжёлая броня кабины повышают живучесть. Эффективен против колонн техники, рассредоточенных средств ПВО малой дальности и кораблей в прибрежных водах.
```

Reason: Removes carrier/payload circumlocution and the idiom «в своей стихии»; retains endurance, speed, survivability features and all three target categories.

### 2. A-19 Brawler — older stored description

Source key:
```text
The A-19 Brawler is a heavily armed and heavily armored dual prop-fan aircraft, specialized in Close Air Support missions. Its large weapon payload of bombs, missiles and rockets, as well as its dual 35mm autocannons make it a very dangerous threat to any enemy vehicle.
```

Before:
```text
A-19 Brawler — тяжеловооружённый и тяжелобронированный двухвинтовентиляторный штурмовик, специализирующийся на непосредственной авиационной поддержке. Большая боевая нагрузка из бомб, ракет и НАР, а также спаренные 35-мм автопушки делают его крайне опасным для любой вражеской техники.
```

After:
```text
A-19 Brawler — штурмовик с мощным вооружением, тяжёлой бронёй и двумя винтовентиляторными двигателями для непосредственной авиаподдержки. Большой боекомплект бомб, ракет и НАР и две 35-мм автопушки опасны для любой техники противника.
```

Reason: Replaces long participial phrasing with direct attributes; retains heavy armament/armor, two engines, close air support, payload types and two 35-mm guns. This stored equipment-description variant is retained, not removed or merged.

### 3. FS-20 Vortex

Source key:
```text
A compact and advanced multirole fighter, the Vortex is capable of operating vertically from small carriers and remaining undetected thanks to outstanding stealth characteristics. While fast, agile, and stealthy when lightly loaded, these characteristics can suffer when carrying a heavy payload of weapons.
```

Before:
```text
Компактный и передовой многоцелевой истребитель Vortex способен вертикально взлетать с малых авианосцев и оставаться незамеченным благодаря выдающимся характеристикам малозаметности. При лёгкой загрузке он быстр, манёврен и малозаметен, однако с тяжёлой боевой нагрузкой эти характеристики ухудшаются.
```

After:
```text
Vortex — компактный передовой многоцелевой истребитель для вертикального взлёта и посадки на малых авианосцах. При лёгкой нагрузке быстр, манёврен и крайне малозаметен; тяжёлое вооружение ухудшает эти качества.
```

Reason: Removes repeated explanations of stealth and payload; preserves vertical carrier operations and the speed/maneuverability/stealth trade-off.

### 4. SFB-81 Darkreach

Source key:
```text
Featuring powerful engines, a stealthy silhouette, and 4 large internal weapon bays, the SFB-81 Darkreach is a formidable bomber capable of deploying both conventional and nuclear weapons. Its blended wing design allows the Darkreach to conduct operations in a variety of flight regimes, from low-altitude penetrating strikes to standoff strategic bombardment.
```

Before:
```text
Оснащённый мощными двигателями, малозаметным силуэтом и 4 крупными внутренними оружейными отсеками, SFB-81 Darkreach — грозный бомбардировщик, способный применять как обычное, так и ядерное вооружение. Конструкция «летающее крыло» позволяет Darkreach проводить операции в различных режимах полёта — от маловысотных прорывных ударов до стратегических бомбардировок с дальней дистанции.
```

After:
```text
SFB-81 Darkreach — малозаметный бомбардировщик с мощными двигателями и четырьмя большими внутренними отсеками для обычного и ядерного оружия. Интегральная компоновка крыла и фюзеляжа подходит для маловысотных прорывных ударов и стратегических бомбардировок с большой дистанции.
```

Reason: Removes introductory and repeated-name phrasing while retaining four large internal bays, engine power, stealth, both weapon categories and both flight/attack regimes. «Интегральная компоновка крыла и фюзеляжа» follows the source's blended-wing design rather than adding a flying-wing claim.

### 5. HLT Mobile Artillery

Source key:
```text
This advanced and highly mobile long-range artillery system fires 155mm laser guided shells. Capable of bombarding targets 40km away at a sustained 5 rounds per minute, the HLT Mobile Artillery will frequently relocate to avoid return fire.
```

Before:
```text
Современная высокомобильная дальнобойная артиллерийская система, стреляющая 155-мм снарядами с лазерным наведением. Способна обстреливать цели на дальности до 40 км с устойчивым темпом 5 выстрелов в минуту и часто меняет позицию, чтобы избежать ответного огня.
```

After:
```text
HLT Mobile Artillery — современная высокомобильная дальнобойная артсистема. Ведёт огонь 155-мм снарядами с лазерным наведением на 40 км с устойчивым темпом 5 выстр./мин. Часто меняет позицию, избегая ответного огня.
```

Reason: Uses concise artillery terminology and a standard rate abbreviation; explicitly retains the English unit name, 155-mm laser guidance, 40-km range, sustained rate and counterfire avoidance.

### 6. UH-90 Ibis

Source key:
```text
Designed for a PALA fast vertical lift program in the 2050s, the UH-90 was conceptualized as a medium-sized compound utility helicopter, but has since been fitted with numerous weapon stations allowing it to occupy a gunship role. Featuring a coaxial rigid rotor system and two reversible turbine-electric ducted fans in pusher configuration, the Ibis can rapidly reach high cruising speeds before decelerating to a vertical landing in less than 30 seconds.
```

Before:
```text
Разработанный в рамках программы PALA по скоростному вертикальному подъёму 2050-х годов, UH-90 был задуман как средний многоцелевой вертолёт комбинированной схемы, однако впоследствии получил многочисленные оружейные узлы, позволяющие выполнять роль ударного вертолёта. Оснащённый соосной жёсткой несущей системой и двумя реверсивными турбоэлектрическими вентиляторами в канальных мотогондолах толкающей схемы, Ibis способен быстро набирать высокую крейсерскую скорость, а затем менее чем за 30 секунд замедляться до вертикальной посадки.
```

After:
```text
UH-90 Ibis создан в рамках программы PALA скоростного вертикального подъёма 2050-х как средний многоцелевой вертолёт комбинированной схемы. Многочисленные узлы подвески добавили ударные возможности. Жёсткие соосные винты и два реверсивных толкающих турбоэлектрических вентилятора в каналах дают быстрый разгон до высокой крейсерской скорости и торможение до вертикальной посадки менее чем за 30 секунд.
```

Reason: Shortens design-history and participial clauses; preserves program/date, original utility role, later armament, rotor/fan configuration and the under-30-second transition.

### 7. Alkyon AB-4

Source key:
```text
The Alkyon AB-4 is an advanced supersonic bomber with electronic warfare capabilities, designed to stealthily deliver nuclear or conventional payloads onto high value targets. 4 afterburning engines combined with variable geometry wings provide incredible top speed and enough maneuverability to evade aerial threats. If critically damaged, a crew escape capsule allows for safe ejection at any altitude or airspeed.
```

Before:
```text
Alkyon AB-4 — это усовершенствованный сверхзвуковой бомбардировщик с возможностями радиоэлектронной борьбы, предназначенный для скрытной доставки ядерных или обычных полезных грузов на важные цели. Четыре форсажных двигателя в сочетании с крыльями изменяемой геометрии обеспечивают невероятную максимальную скорость и достаточную маневренность для уклонения от воздушных угроз. В случае критического повреждения спасательная капсула экипажа позволяет безопасно катапультироваться на любой высоте и скорости полета.
```

After:
```text
Alkyon AB-4 — передовой сверхзвуковой бомбардировщик со средствами РЭБ для скрытных ударов по важным целям обычным или ядерным оружием. Четыре форсажных двигателя и крыло изменяемой геометрии дают очень высокую скорость и манёвренность для уклонения от воздушных угроз. Спасательная капсула обеспечивает безопасное катапультирование при критических повреждениях на любой высоте и скорости.
```

Reason: Replaces verbose capability/payload clauses with direct military terminology; preserves EW, conventional/nuclear role, four engines, variable geometry, evasion and the escape capsule's full envelope.

### 8. Spearhead

Source key:
```text
With a liberal application of armour and weapon modules, the latest iterations of the Spearhead are as protected as they are powerful. The combination of 130mm main gun and ATGM launcher allow it to hold its own against larger numbers of enemy armoured units, while the roof mounted 20kw pulse laser can protect the relatively thinner top armour against missiles. Its ever-growing list of capabilities has come with a diminished top speed and a total weight far exceeding its original design specifications.
```

Before:
```text
Благодаря обширному применению модулей брони и вооружения, последние модификации Spearhead столь же защищены, сколь и мощны. Комбинация 130-мм орудия и пусковой установки ПТУР позволяет противостоять превосходящим силам бронетехники противника, а установленный на крыше 20-кВт импульсный лазер защищает относительно тонкую верхнюю броню от ракет. Постоянно растущий список возможностей привёл к снижению максимальной скорости и общей массе, значительно превышающей первоначальные проектные характеристики.
```

After:
```text
Новые модификации Spearhead усилены модулями брони и вооружения. 130-мм орудие и пусковая установка ПТУР позволяют противостоять численно превосходящей бронетехнике. Импульсный лазер мощностью 20 кВт на крыше защищает более тонкую верхнюю броню от ракет. Рост возможностей снизил максимальную скорость; масса намного превысила проектную.
```

Reason: Splits an overloaded sentence and removes rhetorical repetition; retains module upgrades, numerical disadvantage, gun/ATGM/laser specifications, top-armor protection and speed/weight penalties.

### 9. Argus class frigate

Source key:
```text
Bristling with air defense weapons, the Argus class is a missile frigate designed to protect valuable assets from air attack. Capable of locking down airspace in a wide radius, it is an essential component of BDF naval doctrine. The Argus class is fitted with the NL-98 active radar homing missile, capable of engaging datalinked targets at beyond visual ranges.
```

Before:
```text
Вооруженный средствами противовоздушной обороны, класс «Argus» представляет собой ракетный фрегат, предназначенный для защиты ценных объектов от воздушного нападения. Способный блокировать воздушное пространство в широком радиусе, он является важным компонентом военно-морской доктрины BDF. Класс «Argus» оснащен ракетой активного радиолокационного самонаведения NL-98, способной поражать цели, связанные с передачей данных, за пределами видимости.
```

After:
```text
Ракетный фрегат класса Argus с мощной ПВО защищает ценные объекты от воздушных атак и контролирует обширное воздушное пространство. Важная часть военно-морской доктрины BDF. Ракеты NL-98 с активным радиолокационным самонаведением поражают цели за пределами видимости по целеуказанию из сети обмена данными.
```

Reason: Removes repeated class/capability phrasing; retains area air defense, naval-doctrine role, NL-98 active radar homing and beyond-visual-range datalink targeting.

### 10. FS-12 Revoker

Source key:
```text
The FS-12 Revoker is built for agility above all else, capable of extreme maneuvers at almost any speed. Internal weapon bays help reduce drag, allowing supersonic speeds even at low altitudes and with heavy payloads. While less stealthy than newer fighters, the Revoker remains a cost-effective means of establishing air superiority.
```

Before:
```text
FS-12 Revoker создан прежде всего для маневренности и способен совершать экстремальные маневры практически на любой скорости. Внутренние отсеки вооружения помогают уменьшить лобовое сопротивление, позволяя развивать сверхзвуковую скорость даже на малых высотах и ​​с тяжелой полезной нагрузкой. Несмотря на то, что Revoker менее скрытен, чем новые истребители, он остается экономически эффективным средством установления превосходства в воздухе.
```

After:
```text
FS-12 Revoker создан для манёвренности: выполняет экстремальные манёвры почти на любой скорости. Внутренние оружейные отсеки снижают сопротивление, позволяя летать на сверхзвуке даже у земли с тяжёлой нагрузкой. Уступая новым истребителям в малозаметности, остаётся экономичным средством завоевания превосходства в воздухе.
```

Reason: Removes repeated modal/concessive clauses and the stray invisible characters within this description; preserves extreme maneuverability, internal bays, low-level/heavy-load supersonic flight and cost/stealth trade-off.

## Additional static review

Other long equipment descriptions were reviewed, not blindly edited. VT-7 Vagrant (427 characters) is a likely risk, but its unusual three-post ducted-thrust terminology needs a separate terminology decision. Cursor (390) likewise contains uncertain specialized hull/deck terminology; this pass does not guess at it. Type 12 (380) and Tarantula (376) remain possible follow-up fit-test candidates. No mission/hint text found during the broad length scan was changed.

## Length reductions

Counts are Unicode characters in the Russian values, not rendered lines or pixels.

| Description | Before | After | Reduction |
| --- | ---: | ---: | ---: |
| A-19 Brawler — current | 463 | 344 | 25.7% |
| A-19 Brawler — older stored | 285 | 234 | 17.9% |
| FS-20 Vortex | 301 | 210 | 30.2% |
| SFB-81 Darkreach | 384 | 277 | 27.9% |
| HLT Mobile Artillery | 260 | 215 | 17.3% |
| UH-90 Ibis | 538 | 402 | 25.3% |
| Alkyon AB-4 | 514 | 389 | 24.3% |
| Spearhead | 505 | 337 | 33.3% |
| Argus class frigate | 448 | 306 | 31.7% |
| FS-12 Revoker | 445 | 323 | 27.4% |
| Total selected text | 4143 | 3037 | 26.7% |

## Validation

Completed in the named main repository, not the session worktree. The pre-pass checkpoint is `.verification/encyclopedia-overflow-20261003/`. Exact source/before/after blocks above were checked against that checkpoint before application. A mechanical exact-token substitution preserved the minified JSON and all other bytes. Post-pass comparison confirms exactly the ten listed value changes, identical key order, no added/removed/renamed keys and no other value changes.

- JSON valid; exactly **3716** entries and zero duplicate exact keys.
- Normal audit exit **0**; strict audit exit **0**. Reports are under the checkpoint directory (`audit-before`, `audit-after`, `audit-strict`, Markdown and JSON).
- Protected identities, model/designation violations, proper-name violations, placeholder mismatches and TMP tag mismatches: **0 before and after**.
- All audit metrics/severity counts unchanged: CRITICAL **0**, HIGH **116**, MEDIUM **49**, INFO **13**. Existing trim, case, typography and newline findings were not addressed.
- `IR Flares`, `Radar Countermeasures`, `Continue`, `M12 Jackknife`: all exact identity mappings unchanged.
- Offline QA regression suite: **11/11 tests passed**.
- `scripts/package.ps1 -Version 3.6.3 -SkipBuild`: exit **0**. No compilation or runtime rebuild was invoked; the existing DLLs were packaged. Archive contains exactly the four approved payload files, independently byte-compared to their current inputs. Comparing old/new ZIP payloads confirms that only embedded `ru.json` changed; both DLLs and the font are identical.
- Source/runtime/AutoFit, panels, installers, cockpit/HUD/MFD policy and Mission Editor untouched in this pass. No game installation changes, network access, publishing or commit.

SHA256 values:

| File | Before | After |
| --- | --- | --- |
| `localization/ru.json` | `878E1B61CC21A11BE6D4D18DDE0DCD7394A3D9622E82A7ED6AD375B750DBD1A7` | `70A2F55DB890BA5F3D195BCA6CD511526AB13E9A06D3DFBA23722897B2E8F018` |
| `src/LocalizationPatch/Plugin.cs` | `646D262BEE2EEAAD2CB4A3CB1AEF7660B526379EFE7A9F3CC92EC0F0D20BE789` | Same |
| `src/LocalizationPatchDropdown/Plugin.cs` | `5C673F1D5C21FB0E24D8D66EFC494CB6D9D3D85A1085818976937F2734EB1214` | Same |
| `LocalizationPatch.dll` (Release/net472) | `A23F92C8CA807962793DD0534FDE2A08452BBE975EBE036819BA2174551258CC` | Same |
| `LocalizationPatchDropdown.dll` (Release/net472) | `C63326A4FE4C05C4A46F6593224D4D43C3F24A47700C253E41F8D38AFE51C4A6` | Same |
| Release ZIP v3.6.3 | `C6D2C24FDC085129415FEC300E3FF8E003171D4FDA512D74AC7D499B76DE17E2` | `92A75750D6F19B55F8FAA6F740324DD4F903A08F775D5D9093724D9EE6E74701` |

The ZIP remains `release/NuclearOption-RussianLocalization-v3.6.3.zip`. The previous archive is recoverable at `.verification/previous-packages/3df262563dbd4a35987c9d25f77f4565-NuclearOption-RussianLocalization-v3.6.3.zip`; nothing was deleted.

## Git handoff

This pass modifies only `localization/ru.json`, creates this report, and rebuilds the ignored release ZIP. Ignored verification checkpoints/tests are repository-local. **The repository was already dirty**: changes to Plugin.cs, installer/build scripts, README, CHANGELOG and the other audit tooling below predate this pass and were preserved. Source/DLL hash comparisons are against this pass's start, not Git HEAD. Historical stabilization reports/manifests were not rewritten to absorb these ten new changes.

`git diff --stat` (all accumulated tracked changes; this untracked report is not included):

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

`git status --short`:

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
?? config/
?? reports/encyclopedia-overflow.md
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
