# Localization finding review

Every baseline HIGH/MEDIUM finding from the coherent QA engine is classified below. No context-dependent/editor/hint/avionics values were changed. Curated quality candidates remain review reminders, not automatic errors.

| Severity | Category | Exact source (JSON) | Baseline Russian value | Classification | Decision / reason |
|---|---|---|---|---|---|
| CRITICAL | Model/designation preservation | "T9K41 Boltstrike" | "Т9К41 Болтстрайк" | OBJECTIVE_ERROR | Restore exact ASCII model code and proper name, including in deferred areas. |
| CRITICAL | Proper name | "T9K41 Boltstrike" | "Т9К41 Болтстрайк" | OBJECTIVE_ERROR | Restore exact ASCII model code and proper name, including in deferred areas. |
| HIGH | Trim collision | " \n Path Node  &#124;&#124; Path Node " | "Узел пути &#124;&#124; Узел пути" | INTENTIONAL | Retain all raw keys. Saved Mission has conflicting semantics; other collision values are identical and removal offers no demonstrated benefit. |
| HIGH | Trim collision | " Turret under pilot control &#124;&#124; Turret under pilot control" | "Турель под управлением пилота &#124;&#124; Турель под управлением пилота" | INTENTIONAL | Retain all raw keys. Saved Mission has conflicting semantics; other collision values are identical and removal offers no demonstrated benefit. |
| HIGH | Trim collision | "Already loaded &#124;&#124; Already loaded " | "Уже загружено &#124;&#124; Уже загружено" | INTENTIONAL | Retain all raw keys. Saved Mission has conflicting semantics; other collision values are identical and removal offers no demonstrated benefit. |
| HIGH | Trim collision | "Saved Mission: &#124;&#124; Saved Mission: " | "Миссия сохранена: &#124;&#124; Сохраненная миссия:" | CONTEXT_REQUIRED | Retain all raw keys. Saved Mission has conflicting semantics; other collision values are identical and removal offers no demonstrated benefit. |
| HIGH | Trim safety | " \n Path Node " | "Узел пути" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | " Objective needs a faction" | "Для цели нужна фракция" | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | " This text uses emojis, which have a different byte count." | "В этом тексте используются эмодзи, которые имеют разное количество байтов." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | " Turret under pilot control" | "Турель под управлением пилота" | INTENTIONAL | Retain duplicate: no functional benefit from deletion; pattern sub-probes can carry whitespace. |
| HIGH | Trim safety | "Adding airbase " | "Добавление авиабазы" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Adding command " | "Добавление команды" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Advertising dedicated server with name " | "Рекламный выделенный сервер с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "AfterLoad for mission " | "AfterLoad для миссии" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Airbase with name " | "Авиабаза с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Already loaded " | "Уже загружено" | INTENTIONAL | Retain duplicate: no functional benefit from deletion; pattern sub-probes can carry whitespace. |
| HIGH | Trim safety | "Attached airbase " | "Прикрепленная авиабаза" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "BUILDING REPAIRS COMPLETE " | "РЕМОНТ ЗДАНИЯ ЗАВЕРШЕН" | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Can not write over end of buffer, new length " | "Невозможно записать конец буфера, новая длина" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Can't multiselect " | "Не могу выбрать несколько вариантов" | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Capture could not find ICapturable on " | "Capture не удалось найти ICapturable на" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Chaff rearmed by " | "Чафф перевооружен" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Checking rearm affordability: current value: " | "Проверка доступности перевооружения: текущее значение:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Cleared for landing on " | "Разрешение на посадку на" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Cleared to taxi to " | "Разрешено рулить до" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Client Spawn Request failed: " | "Запрос на создание клиента не выполнен:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Connecting via steam to " | "Подключение через Steam к" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find " | "Не удалось найти" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find GameWorldPrefab " | "Не удалось найти GameWorldPrefab." | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find airbase with name " | "Не удалось найти авиабазу с таким названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find available " | "Не удалось найти в наличии" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find faction with name " | "Не удалось найти фракцию с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find map with name " | "Не удалось найти карту с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find mission with name " | "Не удалось найти миссию с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find road network with name " | "Не удалось найти дорожную сеть с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Could not find unit with name " | "Не удалось найти объект с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Couldn't find engine interface for part " | "Не удалось найти интерфейс двигателя для детали" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Custom Airbase " | "Пользовательская авиабаза" | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Default to load default mission: " | "По умолчанию для загрузки миссии по умолчанию:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Deregistering aeroPart " | "Отмена регистрации aeroPart" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Destination Path Exists, deleting it first: " | "Путь назначения существует, сначала удалив его:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Detonating missile " | "Детонирующая ракета" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Error parsing line: " | "Ошибка разбора строки:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Error reading build hash: " | "Ошибка чтения хеша сборки:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Error reading log file: " | "Ошибка чтения файла журнала:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Error starting TCP listener: " | "Ошибка запуска прослушивателя TCP:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to add command " | "Не удалось добавить команду" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to download image: " | "Не удалось загрузить изображение:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to find Hq in scene with name " | "Не удалось найти штаб-квартиру в сцене с именем." | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to find airbase with name " | "Не удалось найти авиабазу с таким названием." | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to find faction with name: " | "Не удалось найти фракцию с названием:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to find tower with named " | "Не удалось найти башню с именем" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to load DedicatedServerConfig at " | "Не удалось загрузить DedicatedServerConfig на" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to load mission with name " | "Не удалось загрузить миссию с названием." | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to load system scene " | "Не удалось загрузить системную сцену." | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to move " | "Не удалось переместить" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to move mission file to folder because " | "Не удалось переместить файл миссии в папку, поскольку" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to parse " | "Не удалось проанализировать" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to reload mission " | "Не удалось перезагрузить миссию" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to save copy:\n" | "Не удалось сохранить копию:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to set " | "Не удалось установить" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Failed to write to log file: " | "Не удалось записать файл журнала:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "File does not exist: " | "Файл не существует:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "First load for " | "Первая загрузка для" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Flares rearmed by " | "Сигнальные ракеты перезапущены" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Found GameWorldPrefab " | "Найден GameWorldPrefab" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Found Scene full path " | "Полный путь найденной сцены" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Found Scene name " | "Найдено название сцены" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Found config path argument: " | "Найден аргумент пути конфигурации:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Hello, world! " | "Привет, мир!" | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Impossible to set waypoint for " | "Невозможно установить путевую точку для" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Invalid KeyValue key " | "Неверный ключ KeyValue" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Invalid server key " | "Неверный ключ сервера" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Invalid tag key " | "Неверный ключ тега" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Last save: " | "Последнее сохранение:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Load success " | "Загрузка прошла успешно" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Loaded config " | "Загруженная конфигурация" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Loading Steam Ids from " | "Загрузка идентификаторов Steam из" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Loading next Mission " | "Загрузка следующей миссии" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Looking at " | "Глядя на" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Mission Failed, no spawn points available " | "Миссия провалена, нет доступных точек появления." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Mission already equal to " | "Миссия уже равна" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Mission load had errors: " | "При загрузке миссии были ошибки:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Mission must have objective with name " | "Миссия должна иметь цель с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Move failed: Source " | "Переместить не удалось: Источник" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Move paths the same skipping: " | "Пути перемещения такие же, пропуская:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Moving folder from " | "Перемещение папки из" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "NO WRECK HAS BEEN FOUND BY " | "НЕ НАЙДЕНО НИКАКИХ ОБРЕШЕНИЙ" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "No file at path: " | "Нет файла по пути:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "No file at temp path: " | "Нет файла по временному пути:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "No group with name " | "Нет группы с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "No reserve " | "Без резерва" | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "No skips found for faction " | "Пропусков для фракции не найдено" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "No type with name " | "Нет типа с именем" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "OnSceneLoaded for mission " | "OnSceneЗагружено для миссии" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Opening local content " | "Открытие локального контента" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Opening steam " | "Открытие пара" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Path Node " | "Узел пути" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Pilot : " | "Пилот:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Private Build - " | "Частная постройка -" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Queuing audioClip " | "Очередь аудиоклипа" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Reading footer " | "Чтение нижнего колонтитула" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Received Command " | "Получена команда" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Refueled by " | "Заправлено" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Remove from " | "Удалить из" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Removing airbase " | "Удаление авиабазы" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Road Distance: " | "Расстояние по дороге:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Saved Mission: " | "Сохраненная миссия:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Sending footer " | "Отправка нижнего колонтитула" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Sending header " | "Отправка заголовка" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Setting load path to " | "Установка пути загрузки" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Setting parachute attached part to " | "Установка прикрепленной части парашюта в" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Setting url address to " | "Установка URL-адреса для" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Spawn custom airbase " | "Создать собственную авиабазу" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Start Load " | "Начать загрузку" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Successfully loaded : " | "Успешно загружено:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Successfully saved : " | "Успешно сохранено:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Taxi to " | "Такси до" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Teamkilled by " | "Убит командой" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Test 1a Passed: Short string handled correctly. " | "Тест 1a пройден: короткая строка обработана правильно." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Test 1b Passed: Short string handled correctly. " | "Тест 1b пройден: короткая строка обработана правильно." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Test 2 Passed: Long string split into multiple chunks correctly. " | "Тест 2 пройден: длинная строка правильно разбита на несколько частей." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Test 3 Passed: Long string correctly truncated to max length. " | "Тест 3 пройден: длинная строка правильно обрезана до максимальной длины." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Test 4 Passed: String with special characters handled correctly. " | "Тест 4 пройден: строка со специальными символами обработана правильно." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Test 5 Failed: " | "Тест 5 не пройден:" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Test 5 Passed: Japanese text correctly split into chunks under the 255-byte limit. " | "Тест 5 пройден: текст на японском языке правильно разбит на фрагменты размером менее 255 байт." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Test 6 Passed: Empty string handled correctly. " | "Тест 6 пройден: пустая строка обработана правильно." | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Turrets set to " | "Режим турелей: " | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Unable to validate hit claimed by " | "Не удалось подтвердить попадание, заявленное пользователем" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Unit with name " | "Юнит с названием" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Unknown command " | "Неизвестная команда" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "WRECK REMOVAL " | "УДАЛЕНИЕ АВАРИЙ" | OBJECTIVE_ERROR | Only key renamed: approved boundary-space allowlist, no value change or collision. |
| HIGH | Trim safety | "Waiting on pending task for " | "Ожидание отложенной задачи для" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| HIGH | Trim safety | "Waypoint is using objective with name " | "Путевая точка использует цель с именем" | CONTEXT_REQUIRED | Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven. |
| MEDIUM | Case variants | "ACTIVE &#124;&#124; Active" | "АКТИВНО &#124;&#124; Активное" | CONTEXT_REQUIRED | Retain: Adjective gender/standalone-state context is unknown. |
| MEDIUM | Case variants | "AOA &#124;&#124; AoA" | "АОА &#124;&#124; Угол атаки" | CONTEXT_REQUIRED | Retain: Compact abbreviation versus expanded angle-of-attack wording; avionics remains deferred. |
| MEDIUM | Case variants | "BOSCALI &#124;&#124; Boscali" | "БОСКАЛИ &#124;&#124; Boscali" | CONTEXT_REQUIRED | Retain: Faction/place display context unknown; no lore naming policy inferred. |
| MEDIUM | Case variants | "CAMERA TRANSFORM &#124;&#124; Camera Transform" | "ТРАНСФОРМАЦИЯ КАМЕРЫ &#124;&#124; Преобразование камеры" | CONTEXT_REQUIRED | Retain: Editor/internal transform terminology is deferred. |
| MEDIUM | Case variants | "CREATE NEW &#124;&#124; Create New" | "СОЗДАТЬ &#124;&#124; Создать новый" | CONTEXT_REQUIRED | Retain: Omitted object versus explicit adjective may depend on UI context. |
| MEDIUM | Case variants | "DEVELOPMENT ROADMAP &#124;&#124; Development Roadmap" | "ПЛАН РАЗРАБОТКИ &#124;&#124; Дорожная карта разработки" | INTENTIONAL | Retain: Two natural synonyms; no demonstrated semantic defect. |
| MEDIUM | Case variants | "ENEMY &#124;&#124; Enemy" | "ВРАЖЕСКИЕ &#124;&#124; Враг" | CONTEXT_REQUIRED | Retain: Noun versus adjectival/plural UI context is unknown. |
| MEDIUM | Case variants | "FAR &#124;&#124; Far" | "ДАЛЬН. &#124;&#124; Далеко" | INTENTIONAL | Retain: Abbreviation versus expanded adverb may be intentional for space. |
| MEDIUM | Case variants | "FRIENDLY &#124;&#124; Friendly" | "СОЮЗНЫЕ &#124;&#124; Союзный" | CONTEXT_REQUIRED | Retain: Adjectival agreement/number may depend on UI context. |
| MEDIUM | Case variants | "Faction Funds &#124;&#124; Faction funds" | "Фонды фракций &#124;&#124; Средства фракции" | CONTEXT_REQUIRED | Retain: Potential plurality inconsistency; editor/statistics context is unproven. |
| MEDIUM | Case variants | "Faction Score &#124;&#124; Faction score" | "Оценка фракции &#124;&#124; Очки фракции" | CONTEXT_REQUIRED | Retain: Potential score terminology inconsistency; editor/statistics context is unproven. |
| MEDIUM | Case variants | "GUN &#124;&#124; Gun" | "ПИСТОЛЕТ &#124;&#124; Пушка" | CONTEXT_REQUIRED | Retain: Pistol versus cannon is suspicious, but the uppercase label may be deferred cockpit text; no global-invariant corruption. |
| MEDIUM | Case variants | "HIGH &#124;&#124; High" | "ВЫСОКИЙ &#124;&#124; Высокое" | CONTEXT_REQUIRED | Retain: Adjective gender may depend on the omitted noun. |
| MEDIUM | Case variants | "Inner Wing Pylons &#124;&#124; Inner wing pylons" | "Внутренние подкрыльевые пилоны &#124;&#124; Внутренние пилоны крыла" | INTENTIONAL | Retain: Both mean inner wing pylons; style synonym, not a proven semantic defect. |
| MEDIUM | Case variants | "LOW &#124;&#124; Low" | "НИЗКИЙ &#124;&#124; Низкое" | CONTEXT_REQUIRED | Retain: Adjective gender may depend on the omitted noun. |
| MEDIUM | Case variants | "MEDIUM &#124;&#124; Medium" | "СРЕДНИЕ &#124;&#124; Среднее" | CONTEXT_REQUIRED | Retain: Gender/number may depend on the omitted noun. |
| MEDIUM | Case variants | "MISSILE WARNING &#124;&#124; Missile Warning" | "РАКЕТНАЯ ОПАСНОСТЬ &#124;&#124; Предупреждение о ракете" | CONTEXT_REQUIRED | Retain: Warning label variants express the same threat; cockpit context is deferred. |
| MEDIUM | Case variants | "NAME &#124;&#124; Name" | "ИМЯ &#124;&#124; Название" | CONTEXT_REQUIRED | Retain: Personal name versus object name needs display context. |
| MEDIUM | Case variants | "NEW &#124;&#124; New" | "НОВЫЙ &#124;&#124; Новая" | CONTEXT_REQUIRED | Retain: Adjective gender may depend on the omitted noun. |
| MEDIUM | Case variants | "NO TARGET &#124;&#124; No Target" | "НЕТ ЦЕЛИ &#124;&#124; " | CONTEXT_REQUIRED | Retain: Empty target value is suspicious but may intentionally suppress an avionics label; deferred. |
| MEDIUM | Case variants | "Need Preview &#124;&#124; Need preview" | "Нужен предварительный просмотр &#124;&#124; Нужен предпросмотр" | INTENTIONAL | Retain: Two natural preview synonyms; no semantic defect proven. |
| MEDIUM | Case variants | "OBJECTIVE &#124;&#124; Objective" | "ЦЕЛЬ &#124;&#124; Задача" | CONTEXT_REQUIRED | Retain: Target versus task meaning requires context, including deferred editor use. |
| MEDIUM | Case variants | "OPTICAL &#124;&#124; Optical" | "ОПТИЧЕСКИЙ &#124;&#124; Оптическое" | CONTEXT_REQUIRED | Retain: Adjective gender and sensor context need confirmation. |
| MEDIUM | Case variants | "Outer Wing Pylons &#124;&#124; Outer wing pylons" | "Внешние подкрыльевые пилоны &#124;&#124; Пилоны внешнего крыла" | CONTEXT_REQUIRED | Retain: Both refer to outer wing pylons; awkward variant but no proven context-safe convergence. |
| MEDIUM | Case variants | "PRIMEVA ARMED LIBERATION ALLIANCE &#124;&#124; Primeva Armed Liberation Alliance" | "ВООРУЖЁННЫЙ ОСВОБОДИТЕЛЬНЫЙ АЛЬЯНС PRIMEVA &#124;&#124; Альянс вооруженного освобождения Primeva" | CONTEXT_REQUIRED | Retain: Proper faction/title convention and display context need confirmation; no invented lore. |
| MEDIUM | Case variants | "PRIMEVA &#124;&#124; Primeva" | "ПРИМЕВА &#124;&#124; Primeva" | CONTEXT_REQUIRED | Retain: Faction/place naming convention and display context need confirmation. |
| MEDIUM | Case variants | "PUBLIC &#124;&#124; Public" | "ПУБЛИЧНЫЙ &#124;&#124; Открытое" | CONTEXT_REQUIRED | Retain: Adjective gender versus visibility terminology requires lobby context. |
| MEDIUM | Case variants | "PVE &#124;&#124; PvE" | "ПВЕ &#124;&#124; PvE" | CONTEXT_REQUIRED | Retain: Abbreviation style differs but gameplay acronym meaning survives; naming convention unproven. |
| MEDIUM | Case variants | "READY &#124;&#124; Ready" | "ГОТОВО &#124;&#124; Готов" | CONTEXT_REQUIRED | Retain: State versus agreeing adjective may be intentional. |
| MEDIUM | Case variants | "REQUISITION &#124;&#124; Requisition" | "РЕКВИЗИЦИЯ &#124;&#124; Запросить" | CONTEXT_REQUIRED | Retain: Noun versus action verb may reflect status/button context. |
| MEDIUM | Case variants | "SOUTH BOSCALI GENERAL AVIATION &#124;&#124; South Boscali General Aviation" | "ГРАЖДАНСКАЯ АВИАЦИЯ ЮЖНОЙ BOSCALI &#124;&#124; Южный Boscali авиации общего назначения" | CONTEXT_REQUIRED | Retain: Awkward title variant, but entity/lore naming context is insufficient for a safe rewrite. |
| MEDIUM | Case variants | "TOTAL &#124;&#124; Total" | "ОБЩИЙ &#124;&#124; Общий вес" | CONTEXT_REQUIRED | Retain: Explicit weight versus general total may reflect different displays. |
| MEDIUM | Case variants | "VALUE &#124;&#124; Value &#124;&#124; value" | "СТОИМОСТЬ &#124;&#124; Стоимость &#124;&#124; значение" | CONTEXT_REQUIRED | Retain: Cost versus data value is context-dependent, including editor/internal use. |
| MEDIUM | Case variants | "WEAPONS &#124;&#124; Weapons" | "ОРУЖИЕ &#124;&#124; Вооружение" | INTENTIONAL | Retain: Two natural military UI synonyms; no semantic defect proven. |
| MEDIUM | Newline safety | " \n Path Node " | "Узел пути" | CONTEXT_REQUIRED | Retain formatting-sensitive manual key; layout/source evidence is insufficient. |
| MEDIUM | Newline safety | "Failed to save copy:\n" | "Не удалось сохранить копию:" | CONTEXT_REQUIRED | Retain formatting-sensitive manual key; layout/source evidence is insufficient. |
| MEDIUM | Russian typography | "20mm cannon firing explosive shells at a lower rate of fire than its rotary counterpart." | "20мм пушка, стреляющая осколочно-фугасными снарядами с более низкой скорострельностью, чем её роторный аналог." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre in ordinary Encyclopedia prose; no code or telemetry changed. |
| MEDIUM | Russian typography | "23mm AAA Emplacement" | "расположение 23мм ПВО" | CLEAR_LANGUAGE_IMPROVEMENT | AAA is anti-aircraft artillery; emplacement names the installation, not its location. Adjectival calibre typography. |
| MEDIUM | Russian typography | "A heavy forward fixed cannon, firing 57mm multi-purpose warheads at 250rpm. Automatically adjusts fuzing type and timing according to target parameters." | "Тяжёлое неподвижное носовое орудие, стреляющее 57мм многоцелевыми боеголовками со скоростью 250 выстр./мин. Автоматически настраивает тип и время срабатывания взрывателя в соответствии с параметрами цели." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre and correct cannon projectile terminology; fuzing and rate unchanged. |
| MEDIUM | Russian typography | "Allowing a traverse range from -10 to +10 degrees and an elevation range from -20 to +5 degrees, this aimable cannon pod is effective against light armor or aircraft at distances of up to 2000m." | "С углами горизонтальной наводки от -10 до +10 градусов и вертикальной от -20 до +5 градусов, эта наводимая пушечная гондола эффективна против лёгкой брони или самолётов на дальностях до 2000м." | CLEAR_LANGUAGE_IMPROVEMENT | Separate numeric distance and unit in ordinary prose. |
| MEDIUM | Russian typography | "An autoloaded 76mm gun, firing fin-stabilised guided projectiles. The gun requires airflow for cooling. It has a maximum firerate of 60RPM for 10 seconds, and can sustain a constant firerate of at least 40 RPM while moving at 500kph" | "Автоматическое 76мм орудие, стреляющее оперёнными управляемыми снарядами. Для охлаждения требуется воздушный поток. Максимальная скорострельность — 60 выстр./мин в течение 10 секунд, устойчивая — не менее 40 выстр./мин при скорости 500 км/ч" | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre typography in ordinary prose. |
| MEDIUM | Russian typography | "An fast firing, autoloaded 57mm gun, firing high velocity unguided shells. When fired against air targets, the shells use a proximity fuse to deal fragmentation damage." | "Скорострельное автоматическое 57мм орудие, стреляющее высокоскоростными неуправляемыми снарядами. При стрельбе по воздушным целям снаряды используют неконтактный взрыватель для нанесения осколочного урона." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre typography in ordinary prose. |
| MEDIUM | Russian typography | "Column 50m" | "Коллона 50м" | CONTEXT_REQUIRED | Retain: Column 50m/Concrete Wall 10m are editor/scenery labels; the bridge prose is a deferred mission hint. Not a global invariant defect. |
| MEDIUM | Russian typography | "Concrete Wall 10m" | "Бетонная стена 10м" | CONTEXT_REQUIRED | Retain: Column 50m/Concrete Wall 10m are editor/scenery labels; the bridge prose is a deferred mission hint. Not a global invariant defect. |
| MEDIUM | Russian typography | "Firing .50 caliber ammunition, the 12.7mm machine gun is effective against aircraft and lightly armored surface targets at ranges of up to 1km (0.61 miles)." | "Стреляя патронами .50 калибра, 12,7мм пулемёт эффективен против самолётов и легкобронированных наземных целей на дальностях до 1км (0,61 мили)." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre and distance spacing; no numeric values changed. |
| MEDIUM | Russian typography | "Occupying three structural hardpoints and weighing in at 1.6 tons loaded, this seven-barrelled, twin motor behemoth fires a mixed belt of 30mm armour piercing incendiary &amp; HE rounds at 3000rpm. Can be made effective against the majority of enemy vehicles, buildings, and slow moving aircraft." | "Занимая три силовых узла подвески и весом 1,6 тонны в снаряжённом состоянии, этот семиствольный двухмоторный гигант стреляет смешанной лентой из 30мм бронебойно-зажигательных и осколочно-фугасных снарядов со скоростью 3000 выстр./мин. Эффективен против большинства вражеской техники, зданий и тихоходных самолётов." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre typography in ordinary prose. |
| MEDIUM | Russian typography | "Prevent a column of vehicles from crossing the bridge to Boscali Island, before neutralizing the attack at its source." | " Предотвратите коллону транспорта от пересечения моста Острова Boscali, перед тем как нейтрализововать аттаку в ее источнике" | CONTEXT_REQUIRED | Retain: Column 50m/Concrete Wall 10m are editor/scenery labels; the bridge prose is a deferred mission hint. Not a global invariant defect. |
| MEDIUM | Russian typography | "Slower firing than its rotary counterparts, the 27mm Autocannon packs a heavier punch and is effective against both aircraft and moderately armored surface targets." | "Стреляя медленнее своих роторных аналогов, 27мм автопушка обладает большей мощностью и эффективна как против самолётов, так и против умеренно бронированных наземных целей." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre typography in ordinary prose. |
| MEDIUM | Russian typography | "The 20mm rotary cannon fires dual purpose explosive shells, effective against aircraft or moderately armored surface targets." | "20мм роторная пушка стреляет осколочно-фугасными снарядами двойного назначения, эффективными против самолётов или умеренно бронированных наземных целей." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre typography in ordinary prose. |
| MEDIUM | Russian typography | "The 25mm rotary cannon fires dual purpose explosive shells, effective against aircraft or moderately armored surface targets." | "25мм роторная пушка стреляет осколочно-фугасными снарядами двойного назначения, эффективными против самолётов или умеренно бронированных наземных целей." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre typography in ordinary prose. |
| MEDIUM | Russian typography | "The 30mm rotary cannon fires large, dual purpose explosive shells, effective against armored surface targets." | "30мм роторная пушка стреляет крупными осколочно-фугасными снарядами двойного назначения, эффективными против бронированных наземных целей." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre typography in ordinary prose. |
| MEDIUM | Russian typography | "The 35mm Autocannon packs a heavier punch than other aerial guns and is effective against many armored surface targets. Its superior ballistics allow it to remain effective at ranges exceeding 3000m." | "35мм автопушка обладает большей мощностью, чем другие авиапушки, и эффективна против многих бронированных наземных целей. Превосходная баллистика позволяет сохранять эффективность на дальностях свыше 3000м." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre and distance spacing in ordinary prose. |
| MEDIUM | Russian typography | "This gun shoots 30mm explosive shells effective against armored ground vehicles and buildings at ranges of over 2km (1.3m)." | "Эта пушка стреляет 30мм осколочно-фугасными снарядами, эффективными против бронированной наземной техники и зданий на дальностях свыше 2км (1,3 мили)." | CLEAR_LANGUAGE_IMPROVEMENT | Calibre/distance typography only; ambiguous source imperial-unit suffix is not reinterpreted. |
| MEDIUM | Russian typography | "This rotary cannon fires 20mm explosive shells at 6000 rounds per minute, making it highly effective against aerial targets." | "Эта роторная пушка стреляет 20мм осколочно-фугасными снарядами со скоростью 6000 выстрелов в минуту, что делает её высокоэффективной против воздушных целей." | CLEAR_LANGUAGE_IMPROVEMENT | Adjectival calibre typography in ordinary prose. |
| MEDIUM | Translation quality | "1 FORWARD BAY" | "1 ПЕРЕДНИЙ ОТКРЫТЫЙ" | CLEAR_LANGUAGE_IMPROVEMENT | Bay is a compartment, not the adjective open; existing Forward Weapon Bay confirms terminology. |
| MEDIUM | Translation quality | "23mm AAA Emplacement" | "расположение 23мм ПВО" | CLEAR_LANGUAGE_IMPROVEMENT | AAA is anti-aircraft artillery; emplacement names the installation, not its location. Adjectival calibre typography. |
| MEDIUM | Translation quality | "3 HEATER BAYS" | "3 ОТСЕКА НАГРЕВАТЕЛЯ" | CLEAR_LANGUAGE_IMPROVEMENT | Existing KR-67 Ifrit description explicitly defines heater bays as IRM-S2 compartments. |
| MEDIUM | Translation quality | "Dynamo Class Destroyer" | "Dynamo Class Destroyer" | CLEAR_LANGUAGE_IMPROVEMENT | Translate generic vessel type and class wording; preserve Dynamo. |
| MEDIUM | Translation quality | "FGA-57 Anvil" | "FGA-57 Anvil" | INTENTIONAL | Correct exact model/codename identity; no rewrite. |
| MEDIUM | Translation quality | "Forward Bay" | "Форвард Бэй" | CLEAR_LANGUAGE_IMPROVEMENT | Generic loadout compartment; existing Forward Weapon Bay provides context, not a codename. |
| MEDIUM | Translation quality | "Heater Bays" | "Нагревательные отсеки" | CLEAR_LANGUAGE_IMPROVEMENT | Existing Ifrit description explicitly explains the same heater-bay term. |
| MEDIUM | Translation quality | "M12 Jackknife" | "M12 Jackknife" | INTENTIONAL | Correct exact model/codename identity; no rewrite. |
| MEDIUM | Translation quality | "MSV R9 Stratolance Launcher" | "MSV R9 Stratolance Launcher" | CLEAR_LANGUAGE_IMPROVEMENT | Translate generic launcher noun; preserve MSV, R9 and Stratolance. |
| MEDIUM | Translation quality | "Rear Bay" | "Задний залив" | CLEAR_LANGUAGE_IMPROVEMENT | Generic loadout compartment, not a geographical bay; existing Rear Weapon Bay provides context. |

## All case-variant groups

155 groups already agree modulo capitalization/whitespace. All 189 groups remain unchanged; 34 context/style differences are explained above.

| Group | Source variants and current values | Disposition |
|---|---|---|
| ACTIVE | "ACTIVE" → "АКТИВНО"<br>"Active" → "Активное" | Retain; Adjective gender/standalone-state context is unknown. |
| ACTIVE AI AIRCRAFT | "Active AI Aircraft" → "Активные ИИ-самолёты"<br>"Active AI aircraft" → "Активные ИИ-самолёты" | INTENTIONAL: corresponding capitalization/whitespace only. |
| AIR BASE | "AIR BASE" → "АВИАБАЗА"<br>"Air Base" → "Авиабаза"<br>"Air base" → "Авиабаза" | INTENTIONAL: corresponding capitalization/whitespace only. |
| AIRBASE | "AIRBASE" → "АВИАБАЗА"<br>"Airbase" → "Авиабаза" | INTENTIONAL: corresponding capitalization/whitespace only. |
| AIRBASES | "AIRBASES" → "АВИАБАЗЫ"<br>"Airbases" → "Авиабазы" | INTENTIONAL: corresponding capitalization/whitespace only. |
| AIRCRAFT | "AIRCRAFT" → "ВОЗДУШНОЕ СРЕДСТВО"<br>"Aircraft" → "Воздушное средство" | INTENTIONAL: corresponding capitalization/whitespace only. |
| AIRSPEED | "AirSpeed" → "Воздушная скорость"<br>"Airspeed" → "Воздушная скорость" | INTENTIONAL: corresponding capitalization/whitespace only. |
| ALL | "ALL" → "ВСЕ"<br>"All" → "Все" | INTENTIONAL: corresponding capitalization/whitespace only. |
| ALLIES | "ALLIES" → "СОЮЗНИКИ"<br>"Allies" → "Союзники" | INTENTIONAL: corresponding capitalization/whitespace only. |
| AMMO | "AMMO" → "БОЕПРИПАСЫ"<br>"Ammo" → "Боеприпасы" | INTENTIONAL: corresponding capitalization/whitespace only. |
| AOA | "AOA" → "АОА"<br>"AoA" → "Угол атаки" | Retain; Compact abbreviation versus expanded angle-of-attack wording; avionics remains deferred. |
| AUDIO | "AUDIO" → "ЗВУК"<br>"Audio" → "Звук" | INTENTIONAL: corresponding capitalization/whitespace only. |
| BACK | "BACK" → "НАЗАД"<br>"Back" → "Назад" | INTENTIONAL: corresponding capitalization/whitespace only. |
| BINDING SETTINGS | "BINDING SETTINGS" → "НАСТРОЙКИ ПРИВЯЗОК"<br>"Binding Settings" → "Настройки привязок" | INTENTIONAL: corresponding capitalization/whitespace only. |
| BOSCALI | "BOSCALI" → "БОСКАЛИ"<br>"Boscali" → "Boscali" | Retain; Faction/place display context unknown; no lore naming policy inferred. |
| BRAKE | "BRAKE" → "ТОРМОЗ"<br>"Brake" → "Тормоз" | INTENTIONAL: corresponding capitalization/whitespace only. |
| BUILDINGS | "BUILDINGS" → "ЗДАНИЯ"<br>"Buildings" → "Здания" | INTENTIONAL: corresponding capitalization/whitespace only. |
| BURN TIME | "Burn Time" → "Время горения"<br>"Burn time" → "Время горения" | INTENTIONAL: corresponding capitalization/whitespace only. |
| BURN TIME : | "Burn Time :" → "Время горения :"<br>"Burn time :" → "Время горения :" | INTENTIONAL: corresponding capitalization/whitespace only. |
| BUY | "BUY" → "КУПИТЬ"<br>"Buy" → "Купить" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CAMERA CONTROLS | "CAMERA CONTROLS" → "УПРАВЛЕНИЕ КАМЕРОЙ"<br>"Camera Controls" → "Управление камерой" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CAMERA TRANSFORM | "CAMERA TRANSFORM" → "ТРАНСФОРМАЦИЯ КАМЕРЫ"<br>"Camera Transform" → "Преобразование камеры" | Retain; Editor/internal transform terminology is deferred. |
| CANCEL | "CANCEL" → "ОТМЕНА"<br>"Cancel" → "Отмена"<br>"cancel" → "отмена" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CHANGELOG | "CHANGELOG" → "СПИСОК ИЗМЕНЕНИЙ"<br>"Changelog" → "Список изменений" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CHAT | "CHAT" → "ЧАТ"<br>"Chat" → "Чат" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CHAT SETTINGS | "CHAT SETTINGS" → "НАСТРОЙКИ ЧАТА"<br>"Chat Settings" → "Настройки чата" | INTENTIONAL: corresponding capitalization/whitespace only. |
| COCKPIT CAMERA INERTIA | "Cockpit Camera Inertia" → "Инерция камеры в кабине"<br>"Cockpit camera inertia" → "Инерция камеры в кабине" | INTENTIONAL: corresponding capitalization/whitespace only. |
| COMMON SETTINGS | "COMMON SETTINGS" → "ОБЩИЕ НАСТРОЙКИ"<br>"Common Settings" → "Общие настройки" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CONFIRM | "CONFIRM" → "ПОДТВЕРДИТЬ"<br>"Confirm" → "Подтвердить" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CONNECTED | "CONNECTED" → "ПОДКЛЮЧЕНО"<br>"Connected" → "Подключено" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CONTROLS | "CONTROLS" → "УПРАВЛЕНИЕ"<br>"Controls" → "Управление" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CPU | "CPU" → "ЦП"<br>"Cpu" → "ЦП" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CREATE NEW | "CREATE NEW" → "СОЗДАТЬ"<br>"Create New" → "Создать новый" | Retain; Omitted object versus explicit adjective may depend on UI context. |
| CREDITS | "CREDITS" → "АВТОРЫ"<br>"Credits" → "Авторы" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CURRENT | "CURRENT" → "ТЕКУЩИЙ"<br>"Current" → "Текущий" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CUSTOMIZE | "CUSTOMIZE" → "НАСТРОИТЬ"<br>"Customize" → "Настроить" | INTENTIONAL: corresponding capitalization/whitespace only. |
| CUSTOMIZE MISSION | "CUSTOMIZE MISSION" → "НАСТРОИТЬ МИССИЮ"<br>"Customize Mission" → "Настроить миссию" | INTENTIONAL: corresponding capitalization/whitespace only. |
| DEFEAT | "DEFEAT" → "ПОРАЖЕНИЕ"<br>"Defeat" → "Поражение" | INTENTIONAL: corresponding capitalization/whitespace only. |
| DESCRIPTION | "DESCRIPTION" → "ОПИСАНИЕ"<br>"Description" → "Описание" | INTENTIONAL: corresponding capitalization/whitespace only. |
| DEVELOPMENT ROADMAP | "DEVELOPMENT ROADMAP" → "ПЛАН РАЗРАБОТКИ"<br>"Development Roadmap" → "Дорожная карта разработки" | Retain; Two natural synonyms; no demonstrated semantic defect. |
| DID YOU KNOW? | "DID YOU KNOW?" → "ЗНАЕТЕ ЛИ ВЫ?"<br>"Did you know?" → "Знаете ли вы?" | INTENTIONAL: corresponding capitalization/whitespace only. |
| DISPLAY SETTINGS | "DISPLAY SETTINGS" → "НАСТРОЙКИ ДИСПЛЕЯ"<br>"Display Settings" → "Настройки дисплея" | INTENTIONAL: corresponding capitalization/whitespace only. |
| DONATE | "DONATE" → "ПОЖЕРТВОВАТЬ"<br>"Donate" → "Пожертвовать" | INTENTIONAL: corresponding capitalization/whitespace only. |
| DONATE TO THE WAR EFFORT | "DONATE TO THE WAR EFFORT" → "ВКЛАД В ВОЕННЫЕ УСИЛИЯ"<br>"Donate to the War Effort" → "Вклад в военные усилия" | INTENTIONAL: corresponding capitalization/whitespace only. |
| EJECT | "EJECT" → "КАТАПУЛЬТИРОВАНИЕ"<br>"Eject" → "Катапультирование" | INTENTIONAL: corresponding capitalization/whitespace only. |
| ENCYCLOPEDIA | "ENCYCLOPEDIA" → "ЭНЦИКЛОПЕДИЯ"<br>"Encyclopedia" → "Энциклопедия" | INTENTIONAL: corresponding capitalization/whitespace only. |
| ENEMY | "ENEMY" → "ВРАЖЕСКИЕ"<br>"Enemy" → "Враг" | Retain; Noun versus adjectival/plural UI context is unknown. |
| ENVIRONMENT SETTINGS | "ENVIRONMENT SETTINGS" → "НАСТРОЙКИ ОКРУЖЕНИЯ"<br>"Environment Settings" → "Настройки окружения" | INTENTIONAL: corresponding capitalization/whitespace only. |
| ESCALATION | "ESCALATION" → "ЭСКАЛАЦИЯ"<br>"Escalation" → "Эскалация" | INTENTIONAL: corresponding capitalization/whitespace only. |
| EXIT | "EXIT" → "ВЫХОД"<br>"Exit" → "Выход" | INTENTIONAL: corresponding capitalization/whitespace only. |
| EXIT GAME | "EXIT GAME" → "ВЫЙТИ ИЗ ИГРЫ"<br>"Exit Game" → "Выйти из игры" | INTENTIONAL: corresponding capitalization/whitespace only. |
| FACTION FUNDS | "Faction Funds" → "Фонды фракций"<br>"Faction funds" → "Средства фракции" | Retain; Potential plurality inconsistency; editor/statistics context is unproven. |
| FACTION SCORE | "Faction Score" → "Оценка фракции"<br>"Faction score" → "Очки фракции" | Retain; Potential score terminology inconsistency; editor/statistics context is unproven. |
| FACTION SETTINGS | "FACTION SETTINGS" → "НАСТРОЙКИ ФРАКЦИИ"<br>"Faction Settings" → "Настройки фракции" | INTENTIONAL: corresponding capitalization/whitespace only. |
| FAR | "FAR" → "ДАЛЬН."<br>"Far" → "Далеко" | Retain; Abbreviation versus expanded adverb may be intentional for space. |
| FIELD OF VIEW | "FIELD OF VIEW" → "ПОЛЕ ЗРЕНИЯ"<br>"Field of View" → "Поле зрения" | INTENTIONAL: corresponding capitalization/whitespace only. |
| FILTERS | "FILTERS" → "ФИЛЬТРЫ"<br>"Filters" → "Фильтры" | INTENTIONAL: corresponding capitalization/whitespace only. |
| FORCES | "FORCES" → "СИЛЫ"<br>"Forces" → "Силы" | INTENTIONAL: corresponding capitalization/whitespace only. |
| FPS | "FPS" → "КАДР/С"<br>"fps" → "кадр/с" | INTENTIONAL: corresponding capitalization/whitespace only. |
| FREE FLIGHT | "FREE FLIGHT" → "СВОБОДНЫЙ ПОЛЁТ"<br>"Free Flight" → "Свободный полёт" | INTENTIONAL: corresponding capitalization/whitespace only. |
| FRIENDLY | "FRIENDLY" → "СОЮЗНЫЕ"<br>"Friendly" → "Союзный" | Retain; Adjectival agreement/number may depend on UI context. |
| FUEL | "FUEL" → "ТОПЛИВО"<br>"Fuel" → "Топливо" | INTENTIONAL: corresponding capitalization/whitespace only. |
| FUNDS : | "FUNDS :" → "СРЕДСТВА :"<br>"Funds :" → "Средства :" | INTENTIONAL: corresponding capitalization/whitespace only. |
| GAME MODE | "Game Mode" → "Режим игры"<br>"Game mode" → "Режим игры" | INTENTIONAL: corresponding capitalization/whitespace only. |
| GAME OVER | "GAME OVER" → "ИГРА ОКОНЧЕНА"<br>"Game Over" → "Игра окончена" | INTENTIONAL: corresponding capitalization/whitespace only. |
| GAMEPLAY | "GAMEPLAY" → "ГЕЙМПЛЕЙ"<br>"Gameplay" → "Геймплей" | INTENTIONAL: corresponding capitalization/whitespace only. |
| GENERAL | "GENERAL" → "ОБЩИЕ"<br>"General" → "Общие" | INTENTIONAL: corresponding capitalization/whitespace only. |
| GPU | "GPU" → "ГП"<br>"Gpu" → "ГП" | INTENTIONAL: corresponding capitalization/whitespace only. |
| GRAPHICS | "GRAPHICS" → "ГРАФИКА"<br>"Graphics" → "Графика" | INTENTIONAL: corresponding capitalization/whitespace only. |
| GUN | "GUN" → "ПИСТОЛЕТ"<br>"Gun" → "Пушка" | Retain; Pistol versus cannon is suspicious, but the uppercase label may be deferred cockpit text; no global-invariant corruption. |
| HIDE | "HIDE" → "СКРЫТЬ"<br>"Hide" → "Скрыть" | INTENTIONAL: corresponding capitalization/whitespace only. |
| HIDE UI | "HIDE UI" → "СКРЫТЬ ИНТЕРФЕЙС"<br>"Hide UI" → "Скрыть интерфейс" | INTENTIONAL: corresponding capitalization/whitespace only. |
| HIGH | "HIGH" → "ВЫСОКИЙ"<br>"High" → "Высокое" | Retain; Adjective gender may depend on the omitted noun. |
| HINT | "HINT" → "ПОДСКАЗКА"<br>"Hint" → "Подсказка" | INTENTIONAL: corresponding capitalization/whitespace only. |
| HOST | "HOST" → "ХОСТ"<br>"Host" → "Хост" | INTENTIONAL: corresponding capitalization/whitespace only. |
| HOST GAME | "HOST GAME" → "СОЗДАТЬ ИГРУ"<br>"Host Game" → "Создать игру" | INTENTIONAL: corresponding capitalization/whitespace only. |
| INNER WING PYLONS | "Inner Wing Pylons" → "Внутренние подкрыльевые пилоны"<br>"Inner wing pylons" → "Внутренние пилоны крыла" | Retain; Both mean inner wing pylons; style synonym, not a proven semantic defect. |
| INPUT | "INPUT" → "ВВОД"<br>"Input" → "Ввод" | INTENTIONAL: corresponding capitalization/whitespace only. |
| INSTANT ACTION | "INSTANT ACTION" → "БЫСТРЫЙ БОЙ"<br>"Instant Action" → "Быстрый бой" | INTENTIONAL: corresponding capitalization/whitespace only. |
| ITEM | "ITEM" → "ОБЪЕКТ"<br>"Item" → "Объект" | INTENTIONAL: corresponding capitalization/whitespace only. |
| JOIN | "JOIN" → "ПРИСОЕДИНИТЬСЯ"<br>"Join" → "Присоединиться" | INTENTIONAL: corresponding capitalization/whitespace only. |
| JOIN FACTION | "JOIN FACTION" → "ПРИСОЕДИНИТЬСЯ К ФРАКЦИИ"<br>"Join Faction" → "Присоединиться к фракции" | INTENTIONAL: corresponding capitalization/whitespace only. |
| JOIN OUR COMMUNITY | "JOIN OUR COMMUNITY" → "ПРИСОЕДИНИТЬСЯ К СООБЩЕСТВУ"<br>"Join Our Community" → "Присоединиться к сообществу"<br>"Join our Community" → "Присоединиться к сообществу" | INTENTIONAL: corresponding capitalization/whitespace only. |
| KEYBINDINGS | "KEYBINDINGS" → "НАЗНАЧЕНИЕ КЛАВИШ"<br>"Keybindings" → "Назначение клавиш" | INTENTIONAL: corresponding capitalization/whitespace only. |
| KILL FEED OPTIONS | "KILL FEED OPTIONS" → "НАСТРОЙКИ ЛЕНТЫ УНИЧТОЖЕНИЙ"<br>"Kill Feed Options" → "Настройки ленты уничтожений" | INTENTIONAL: corresponding capitalization/whitespace only. |
| LABEL | "LABEL" → "МЕТКА"<br>"Label" → "Метка" | INTENTIONAL: corresponding capitalization/whitespace only. |
| LASER | "LASER" → "ЛАЗЕР"<br>"Laser" → "Лазер" | INTENTIONAL: corresponding capitalization/whitespace only. |
| LOADING | "LOADING" → "ЗАГРУЗКА"<br>"Loading" → "Загрузка" | INTENTIONAL: corresponding capitalization/whitespace only. |
| LOADOUT | "LOADOUT" → "НАСТРОЙКА ВООРУЖЕНИЯ"<br>"Loadout" → "Настройка вооружения" | INTENTIONAL: corresponding capitalization/whitespace only. |
| LOBBY | "LOBBY" → "ЛОББИ"<br>"Lobby" → "Лобби" | INTENTIONAL: corresponding capitalization/whitespace only. |
| LOSSES | "LOSSES" → "ПОТЕРИ"<br>"Losses" → "Потери" | INTENTIONAL: corresponding capitalization/whitespace only. |
| LOW | "LOW" → "НИЗКИЙ"<br>"Low" → "Низкое" | Retain; Adjective gender may depend on the omitted noun. |
| MAP | "MAP" → "КАРТА"<br>"Map" → "Карта" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MAP OPTIONS | "MAP OPTIONS" → "НАСТРОЙКИ КАРТЫ"<br>"Map Options" → "Настройки карты" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MASS | "MASS" → "МАССА"<br>"Mass" → "Масса" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MEDIUM | "MEDIUM" → "СРЕДНИЕ"<br>"Medium" → "Среднее" | Retain; Gender/number may depend on the omitted noun. |
| MISSILE WARNING | "MISSILE WARNING" → "РАКЕТНАЯ ОПАСНОСТЬ"<br>"Missile Warning" → "Предупреждение о ракете" | Retain; Warning label variants express the same threat; cockpit context is deferred. |
| MISSILES | "MISSILES" → "РАКЕТЫ"<br>"Missiles" → "Ракеты" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MISSION COMPLETE | "MISSION COMPLETE" → "МИССИЯ ВЫПОЛНЕНА"<br>"Mission Complete" → "Миссия выполнена" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MISSION EDITOR | "MISSION EDITOR" → "РЕДАКТОР МИССИЙ"<br>"Mission Editor" → "Редактор миссий" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MISSION FAILED | "MISSION FAILED" → "МИССИЯ ПРОВАЛЕНА"<br>"Mission Failed" → "Миссия провалена" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MISSION PARAMETERS | "MISSION PARAMETERS" → "ПАРАМЕТРЫ МИССИИ"<br>"Mission Parameters" → "Параметры миссии" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MISSION PREVIEW | "Mission Preview" → "Предварительный просмотр миссии"<br>"Mission preview" → "Предварительный просмотр миссии" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MISSIONS | "MISSIONS" → "МИССИИ"<br>"Missions" → "Миссии" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MLRS ROCKET | "MLRS Rocket" → "Ракета РСЗО"<br>"MLRS rocket" → "Ракета РСЗО" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MULTIPLAYER | "MULTIPLAYER" → "МУЛЬТИПЛЕЕР"<br>"Multiplayer" → "Мультиплеер" | INTENTIONAL: corresponding capitalization/whitespace only. |
| MUNITIONS | "MUNITIONS" → "БОЕПРИПАСЫ"<br>"Munitions" → "Боеприпасы" | INTENTIONAL: corresponding capitalization/whitespace only. |
| NAME | "NAME" → "ИМЯ"<br>"Name" → "Название" | Retain; Personal name versus object name needs display context. |
| NEED PREVIEW | "Need Preview" → "Нужен предварительный просмотр"<br>"Need preview" → "Нужен предпросмотр" | Retain; Two natural preview synonyms; no semantic defect proven. |
| NEW | "NEW" → "НОВЫЙ"<br>"New" → "Новая" | Retain; Adjective gender may depend on the omitted noun. |
| NO LOCK | "NO LOCK" → "НЕТ ЗАХВАТА"<br>"No Lock" → "Нет захвата" | INTENTIONAL: corresponding capitalization/whitespace only. |
| NO TARGET | "NO TARGET" → "НЕТ ЦЕЛИ"<br>"No Target" → "" | Retain; Empty target value is suspicious but may intentionally suppress an avionics label; deferred. |
| NONE | "NONE" → "НЕТ"<br>"None" → "Нет" | INTENTIONAL: corresponding capitalization/whitespace only. |
| OBJECTIVE | "OBJECTIVE" → "ЦЕЛЬ"<br>"Objective" → "Задача" | Retain; Target versus task meaning requires context, including deferred editor use. |
| OBJECTIVES | "OBJECTIVES" → "ЗАДАЧИ"<br>"Objectives" → "Задачи" | INTENTIONAL: corresponding capitalization/whitespace only. |
| OK | "OK" → "ОК"<br>"Ok" → "ОК" | INTENTIONAL: corresponding capitalization/whitespace only. |
| OPTICAL | "OPTICAL" → "ОПТИЧЕСКИЙ"<br>"Optical" → "Оптическое" | Retain; Adjective gender and sensor context need confirmation. |
| OPTIONS | "OPTIONS" → "ПАРАМЕТРЫ"<br>"Options" → "Параметры" | INTENTIONAL: corresponding capitalization/whitespace only. |
| OTHER UNIT | "OTHER UNIT" → "ПРОЧИЕ ЮНИТЫ"<br>"Other Unit" → "Прочие юниты" | INTENTIONAL: corresponding capitalization/whitespace only. |
| OUTER WING PYLONS | "Outer Wing Pylons" → "Внешние подкрыльевые пилоны"<br>"Outer wing pylons" → "Пилоны внешнего крыла" | Retain; Both refer to outer wing pylons; awkward variant but no proven context-safe convergence. |
| OWNER | "OWNER" → "ВЛАДЕЛЕЦ"<br>"Owner" → "Владелец"<br>"owner" → "владелец" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PASSWORD | "Password" → "Пароль"<br>"password" → "пароль" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PILOT | "PILOT" → "ПИЛОТ"<br>"Pilot" → "Пилот" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PITCH | "PITCH" → "ТАНГАЖ"<br>"Pitch" → "Тангаж" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PLAY | "PLAY" → "ИГРАТЬ"<br>"Play" → "Играть" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PLAYER | "PLAYER" → "ИГРОК"<br>"Player" → "Игрок" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PLAYER MODE | "Player Mode" → "Режим игрока"<br>"Player mode" → "Режим игрока" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PLAYERS | "PLAYERS" → "ИГРОКИ"<br>"Players" → "Игроки" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PRIMEVA | "PRIMEVA" → "ПРИМЕВА"<br>"Primeva" → "Primeva" | Retain; Faction/place naming convention and display context need confirmation. |
| PRIMEVA ARMED LIBERATION ALLIANCE | "PRIMEVA ARMED LIBERATION ALLIANCE" → "ВООРУЖЁННЫЙ ОСВОБОДИТЕЛЬНЫЙ АЛЬЯНС PRIMEVA"<br>"Primeva Armed Liberation Alliance" → "Альянс вооруженного освобождения Primeva" | Retain; Proper faction/title convention and display context need confirmation; no invented lore. |
| PROFANITY FILTER | "Profanity Filter" → "Фильтр ненормативной лексики"<br>"Profanity filter" → "Фильтр ненормативной лексики" | INTENTIONAL: corresponding capitalization/whitespace only. |
| PUBLIC | "PUBLIC" → "ПУБЛИЧНЫЙ"<br>"Public" → "Открытое" | Retain; Adjective gender versus visibility terminology requires lobby context. |
| PVE | "PVE" → "ПВЕ"<br>"PvE" → "PvE" | Retain; Abbreviation style differs but gameplay acronym meaning survives; naming convention unproven. |
| QUALITY SETTINGS | "QUALITY SETTINGS" → "НАСТРОЙКИ КАЧЕСТВА"<br>"Quality Settings" → "Настройки качества" | INTENTIONAL: corresponding capitalization/whitespace only. |
| QUICK MATCH | "QUICK MATCH" → "БЫСТРЫЙ МАТЧ"<br>"Quick Match" → "Быстрый матч" | INTENTIONAL: corresponding capitalization/whitespace only. |
| QUIT | "QUIT" → "ВЫХОД"<br>"Quit" → "Выход" | INTENTIONAL: corresponding capitalization/whitespace only. |
| QUIT GAME | "QUIT GAME" → "ВЫЙТИ ИЗ ИГРЫ"<br>"Quit Game" → "Выйти из игры" | INTENTIONAL: corresponding capitalization/whitespace only. |
| QUIT MISSION | "QUIT MISSION" → "ПОКИНУТЬ МИССИЮ"<br>"Quit Mission" → "Покинуть миссию" | INTENTIONAL: corresponding capitalization/whitespace only. |
| RADAR | "RADAR" → "РАДАР"<br>"Radar" → "Радар" | INTENTIONAL: corresponding capitalization/whitespace only. |
| RANK | "RANK" → "РАНГ"<br>"Rank" → "Ранг" | INTENTIONAL: corresponding capitalization/whitespace only. |
| RANK 1 | "RANK 1" → "РАНГ 1"<br>"Rank 1" → "Ранг 1" | INTENTIONAL: corresponding capitalization/whitespace only. |
| RCS: | "RCS:" → "ЭПР:"<br>"rcs:" → "ЭПР:" | INTENTIONAL: corresponding capitalization/whitespace only. |
| READY | "READY" → "ГОТОВО"<br>"Ready" → "Готов" | Retain; State versus agreeing adjective may be intentional. |
| REFRESH | "REFRESH" → "ОБНОВИТЬ"<br>"Refresh" → "Обновить" | INTENTIONAL: corresponding capitalization/whitespace only. |
| REQUISITION | "REQUISITION" → "РЕКВИЗИЦИЯ"<br>"Requisition" → "Запросить" | Retain; Noun versus action verb may reflect status/button context. |
| RESET | "RESET" → "СБРОС"<br>"Reset" → "Сброс" | INTENTIONAL: corresponding capitalization/whitespace only. |
| RESTART MISSION | "RESTART MISSION" → "ПЕРЕЗАПУСТИТЬ МИССИЮ"<br>"Restart Mission" → "Перезапустить миссию" | INTENTIONAL: corresponding capitalization/whitespace only. |
| RESUME MISSION | "RESUME MISSION" → "ПРОДОЛЖИТЬ МИССИЮ"<br>"Resume Mission" → "Продолжить миссию" | INTENTIONAL: corresponding capitalization/whitespace only. |
| ROLL | "ROLL" → "КРЕН"<br>"Roll" → "Крен" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SCENERY | "SCENERY" → "ДЕКОРАЦИИ"<br>"Scenery" → "Декорации" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SCORE | "SCORE" → "ОЧКИ"<br>"Score" → "Очки" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SELECT AIRCRAFT | "SELECT AIRCRAFT" → "ВЫБОР ВОЗДУШНОГО СРЕДСТВА"<br>"Select Aircraft" → "Выбор воздушного средства" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SELECT FACTION | "SELECT FACTION" → "ВЫБОР ФРАКЦИИ"<br>"Select Faction" → "Выбор фракции" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SELECT MISSION | "SELECT MISSION" → "ВЫБОР МИССИИ"<br>"Select Mission" → "Выбор миссии" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SELL | "SELL" → "ПРОДАТЬ"<br>"Sell" → "Продать" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SERVER BROWSER | "SERVER BROWSER" → "ОБЗОР СЕРВЕРОВ"<br>"Server Browser" → "Обзор серверов" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SERVER FULL | "Server Full" → "Сервер заполнен"<br>"Server full" → "Сервер заполнен" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SETTINGS | "SETTINGS" → "НАСТРОЙКИ"<br>"Settings" → "Настройки" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SHIPS | "SHIPS" → "КОРАБЛИ"<br>"Ships" → "Корабли" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SINGLE PLAYER | "Single Player" → "Одиночная игра"<br>"Single player" → "Одиночная игра" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SINGLE PLAYER MISSIONS | "SINGLE PLAYER MISSIONS" → "ОДИНОЧНЫЕ МИССИИ"<br>"Single Player Missions" → "Одиночные миссии" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SINGLEPLAYER | "SINGLEPLAYER" → "ОДИНОЧНАЯ ИГРА"<br>"Singleplayer" → "Одиночная игра" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SOUTH BOSCALI GENERAL AVIATION | "SOUTH BOSCALI GENERAL AVIATION" → "ГРАЖДАНСКАЯ АВИАЦИЯ ЮЖНОЙ BOSCALI"<br>"South Boscali General Aviation" → "Южный Boscali авиации общего назначения" | Retain; Awkward title variant, but entity/lore naming context is insufficient for a safe rewrite. |
| SPECTATE | "SPECTATE" → "НАБЛЮДАТЬ"<br>"Spectate" → "Наблюдать" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SPEED | "SPEED" → "СКОРОСТЬ"<br>"Speed" → "Скорость" | INTENTIONAL: corresponding capitalization/whitespace only. |
| SPENT | "SPENT" → "ПОТРАЧЕННЫЙ"<br>"Spent" → "Потраченный" | INTENTIONAL: corresponding capitalization/whitespace only. |
| START MISSION | "START MISSION" → "НАЧАТЬ МИССИЮ"<br>"Start Mission" → "Начать миссию" | INTENTIONAL: corresponding capitalization/whitespace only. |
| T/A-30 COMPASS | "T/A-30 COMPASS" → "T/A-30 COMPASS"<br>"T/A-30 Compass" → "T/A-30 Compass" | INTENTIONAL: corresponding capitalization/whitespace only. |
| TARGET | "TARGET" → "ЦЕЛЬ"<br>"Target" → "Цель" | INTENTIONAL: corresponding capitalization/whitespace only. |
| TARGET SELECTION | "TARGET SELECTION" → "ВЫБОР ЦЕЛИ"<br>"Target Selection" → "Выбор цели" | INTENTIONAL: corresponding capitalization/whitespace only. |
| TEXTURE QUALITY | "TEXTURE QUALITY" → "КАЧЕСТВО ТЕКСТУР"<br>"Texture Quality" → "Качество текстур" | INTENTIONAL: corresponding capitalization/whitespace only. |
| THROTTLE | "THROTTLE" → "ТЯГА"<br>"Throttle" → "Тяга" | INTENTIONAL: corresponding capitalization/whitespace only. |
| TIME | "TIME" → "ВРЕМЯ"<br>"Time" → "Время" | INTENTIONAL: corresponding capitalization/whitespace only. |
| TIP | "TIP" → "СОВЕТ"<br>"Tip" → "Совет" | INTENTIONAL: corresponding capitalization/whitespace only. |
| TOTAL | "TOTAL" → "ОБЩИЙ"<br>"Total" → "Общий вес" | Retain; Explicit weight versus general total may reflect different displays. |
| TUTORIAL | "TUTORIAL" → "ОБУЧЕНИЕ"<br>"Tutorial" → "Обучение" | INTENTIONAL: corresponding capitalization/whitespace only. |
| TUTORIALS | "TUTORIALS" → "ОБУЧЕНИЕ"<br>"Tutorials" → "Обучение" | INTENTIONAL: corresponding capitalization/whitespace only. |
| UNIT SYSTEM | "UNIT SYSTEM" → "СИСТЕМА ЕДИНИЦ"<br>"Unit System" → "Система единиц" | INTENTIONAL: corresponding capitalization/whitespace only. |
| USER | "USER" → "ПОЛЬЗОВАТЕЛЬ"<br>"User" → "Пользователь" | INTENTIONAL: corresponding capitalization/whitespace only. |
| VALUE | "VALUE" → "СТОИМОСТЬ"<br>"Value" → "Стоимость"<br>"value" → "значение" | Retain; Cost versus data value is context-dependent, including editor/internal use. |
| VARIOUS OPTIONS | "VARIOUS OPTIONS" → "ПРОЧИЕ НАСТРОЙКИ"<br>"Various Options" → "Прочие настройки" | INTENTIONAL: corresponding capitalization/whitespace only. |
| VEHICLES | "VEHICLES" → "ТЕХНИКА"<br>"Vehicles" → "Техника" | INTENTIONAL: corresponding capitalization/whitespace only. |
| VICTORY | "VICTORY" → "ПОБЕДА"<br>"Victory" → "Победа" | INTENTIONAL: corresponding capitalization/whitespace only. |
| VOTE KICK | "VOTE KICK" → "ГОЛОСОВАНИЕ ЗА ИСКЛЮЧЕНИЕ"<br>"Vote Kick" → "Голосование за исключение" | INTENTIONAL: corresponding capitalization/whitespace only. |
| WAITING FOR PLAYERS | "Waiting for Players" → "Ожидание игроков"<br>"Waiting for players" → "Ожидание игроков" | INTENTIONAL: corresponding capitalization/whitespace only. |
| WEAPON | "WEAPON" → "ОРУЖИЕ"<br>"Weapon" → "Оружие" | INTENTIONAL: corresponding capitalization/whitespace only. |
| WEAPONS | "WEAPONS" → "ОРУЖИЕ"<br>"Weapons" → "Вооружение" | Retain; Two natural military UI synonyms; no semantic defect proven. |
| WORKSHOP | "WORKSHOP" → "МАСТЕРСКАЯ"<br>"Workshop" → "Мастерская" | INTENTIONAL: corresponding capitalization/whitespace only. |
| YAW | "YAW" → "РЫСКАНИЕ"<br>"Yaw" → "Рыскание" | INTENTIONAL: corresponding capitalization/whitespace only. |
