# Nuclear Option — русская локализация

Самостоятельный BepInEx-мод русской локализации **Nuclear Option**. Мод переводит основные меню, Encyclopedia и общий интерфейс по словарю `ru.json`. В комплект входят основной плагин, дополнение для выпадающих списков и шрифт Tektur для кириллицы.

## Требования

- Nuclear Option для Windows;
- BepInEx 5.x, установленный в папку игры;
- один предварительный запуск игры после установки BepInEx.

## Установка

1. Скачайте ZIP из GitHub Release.
2. Распакуйте его в корень Nuclear Option с сохранением структуры папок.
3. Убедитесь, что существуют файлы:
   - `BepInEx\plugins\LocalizationPatch\LocalizationPatch.dll`;
   - `BepInEx\plugins\LocalizationPatch\LocalizationPatchDropdown.dll`;
   - `BepInEx\plugins\LocalizationPatch\ru.json`;
   - `BepInEx\plugins\LocalizationPatch\Tektur-Reg.ttf`.
4. Запустите игру. При необходимости задайте `Language = ru` в `BepInEx\config\com.noms.localizationpatch.cfg`.

Для установки собранной локальной версии разработчик может выполнить:

```powershell
.\scripts\install-local.ps1 -GameDir 'G:\SteamLibrary\steamapps\common\Nuclear Option'
```

Скрипт сохраняет полную резервную копию прежней папки в `BepInEx\LocalizationPatchBackups`, вне области сканирования плагинов, и оставляет активными ровно две DLL.

## Обновление

Закройте игру и установите новую версию поверх старой. При ручном обновлении сначала сохраните копию `BepInEx\plugins\LocalizationPatch`. Не оставляйте в `BepInEx\plugins` старые DLL, даже если в имени есть `backup`, `old` или номер версии: BepInEx может загрузить любой файл с расширением `.dll`.

`install-local.ps1` делает резервную копию автоматически, удаляет из активной папки старые DLL и DLL-backup-файлы, затем устанавливает только:

- `LocalizationPatch.dll`;
- `LocalizationPatchDropdown.dll`.

## Удаление

1. Закройте игру.
2. Удалите `BepInEx\plugins\LocalizationPatch` или переместите эту папку за пределы `BepInEx\plugins`.
3. При желании удалите `BepInEx\config\com.noms.localizationpatch.cfg`.

Резервные копии в `BepInEx\LocalizationPatchBackups` автоматически не удаляются.

## Что остаётся на английском

Названия техники, вооружения и юнитов намеренно сохраняются в оригинальном английском написании, в том числе внутри описаний. `IR Flares` и `Radar Countermeasures` также остаются без перевода.

## Известные ограничения

- cockpit/HUD/MFD может частично оставаться на английском;
- мод намеренно не сканирует всю cockpit hierarchy и не пытается автоматически переводить каждый авионический дисплей;
- Mission Editor пока переведён не полностью;
- mission hints пока переведены не полностью;
- после обновления игры новые или изменённые строки могут временно оставаться на английском до обновления `ru.json`.

## Горячие клавиши

- `F10` или `F9` — показать/скрыть диагностическую панель;
- `Ctrl+F10` — перезагрузить `ru.json`;
- `Ctrl+F11` — выгрузить игровые строки для работы переводчика.
