# Аудит совместимости Nuclear Option 0.34.6

Дата: 2026-10-31, Europe/Moscow. Кандидат: **LocalizationPatch 3.6.5**.
Вердикт: **READY FOR GAME TEST**. Это результат статической проверки и автономных тестов;
запуск Unity, host/client и визуальная проверка не выполнялись.

## A. Установленная игра и Git

- Фактический каталог: `C:/Program Files (x86)/Steam/steamapps/common/Nuclear Option`.
  Указанный в задании каталог на `G:` не доступен из текущей сессии. Доступная установка
  на `C:` найдена через конфигурацию Steam; факт её переноса с `G:` не установлен.
- `steamapps/appmanifest_2168680.acf`: appid `2168680`, StateFlags `4`, build **26327221**.
- `NuclearOption_Data/globalgamemanagers`: строка версии **0.34.6**, смещение 1844,
  корректный четырёхбайтовый префикс длины 6. Отдельной установки 0.34.5 для сравнения нет.
- Начальное дерево чистое. Начальная ветка `main`, HEAD **90e6a968dcc689548c80acc828b7387935acc260**.
  После checkpoint `8046c91` были добавлены mixed-license/provenance-документы, README и установщик.
- Работа выполнена в **fix/game-0346-compatibility**; HEAD не изменён.
  Новых AGENTS.md в репозитории и его родительских каталогах не обнаружено.

Повторная диагностика среды после уточнения пользователя: Windows/Win32NT,
версия ОС `10.0.26200.0`, PowerShell `5.1.26100.9711`, видимые файловые диски
`C:`, `D:`, `E:`, `G:`, `W:`. Корни `G:` и `W:` доступны. Репозиторий — рабочий
Git checkout по указанному пути на `W:`, с собственным `.git`, без reparse-point
на корне checkout или `.git`; git-dir/common-dir — `.git`, без переопределений
GIT_DIR/GIT_WORK_TREE. Это подтверждает доступ к Windows checkout, но не доказывает,
что среда исполнения не изолирована или что checkout никогда не копировался.
Доступ к файлам сессии ограничен sandbox-политикой.

Проверены только известные Steam roots и пути из `libraryfolders.vdf`: конфигурация
перечисляет библиотеки на `C:`, `D:`, `G:`, `W:`. Манифест Nuclear Option найден
в библиотеке на `C:`; DLL там доступны для чтения, их хеш повторно совпал.
Неограниченного поиска по файловой системе не было. Поэтому проверка метаданных
доступной установки не имеет статуса BLOCKED BY ENVIRONMENT; игровой запуск
по-прежнему не выполнен. Историческое расположение установки на `G:` этим не опровергается.

## B. Находки, серьёзность и доказательства

| Категория | Серьёзность | Результат и доказательство |
| --- | --- | --- |
| Подтверждённый дефект защиты текста | Высокая | Общие TMP-перехваты/сканы не различали текст ввода и UI-метки. Автономная фикстура с исходным методом из `90e6a96` воспроизводит замену введённого `Multiplayer` на русский текст. Новый ChatBox синхронизирует mentions с TMP_InputField; ChatSuggestionItemUI содержит имена, аргументы и историю. Добавлено исключение этих компонентов из общего перевода и AutoFit. Такой дефект существовал в общей логике раньше; именно дату его появления по двум установленным версиям доказать нельзя. |
| Подтверждённый пробел перехвата | Средняя | В установленной Unity.TextMeshPro нет `SetText(string)`, есть `SetText(string, bool)`. Новый `ChatAutocompleteUI.SetHeader` использует вторую перегрузку. Добавлен точный fallback только для русского языка, с проверкой void; отсутствие метода безопасно пропускается. Задержка/мерцание на экране требует игрового теста. |
| Непереведённые UI-строки | Средняя | `Recent`, `Commands`, `Mention player`, `Suggestions`, `Mod Required` отсутствовали в базовом словаре. Все пять найдены как IL-литералы конкретных UI-производителей; добавлены точные переводы. Источники и хеш сборки записаны в `config/game-0346-ui.json`. |
| Совместимость Harmony | Проблем не найдено статически | TMP/legacy text setters, оба concrete TMP OnEnable и все четыре AddOptions(List<string>/List<OptionData>) существуют. FontEngine.LoadFontFace(Font,int) существует. Сигнатура миссионного производителя и его два вызывающих пути повторно проверены по IL. |
| Существующий BepInEx-лог | Недостаточно свежих данных | Последняя запись файла: `2026-10-03T21:14:43Z`. По одному загруженному основному плагину и addon, шесть успешных основных патчей, 0 warnings/errors/patch exceptions и scan errors. Этот лог не доказывает совместимость с нынешним build; таймингов производительности в нём нет. Личные строки лога в отчёт/репозиторий не копировались. |
| Словарь и защищённые имена | Проблем не найдено | Сохранены все 3729 базовых ключей и значений; добавлены только пять записей, итог **3734**. Continue, IR Flares, Radar Countermeasures, M12 Jackknife, обозначения и собственные имена проходят QA. |
| Теги карт/миссий | Частично проверено | Встроенные Single Player/Multiplayer, PvE/PvP, Dawn/Day/Dusk/Night уже покрыты. Mod Required добавлен. SetValue пишет отображаемый текст; данные MissionTag не меняются. Реальные карты, размеры тегов и фильтрация требуют UI-теста. |
| Multiplayer/длинные названия | Требуется игровой тест | Проверены LobbyListItem, LobbyDetailsModal и DedicatedServerKeyValues. Сетевые ключи/ограничения длины и публикация названий не патчатся. Метки Player Hosted/Dedicated Server уже есть. Длинное название, tooltip, модальные окна и обрезание визуально не проверены. |
| Счётчик ракет | Проблем локализации не подтверждено | Код расчёта/синхронизации количества и числовые SetText(float...) не изменены. Исправление игры 0.34.6 не считается автоматически проверенным; нужен отдельный client-тест. |
| Encyclopedia/меню/производительность | Требуется игровой тест | Старые OnEnable, периодичность сканов, dropdown и text-only AutoFit сохранены. Новых FindObjects-сканов нет. Унаследованный быстрый Resources.FindObjectsOfTypeAll с интервалом 0.02 с остаётся; стоимость существующих сканов и новых guard-проверок на реальной сцене не измерялась. |
| Отложено/вне области | Низкая/средняя | Динамические счётчики autocomplete (`{0} found/players/options`), составные заголовки аргументов и /help не переводятся широким матчингом. Описания встроенных команд в строках подсказок оставлены английскими. Mission Editor, общие hints, join/leave и HQ-сообщения отложены. |

Текущие resources.assets дают **34** валидированных именованных JSON-миссии:
146 записей категории hints, 177 идентификаторов и 157 статических кандидатов, включая описания.
Все **13** разрешённых сообщений Reprisal повторно найдены с прежними полями и значениями.
У **8** описаний миссий нет точного ключа в словаре; их новизна и путь отображения не доказаны,
поэтому они отдельно отложены. Диагностика, profiler markers, RPC-имена, ключи серверных
параметров, команды, player/argument tokens и игровые идентификаторы не добавлялись в ru.json.

Точная проверенная сигнатура: private instance void
`MissionMessages.ShowMessgeLocal(System.String, System.Boolean, FactionHQ)`.
Сохранены IsLocalFaction, GameMessage и PlaySound, два вызывающих пути, оригинальная
сериализация RPC, исходные mission fields и allowlist. HQMessageInternal и готовая лента
не получили новых патчей/regex. Guard только исключает две display-компоненты ленты из
общего UI-перевода; перевод разрешённых сообщений остаётся на локальном производителе.

## C. Точные изменения файлов

| Файл | Изменение |
| --- | --- |
| `src/LocalizationPatch/Plugin.cs` | Версия 3.6.5; точный SetText fallback; русские guard-проверки editable TMP text, suggestion rows, MessageUI.messageText/killFeedText. Новые тип/поля разрешаются безопасно; EN/RU-комментарии. |
| `src/LocalizationPatch/LocalizationPatch.csproj` | Версия/assembly/file 3.6.5/3.6.5.0; описание кандидата. |
| `localization/ru.json` | Только пять добавлений из manifest; исходные 3729 пар неизменны. |
| `config/localization-audit.json` | Ожидаемый итог 3734. |
| `config/game-0346-ui.json` | Новый перечень пяти переводов, производителей и проверенной сборки. |
| `tools/inspect-game-compatibility.ps1` | Новый read-only Cecil-аудит: сигнатуры, ограниченные IL/строки, хеши, обезличенная сводка лога; вывод только в новый `.verification`-каталог. |
| `tools/inspect-mission-runtime.ps1` | Явный ExpectedAssemblySha256 для повторной проверки новой сборки. По умолчанию сохраняется старый pin; исторический manifest не переписан. |
| `tools/test-ui-compatibility.py`, `tools/ui-compatibility-fixtures.cs` | Новые автономные проверки реальных извлечённых методов/Harmony hooks, воспроизведение baseline-дефекта, защита содержимого, точный baseline и сверка меток с локальными метаданными. |
| `tools/test-mission-runtime.py` | Разрешён только явно перечисленный UI-delta; остальная логика по-прежнему сравнивается с прежним baseline. |
| `tools/test-mission-messages.py` | Учёт пяти UI-добавлений без изменения 13 миссионных переводов. |
| `CHANGELOG.md`, `README.md` | Версия кандидата, объём и ссылка на этот отчёт. |
| `THIRD_PARTY_NOTICES.md`, `localization/PROVENANCE.md` | Актуальное число записей и происхождение пяти новых русских значений. Смешанные лицензии и нерешённые upstream-права сохранены. |
| `reports/game-0346-compatibility.md` | Этот отчёт. |

Dropdown source и его версия 1.0.0 не изменены. README_RU, лицензии, шрифт,
исторические отчёты и config/mission-messages.json не изменены.

## D. Валидация и SHA256

- Offline dotnet restore/build обоих проектов, Release, warnings as errors: **PASS**, 0 warnings/errors.
- `test-localization-qa.py`: **11/11 PASS**; `test-mission-messages.py`: **11/11 PASS**.
- `test-mission-runtime.py`: **13/13 Harmony fixtures PASS**; локальный реальный IL-производитель проверен отдельно.
- `test-ui-compatibility.py --metadata ...`: **PASS** — реальный setter/SetText prefix, неизменный bool,
  input/placeholder (включая скрытые панели), suggestion/feed guards, scan/fit paths, исходные байты команд/mentions/messages,
  приватный текст не записывается как miss, non-Russian и missing/wrong-return targets.
- Localization strict audit: **PASS**, 0 strict failures, duplicate keys, placeholder/TMP-tag,
  designation/proper-name/protected-identity нарушений. Сохранены прежние 112 trim-unsafe ключей,
  4 trim collisions, 2 newline warnings, 34 inconsistent case groups; новых проблем этих категорий нет.
  Уровень HIGH для старых trim-ключей в отчёте QA не равен strict failure.
- Installer tests: **7/7 PASS**; release installer: **4/4 PASS**. Только макеты внутри `.verification`.
- Пакет **PASS**: 12 файлов — 4 runtime, 6 legal/provenance, 2 installer; содержимое и хеши проверены.
  Ни одной зависимости игры, Cecil/Harmony/Unity DLL, PDB или извлечённых assets в пакете нет.
- `git diff --check`: **PASS**. Staged-файлов и tracked игровых/скомпилированных DLL/EXE/assets: **0**.
- Повторная проверка всех **11** записанных хешей файлов игры, зависимостей и установленных плагинов:
  **не изменились**. Steam-файлы и плагины не устанавливались/не заменялись.

| Локальный вход | SHA256 |
| --- | --- |
| Assembly-CSharp.dll | `BABDD626BBAB5F01E6C244150C1E77C57C131EE86967214E2E5CED6D813C2BCE` |
| Unity.TextMeshPro.dll | `EAE7010F98C1C6B0ED573CCD73114E6ADEFF306AC6FBCF22517670D9789422F1` |
| UnityEngine.UI.dll | `73B13688FF1E87652A6111F5A11896542B54B4571617B52F52C8BEFB05BF8CA7` |
| UnityEngine.TextCoreFontEngineModule.dll | `A40958FA318BFE7D175BFED37B2DBF79528240C287165F198787457C2E136715` |
| resources.assets | `FCE2A1CECD65F185F4C72873C929421D95FEB7BAB845C7261DAC1CAE541575FC` |
| Установленный LocalizationPatch.dll 3.6.4.0 | `CBA51FB51BC5984DB8A46BAF10B4F142799F8FB33BCE44C48E6FE772F0F9ABEC` |
| Установленный LocalizationPatchDropdown.dll 1.0.0.0 | `7D94BE72CD7652534640B73B74211812E9DD05CA6E8249EDB2452C6416AD62A7` |

Все остальные входные хеши, 498 сигнатур/методов и 308 ограниченно отобранных IL-литералов
остаются локально в `.verification/game-0346-final-evidence/metadata.json` (не в Git).
Доказательства миссионного производителя: `.verification/game-0346-mission-review/`.
Strict QA: `.verification/game-0346-strict-audit.json` и `.md`.

| Сгенерированный локальный кандидат | SHA256 |
| --- | --- |
| `.verification/game-0346-build-candidate/src/LocalizationPatch/bin/Release/net472/LocalizationPatch.dll` | `672426E050B01A94E660F47E22C5ABAD26D9BB545698990F1697DBCEDF766706` |
| `.verification/game-0346-build-candidate/src/LocalizationPatchDropdown/bin/Release/net472/LocalizationPatchDropdown.dll` | `9BD8ABA44F5DAFBE685CB4E88CBBCFA500895EA468355EA739CF26E16120D429` |
| `.verification/game-0346-final-package/NuclearOption-RussianLocalization-v3.6.5.zip` | `A9B3982197F81D8DDE23DDC6877672B0EB6D9FE012345B90B1D1A11C7DCBE1CB` |

## E. Что остаётся неопределённым

Нет свежего игрового лога, визуального теста, multiplayer-доказательств и профиля времени кадра.
Совпадение версии установленного плагина с 3.6.4 само по себе не доказывает воспроизводимость
его бинарника из текущего исходника. Плагин в установленной игре сохранён без изменений.
Атрибуция обновлений именно 0.34.5 против 0.34.6 ограничена отсутствием старой установки:
подтверждены факты текущего build, а не полный дифф двух игровых версий.
Прочие английские строки и старые QA-предупреждения из раздела B остаются открытыми.

## F. Точечный ручной чеклист

1. После отдельно одобренной установки кандидата проверить свежий лог: одна загрузка каждого
   плагина, точный SetText(string,bool), отсутствие Harmony exceptions и scan errors.
2. Mission Select: Recent, все карты/теги/счётчики, смена фильтров и описаний; отсутствие мерцания.
3. Чат: `/help`, slash autocomplete, стрелки/Tab/Enter/Escape, история, клики, @mentions;
   использовать игрока/сообщение с именем UI-ключа (`Multiplayer`, `Commands`, `Buy ...`).
   Проверить видимый текст, caret, отправленные байты и ответы host/client.
4. Server List: обычные/выделенные/модифицированные серверы, пароль, детали и tooltips;
   название миссии длиннее обычного и с кириллицей, фильтрация и подключение.
5. На client проверить количество ракет до/после пуска и после синхронизации с host.
6. Reprisal на host и client: 13 разрешённых сообщений, K92/PALA, faction filtering и звук;
   неизвестное сообщение, join/leave и чат остаются исходными, составная лента не переводится повторно.
7. Encyclopedia: длинные статьи, переключение короткая/длинная, меню и dropdown;
   Continue, IR Flares, Radar Countermeasures, M12 Jackknife; родительские RectTransform неизменны.
8. Сравнить UI при другом языке, отключённой локализации и частоте кадров в насыщенной сцене.

## G. Git и объём

HEAD остаётся `90e6a96`, ветка `fix/game-0346-compatibility`.
11 изменённых tracked-файлов и 5 новых untracked-файлов (включая этот отчёт);
индекс пуст. Полный список — раздел C. Сгенерированные DLL/ZIP/evidence игнорируются.
Tracked diff stat: **11 files changed, 117 insertions(+), 33 deletions(-)**;
untracked-файлы Git в него не включает.

```text
 M CHANGELOG.md
 M README.md
 M THIRD_PARTY_NOTICES.md
 M config/localization-audit.json
 M localization/PROVENANCE.md
 M localization/ru.json
 M src/LocalizationPatch/LocalizationPatch.csproj
 M src/LocalizationPatch/Plugin.cs
 M tools/inspect-mission-runtime.ps1
 M tools/test-mission-messages.py
 M tools/test-mission-runtime.py
?? config/game-0346-ui.json
?? reports/game-0346-compatibility.md
?? tools/inspect-game-compatibility.ps1
?? tools/test-ui-compatibility.py
?? tools/ui-compatibility-fixtures.cs
```

## H. Вердикт

**READY FOR GAME TEST** — кандидат собран и проверен автономно; runtime compatibility PASS
не заявляется. Commit, push, release, tag, merge, live-install и публикация не выполнялись.
