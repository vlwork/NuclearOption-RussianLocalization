# Nuclear Option — русская локализация

Русская локализация **Nuclear Option** на базе **BepInEx 5**.

Проект предназначен для полноценного использования русского языка в игре и содержит основной плагин локализации, дополнительный модуль для элементов интерфейса, русский словарь и кириллический шрифт.

Текущая версия локализации основана на ветке разработки **3.6.4** и содержит **3 729 записей перевода**.

## Что переводится

Локализация охватывает:

- основные меню;
- Encyclopedia;
- большую часть стандартного интерфейса;
- игровые сообщения;
- поддерживаемые сообщения миссий;
- элементы выпадающих списков.

Для некоторых названий намеренно сохраняется оригинальное английское написание.

В частности, обозначения моделей, собственные названия техники, вооружения, юнитов и кодовые имена обычно остаются на английском.

Строки:

- `IR Flares`;
- `Radar Countermeasures`;
- `Continue`;
- `M12 Jackknife`

также намеренно сохраняются без перевода.

## Известные ограничения

Локализация пока не считается полностью завершённой.

Частично на английском могут оставаться:

- cockpit / HUD / MFD;
- Mission Editor;
- mission hints;
- новые или изменённые строки после обновлений Nuclear Option.

Плагин намеренно не выполняет агрессивное сканирование всей структуры cockpit и не пытается автоматически изменять каждый авионический дисплей.

Версия 3.6.4 также требует дополнительной проверки непосредственно в игре, включая режимы host/client.

Чат и системные уведомления о подключении и отключении игроков не перехватываются.

# Установка

## Требования

- Nuclear Option для Windows;
- BepInEx 5.x, установленный в папку игры;
- один предварительный запуск игры после установки BepInEx.

## Рекомендуемый способ

1. Скачайте ZIP-архив нужной версии из раздела **Releases**.
2. Распакуйте архив в любую временную папку.
3. Запустите `Install.cmd`.
4. Установщик попытается автоматически найти Nuclear Option в библиотеках Steam.
5. Если игра не найдена автоматически, выберите папку Nuclear Option вручную — ту, где находится `NuclearOption.exe`.

Установщик:

- проверяет наличие Nuclear Option и BepInEx 5;
- проверяет структуру релизного пакета;
- создаёт резервную копию предыдущей локализации вне дерева `BepInEx`;
- обнаруживает старые или дублирующиеся сборки LocalizationPatch;
- переносит подтверждённые дубли в резервную копию;
- устанавливает ровно четыре runtime-файла;
- после копирования проверяет SHA-256 установленных файлов;
- не устанавливает лицензионные и provenance-документы в `BepInEx\plugins`.

После установки активные файлы находятся здесь:

```text
BepInEx\plugins\LocalizationPatch\LocalizationPatch.dll
BepInEx\plugins\LocalizationPatch\LocalizationPatchDropdown.dll
BepInEx\plugins\LocalizationPatch\ru.json
BepInEx\plugins\LocalizationPatch\Tektur-Reg.ttf
```

Если запуск `Install.cmd` запрещён политиками системы, из распакованного релизного архива можно выполнить:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\Install.ps1
```

## Ручная установка

Если автоматический установщик использовать нельзя, скопируйте папку:

```text
BepInEx
```

из релизного архива в корневую папку Nuclear Option с объединением каталогов.

При ручной установке рекомендуется заранее сохранить существующую папку:

```text
BepInEx\plugins\LocalizationPatch
```

за пределами всего дерева `BepInEx`.

При необходимости язык можно указать вручную в:

```text
BepInEx\config\com.noms.localizationpatch.cfg
```

Параметр:

```ini
Language = ru
```
# Обновление

Рекомендуемый способ обновления:

1. Закройте Nuclear Option.
2. Скачайте новый релиз.
3. Распакуйте архив.
4. Запустите `Install.cmd`.

Установщик автоматически создаст новую резервную копию предыдущей версии перед заменой файлов.

При ручном обновлении сначала сохраните:

```text
BepInEx\plugins\LocalizationPatch
```

за пределами дерева `BepInEx`, затем скопируйте новые runtime-файлы поверх старых.

Не храните старые DLL внутри `BepInEx`, даже под именами вроде:

```text
LocalizationPatch.old.dll
LocalizationPatch.backup.dll
LocalizationPatch-3.6.3.dll
```

BepInEx может обнаружить их как активные плагины.
# Удаление

Закройте Nuclear Option.

Удалите:

```text
BepInEx\plugins\LocalizationPatch
```

При необходимости также можно удалить конфигурацию:

```text
BepInEx\config\com.noms.localizationpatch.cfg
```

Оригинальные игровые файлы Nuclear Option при обычной установке локализации напрямую не изменяются.

# Горячие клавиши

- `F10` или `F9` — показать или скрыть диагностическую панель;
- `Ctrl+F10` — перезагрузить `ru.json`;
- `Ctrl+F11` — выгрузить игровые строки для работы над переводом.

# Для разработчиков

## Сборка

Требования:

- Windows PowerShell 5.1 или новее;
- Python 3.10 или новее;
- .NET SDK;
- локальная поддержка .NET Framework 4.7.2;
- установленная Nuclear Option;
- BepInEx 5.

Сборка:

```powershell
.\scripts\build.ps1
```

При необходимости можно явно указать каталог игры:

```powershell
.\scripts\build.ps1 -GameDir 'G:\SteamLibrary\steamapps\common\Nuclear Option'
```

Если выполнение PowerShell-скриптов заблокировано политикой системы:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1
```

Игровые DLL используются только как локальные зависимости сборки и не включаются в репозиторий.

## Локальная установка сборки

```powershell
.\scripts\install-local.ps1 -GameDir 'G:\SteamLibrary\steamapps\common\Nuclear Option'
```

Перед заменой активной версии скрипт создаёт резервную копию вне дерева `BepInEx`.

Предварительная проверка без изменения файлов:

```powershell
.\scripts\install-local.ps1 -GameDir 'G:\SteamLibrary\steamapps\common\Nuclear Option' -WhatIf
```

## Создание релизного архива

```powershell
.\scripts\package.ps1 -Version 3.6.4
```

Создаётся архив вида:

```text
release\NuclearOption-RussianLocalization-v3.6.4.zip
```

В релизный архив входят `Install.cmd`, `Install.ps1` и четыре runtime-файла в:

```text
BepInEx/plugins/LocalizationPatch/
```

а также документы лицензирования, attribution и provenance на уровне корня архива.

## Проверка локализации

```powershell
.\scripts\audit-localization.ps1
.\scripts\audit-localization.ps1 -Strict
python .\tools\test-localization-qa.py
```

Текущий проверенный словарь содержит:

```text
3 729 записей
```

# Структура репозитория

```text
src/LocalizationPatch
```

Основной BepInEx-плагин.

```text
src/LocalizationPatchDropdown
```

Дополнительный плагин для элементов выпадающих списков.

```text
localization/ru.json
```

Основной русский словарь.

```text
fonts/Tektur-Reg.ttf
```

Шрифт с поддержкой кириллицы.

```text
scripts
```

Скрипты сборки, проверки, установки и упаковки.

```text
tools
```

Инструменты автоматической проверки локализации.

```text
reports
```

Отчёты по аудиту и стабилизации.

# Лицензии и происхождение материалов

Этот репозиторий содержит материалы с различными условиями использования.

Собственные скрипты, QA-инструменты, документация и идентифицируемые изменения, созданные в рамках данного репозитория, распространяются на условиях [MIT License](LICENSE-CODE).

Идентифицируемые русские переводы, созданные участниками этого репозитория, распространяются на условиях [Creative Commons Attribution 4.0 International](LICENSE-TRANSLATION).

Это **не означает**, что MIT или CC BY 4.0 распространяются на весь исторически унаследованный код или весь файл перевода.

`LocalizationPatch` и `LocalizationPatchDropdown` основаны на:

[9138noms/NuclearOption-LocalizationPatch](https://github.com/9138noms/NuclearOption-LocalizationPatch)

Унаследованный код этого проекта данным репозиторием не перелицензируется.

Русский перевод исторически основан на:

[9138noms/NuclearOption-RussianPatch](https://github.com/9138noms/NuclearOption-RussianPatch)

Сохраняется указание авторства предыдущих участников перевода:

- Shumatsu [UMA];
- Jonyx2;
- хомяк.

Условия повторного использования унаследованных частей перевода требуют отдельного уточнения.

Шрифт **Tektur** распространяется на условиях **SIL Open Font License 1.1**.

Текст Nuclear Option и другие материалы, происходящие непосредственно из игры, остаются собственностью **Shockfront Studios Pty Ltd** или соответствующих лицензиаров и не лицензируются данным репозиторием.

Подробные условия и границы происхождения материалов:

- [LICENSE.md](LICENSE.md)
- [LICENSE-CODE](LICENSE-CODE)
- [LICENSE-TRANSLATION](LICENSE-TRANSLATION)
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- [localization/PROVENANCE.md](localization/PROVENANCE.md)
- [third_party/README.md](third_party/README.md)

# Благодарности

Проект основан на предыдущей работе сообщества Nuclear Option.

Отдельная благодарность:

- Shumatsu [UMA];
- Jonyx2;
- хомяк;
- 9138noms;
- другим участникам исходных проектов локализации и плагина.

---

**Nuclear Option — русская локализация** является независимым неофициальным проектом сообщества и не является продуктом Shockfront Studios.