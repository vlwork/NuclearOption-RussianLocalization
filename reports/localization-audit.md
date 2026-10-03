# Localization quality audit

Deterministic offline report. Localization/package inputs are read-only. Review candidates are not automatically defects.

## Summary

| Metric | Count |
|---|---:|
| EntryCount | 3729 |
| DuplicateExactKeys | 0 |
| ProtectedIdentityViolations | 0 |
| TrimUnsafeKeys | 112 |
| TrimCollisions | 4 |
| DesignationViolations | 0 |
| ProperNameViolations | 0 |
| PlaceholderMismatches | 0 |
| TmpTagMismatches | 0 |
| NewlineMismatches | 2 |
| CaseVariantGroups | 189 |
| InconsistentCaseVariantGroups | 34 |
| TypographyWarnings | 3 |
| DynamicNoiseEntries | 12 |
| CRITICAL | 0 |
| HIGH | 116 |
| MEDIUM | 49 |
| INFO | 13 |

Strict mode fails on objective invariants (JSON/schema/count/duplicates, identities, codes, proper names, placeholders and TMP). Style, trim and context warnings do not fail strict mode.

## Coverage

Unavailable: no extracted source snapshot. No coverage percentage can be established.

## CRITICAL

| Category | Source key (JSON-escaped) | Current Russian value | Reason | Suggested action |
|---|---|---|---|---|

## HIGH

| Category | Source key (JSON-escaped) | Current Russian value | Reason | Suggested action |
|---|---|---|---|---|
| Trim collision | " \n Path Node  &#124;&#124; Path Node " | "Узел пути &#124;&#124; Узел пути" | All normalize to 'Path Node'. | Retain until context and values justify a decision. |
| Trim collision | " Turret under pilot control &#124;&#124; Turret under pilot control" | "Турель под управлением пилота &#124;&#124; Турель под управлением пилота" | All normalize to 'Turret under pilot control'. | Retain until context and values justify a decision. |
| Trim collision | "Already loaded &#124;&#124; Already loaded " | "Уже загружено &#124;&#124; Уже загружено" | All normalize to 'Already loaded'. | Retain until context and values justify a decision. |
| Trim collision | "Saved Mission: &#124;&#124; Saved Mission: " | "Миссия сохранена: &#124;&#124; Сохраненная миссия:" | All normalize to 'Saved Mission:'. | Retain until context and values justify a decision. |
| Trim safety | " \n Path Node " | "Узел пути" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | " Turret under pilot control" | "Турель под управлением пилота" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Adding airbase " | "Добавление авиабазы" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Adding command " | "Добавление команды" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Advertising dedicated server with name " | "Рекламный выделенный сервер с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "AfterLoad for mission " | "AfterLoad для миссии" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Airbase with name " | "Авиабаза с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Already loaded " | "Уже загружено" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Attached airbase " | "Прикрепленная авиабаза" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Can not write over end of buffer, new length " | "Невозможно записать конец буфера, новая длина" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Capture could not find ICapturable on " | "Capture не удалось найти ICapturable на" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Chaff rearmed by " | "Чафф перевооружен" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Checking rearm affordability: current value: " | "Проверка доступности перевооружения: текущее значение:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Cleared for landing on " | "Разрешение на посадку на" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Cleared to taxi to " | "Разрешено рулить до" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Client Spawn Request failed: " | "Запрос на создание клиента не выполнен:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Connecting via steam to " | "Подключение через Steam к" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find " | "Не удалось найти" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find GameWorldPrefab " | "Не удалось найти GameWorldPrefab." | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find airbase with name " | "Не удалось найти авиабазу с таким названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find available " | "Не удалось найти в наличии" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find faction with name " | "Не удалось найти фракцию с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find map with name " | "Не удалось найти карту с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find mission with name " | "Не удалось найти миссию с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find road network with name " | "Не удалось найти дорожную сеть с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Could not find unit with name " | "Не удалось найти объект с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Couldn't find engine interface for part " | "Не удалось найти интерфейс двигателя для детали" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Default to load default mission: " | "По умолчанию для загрузки миссии по умолчанию:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Deregistering aeroPart " | "Отмена регистрации aeroPart" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Destination Path Exists, deleting it first: " | "Путь назначения существует, сначала удалив его:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Detonating missile " | "Детонирующая ракета" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Error parsing line: " | "Ошибка разбора строки:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Error reading build hash: " | "Ошибка чтения хеша сборки:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Error reading log file: " | "Ошибка чтения файла журнала:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Error starting TCP listener: " | "Ошибка запуска прослушивателя TCP:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to add command " | "Не удалось добавить команду" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to download image: " | "Не удалось загрузить изображение:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to find Hq in scene with name " | "Не удалось найти штаб-квартиру в сцене с именем." | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to find airbase with name " | "Не удалось найти авиабазу с таким названием." | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to find faction with name: " | "Не удалось найти фракцию с названием:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to find tower with named " | "Не удалось найти башню с именем" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to load DedicatedServerConfig at " | "Не удалось загрузить DedicatedServerConfig на" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to load mission with name " | "Не удалось загрузить миссию с названием." | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to load system scene " | "Не удалось загрузить системную сцену." | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to move " | "Не удалось переместить" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to move mission file to folder because " | "Не удалось переместить файл миссии в папку, поскольку" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to parse " | "Не удалось проанализировать" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to reload mission " | "Не удалось перезагрузить миссию" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to save copy:\n" | "Не удалось сохранить копию:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to set " | "Не удалось установить" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Failed to write to log file: " | "Не удалось записать файл журнала:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "File does not exist: " | "Файл не существует:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "First load for " | "Первая загрузка для" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Flares rearmed by " | "Сигнальные ракеты перезапущены" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Found GameWorldPrefab " | "Найден GameWorldPrefab" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Found Scene full path " | "Полный путь найденной сцены" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Found Scene name " | "Найдено название сцены" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Found config path argument: " | "Найден аргумент пути конфигурации:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Impossible to set waypoint for " | "Невозможно установить путевую точку для" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Invalid KeyValue key " | "Неверный ключ KeyValue" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Invalid server key " | "Неверный ключ сервера" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Invalid tag key " | "Неверный ключ тега" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Last save: " | "Последнее сохранение:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Load success " | "Загрузка прошла успешно" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Loaded config " | "Загруженная конфигурация" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Loading Steam Ids from " | "Загрузка идентификаторов Steam из" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Loading next Mission " | "Загрузка следующей миссии" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Looking at " | "Глядя на" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Mission already equal to " | "Миссия уже равна" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Mission load had errors: " | "При загрузке миссии были ошибки:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Mission must have objective with name " | "Миссия должна иметь цель с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Move failed: Source " | "Переместить не удалось: Источник" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Move paths the same skipping: " | "Пути перемещения такие же, пропуская:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Moving folder from " | "Перемещение папки из" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "NO WRECK HAS BEEN FOUND BY " | "НЕ НАЙДЕНО НИКАКИХ ОБРЕШЕНИЙ" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "No file at path: " | "Нет файла по пути:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "No file at temp path: " | "Нет файла по временному пути:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "No group with name " | "Нет группы с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "No skips found for faction " | "Пропусков для фракции не найдено" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "No type with name " | "Нет типа с именем" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "OnSceneLoaded for mission " | "OnSceneЗагружено для миссии" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Opening local content " | "Открытие локального контента" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Opening steam " | "Открытие пара" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Path Node " | "Узел пути" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Pilot : " | "Пилот:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Private Build - " | "Частная постройка -" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Queuing audioClip " | "Очередь аудиоклипа" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Reading footer " | "Чтение нижнего колонтитула" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Received Command " | "Получена команда" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Refueled by " | "Заправлено" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Remove from " | "Удалить из" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Removing airbase " | "Удаление авиабазы" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Road Distance: " | "Расстояние по дороге:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Saved Mission: " | "Сохраненная миссия:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Sending footer " | "Отправка нижнего колонтитула" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Sending header " | "Отправка заголовка" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Setting load path to " | "Установка пути загрузки" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Setting parachute attached part to " | "Установка прикрепленной части парашюта в" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Setting url address to " | "Установка URL-адреса для" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Spawn custom airbase " | "Создать собственную авиабазу" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Start Load " | "Начать загрузку" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Successfully loaded : " | "Успешно загружено:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Successfully saved : " | "Успешно сохранено:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Taxi to " | "Такси до" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Teamkilled by " | "Убит командой" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Test 5 Failed: " | "Тест 5 не пройден:" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Turrets set to " | "Режим турелей: " | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Unable to validate hit claimed by " | "Не удалось подтвердить попадание, заявленное пользователем" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Unit with name " | "Юнит с названием" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Unknown command " | "Неизвестная команда" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Waiting on pending task for " | "Ожидание отложенной задачи для" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |
| Trim safety | "Waypoint is using objective with name " | "Путевая точка использует цель с именем" | Boundary whitespace prevents ordinary exact runtime lookup. | Review source/context; never bulk-trim. |

## MEDIUM

| Category | Source key (JSON-escaped) | Current Russian value | Reason | Suggested action |
|---|---|---|---|---|
| Case variants | "ACTIVE &#124;&#124; Active" | "АКТИВНО &#124;&#124; Активное" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "AOA &#124;&#124; AoA" | "АОА &#124;&#124; Угол атаки" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "BOSCALI &#124;&#124; Boscali" | "БОСКАЛИ &#124;&#124; Boscali" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "CAMERA TRANSFORM &#124;&#124; Camera Transform" | "ТРАНСФОРМАЦИЯ КАМЕРЫ &#124;&#124; Преобразование камеры" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "CREATE NEW &#124;&#124; Create New" | "СОЗДАТЬ &#124;&#124; Создать новый" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "DEVELOPMENT ROADMAP &#124;&#124; Development Roadmap" | "ПЛАН РАЗРАБОТКИ &#124;&#124; Дорожная карта разработки" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "ENEMY &#124;&#124; Enemy" | "ВРАЖЕСКИЕ &#124;&#124; Враг" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "FAR &#124;&#124; Far" | "ДАЛЬН. &#124;&#124; Далеко" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "FRIENDLY &#124;&#124; Friendly" | "СОЮЗНЫЕ &#124;&#124; Союзный" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "Faction Funds &#124;&#124; Faction funds" | "Фонды фракций &#124;&#124; Средства фракции" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "Faction Score &#124;&#124; Faction score" | "Оценка фракции &#124;&#124; Очки фракции" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "GUN &#124;&#124; Gun" | "ПИСТОЛЕТ &#124;&#124; Пушка" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "HIGH &#124;&#124; High" | "ВЫСОКИЙ &#124;&#124; Высокое" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "Inner Wing Pylons &#124;&#124; Inner wing pylons" | "Внутренние подкрыльевые пилоны &#124;&#124; Внутренние пилоны крыла" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "LOW &#124;&#124; Low" | "НИЗКИЙ &#124;&#124; Низкое" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "MEDIUM &#124;&#124; Medium" | "СРЕДНИЕ &#124;&#124; Среднее" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "MISSILE WARNING &#124;&#124; Missile Warning" | "РАКЕТНАЯ ОПАСНОСТЬ &#124;&#124; Предупреждение о ракете" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "NAME &#124;&#124; Name" | "ИМЯ &#124;&#124; Название" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "NEW &#124;&#124; New" | "НОВЫЙ &#124;&#124; Новая" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "NO TARGET &#124;&#124; No Target" | "НЕТ ЦЕЛИ &#124;&#124; " | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "Need Preview &#124;&#124; Need preview" | "Нужен предварительный просмотр &#124;&#124; Нужен предпросмотр" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "OBJECTIVE &#124;&#124; Objective" | "ЦЕЛЬ &#124;&#124; Задача" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "OPTICAL &#124;&#124; Optical" | "ОПТИЧЕСКИЙ &#124;&#124; Оптическое" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "Outer Wing Pylons &#124;&#124; Outer wing pylons" | "Внешние подкрыльевые пилоны &#124;&#124; Пилоны внешнего крыла" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "PRIMEVA ARMED LIBERATION ALLIANCE &#124;&#124; Primeva Armed Liberation Alliance" | "ВООРУЖЁННЫЙ ОСВОБОДИТЕЛЬНЫЙ АЛЬЯНС PRIMEVA &#124;&#124; Альянс вооруженного освобождения Primeva" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "PRIMEVA &#124;&#124; Primeva" | "ПРИМЕВА &#124;&#124; Primeva" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "PUBLIC &#124;&#124; Public" | "ПУБЛИЧНЫЙ &#124;&#124; Открытое" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "PVE &#124;&#124; PvE" | "ПВЕ &#124;&#124; PvE" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "READY &#124;&#124; Ready" | "ГОТОВО &#124;&#124; Готов" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "REQUISITION &#124;&#124; Requisition" | "РЕКВИЗИЦИЯ &#124;&#124; Запросить" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "SOUTH BOSCALI GENERAL AVIATION &#124;&#124; South Boscali General Aviation" | "ГРАЖДАНСКАЯ АВИАЦИЯ ЮЖНОЙ BOSCALI &#124;&#124; Южный Boscali авиации общего назначения" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "TOTAL &#124;&#124; Total" | "ОБЩИЙ &#124;&#124; Общий вес" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "VALUE &#124;&#124; Value &#124;&#124; value" | "СТОИМОСТЬ &#124;&#124; Стоимость &#124;&#124; значение" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Case variants | "WEAPONS &#124;&#124; Weapons" | "ОРУЖИЕ &#124;&#124; Вооружение" | Translations differ beyond capitalization/whitespace. | Verify context; case-only groups are not automatically errors. |
| Newline safety | " \n Path Node " | "Узел пути" | Line break counts differ; formatting may be intentional. | Check layout/concatenation before editing. |
| Newline safety | "Failed to save copy:\n" | "Не удалось сохранить копию:" | Line break counts differ; formatting may be intentional. | Check layout/concatenation before editing. |
| Russian typography | "Column 50m" | "Коллона 50м" | Number touches a Cyrillic unit. | Review ordinary prose only; protect telemetry and identifiers. |
| Russian typography | "Concrete Wall 10m" | "Бетонная стена 10м" | Number touches a Cyrillic unit. | Review ordinary prose only; protect telemetry and identifiers. |
| Russian typography | "Prevent a column of vehicles from crossing the bridge to Boscali Island, before neutralizing the attack at its source." | " Предотвратите коллону транспорта от пересечения моста Острова Boscali, перед тем как нейтрализововать аттаку в ее источнике" | Added boundary whitespace. | Review ordinary prose only; protect telemetry and identifiers. |
| Translation quality | "1 FORWARD BAY" | "1 ПЕРЕДНИЙ ОТСЕК" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "23mm AAA Emplacement" | "23-мм зенитная установка" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "3 HEATER BAYS" | "3 ОТСЕКА ДЛЯ ИК-РАКЕТ" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "Dynamo Class Destroyer" | "Эсминец класса Dynamo" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "FGA-57 Anvil" | "FGA-57 Anvil" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "Forward Bay" | "Передний отсек" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "Heater Bays" | "Отсеки для ИК-ракет" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "M12 Jackknife" | "M12 Jackknife" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "MSV R9 Stratolance Launcher" | "Пусковая установка MSV R9 Stratolance" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |
| Translation quality | "Rear Bay" | "Задний отсек" | Curated terminology/identity review candidate, not an automatic error. | Record a reviewed decision; retain ambiguity. |

## INFO

| Category | Source key (JSON-escaped) | Current Russian value | Reason | Suggested action |
|---|---|---|---|---|
| Coverage | "extracted_gamedata.txt" | "(unavailable)" | No local extracted snapshot: coverage is unknown, not 100%. | Supply an existing snapshot for an offline comparison. |
| Dynamic noise | "1280x720" | "1280x720" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1280x768" | "1280x768" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1280x800" | "1280x800" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1360x768" | "1360x768" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1366x768" | "1366x768" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1440x900" | "1440x900" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1600x1024" | "1600x1024" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1600x900" | "1600x900" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1680x1050" | "1680x1050" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "1920x1080" | "1920x1080" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "CAPACITOR 90%" | "КОНДЕНСАТОР 90%" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
| Dynamic noise | "SPD : 648km/h" | "СКОР.: 648 км/ч" | Generated telemetry/resolution-like literal. | Report only; no untested runtime pattern changes. |
