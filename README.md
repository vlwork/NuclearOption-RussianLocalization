# Nuclear Option — LocalizationPatch (source)

Source code for `LocalizationPatch.dll`, the BepInEx plugin behind every
Nuclear Option language patch published under this account.

The plugin itself contains **no translations**. It loads a `<lang>.json` file that sits
next to it and substitutes text at runtime, so one binary serves all languages. Each
language patch ships this same DLL plus its own JSON and font.

## Language patches built on this plugin

| Language | Repository |
|---|---|
| Korean | [NuclearOption-KoreanPatch](https://github.com/9138noms/NuclearOption-KoreanPatch) |
| Ukrainian | [NuclearOption-UkrainianPatch](https://github.com/9138noms/NuclearOption-UkrainianPatch) |
| Russian | [NuclearOption-RussianPatch](https://github.com/9138noms/NuclearOption-RussianPatch) |
| Belarusian | [NuclearOption-BelarusianPatch](https://github.com/9138noms/NuclearOption-BelarusianPatch) |
| German | [NuclearOption-GermanPatch](https://github.com/9138noms/NuclearOption-GermanPatch) |
| French | [NuclearOption-FrenchPatch](https://github.com/9138noms/NuclearOption-FrenchPatch) |
| Spanish | [NuclearOption-SpanishPatch](https://github.com/9138noms/NuclearOption-SpanishPatch) |
| Italian | [NuclearOption-ItalianPatch](https://github.com/9138noms/NuclearOption-ItalianPatch) |
| Portuguese (BR) | [NuclearOption-PortuguesePatch](https://github.com/9138noms/NuclearOption-PortuguesePatch) |
| Turkish | [NuclearOption-TurkishPatch](https://github.com/9138noms/NuclearOption-TurkishPatch) |
| Chinese (Traditional) | [NuclearOption-TraditionalChinesePatch](https://github.com/9138noms/NuclearOption-TraditionalChinesePatch) |
| Norwegian | [NuclearOption-NorwegianPatch](https://github.com/9138noms/NuclearOption-NorwegianPatch) |

Want a language that isn't listed? See the
[Translation Toolkit](https://github.com/9138noms/NuclearOption-TranslationToolkit) —
no programming required.

## Building

Requires the .NET SDK (any version that can target `net472`), a copy of Nuclear Option,
and BepInEx 5 installed into the game folder. The project references the game's own
assemblies, so they are never redistributed here.

```
dotnet build -c Release
```

If the game is not at the default Steam path:

```
dotnet build -c Release -p:NuclearOptionDir="D:\Games\Nuclear Option"
```

Output lands in `bin/Release/net472/LocalizationPatch.dll`.

Builds are not byte-identical between machines — .NET writes a fresh module MVID on
every compile and embeds source paths. To confirm a released DLL matches this source,
compare the decompiled IL rather than file hashes.

## How it works

Two paths put translated text on screen:

1. **Setter hooks** — Harmony patches on `TMP_Text.text`, `Text.text` and
   `TextMeshProUGUI.OnEnable`. The `OnEnable` hook is what stops prefab-authored text
   from flashing English when a panel opens.
2. **Periodic sweep** — every `ScanInterval` seconds (default 0.3) the plugin walks
   `Resources.FindObjectsOfTypeAll<TMP_Text>()` and translates anything the hooks did
   not catch. Instance IDs of already-translated components are cached so the sweep
   stays cheap.

Lookup is an exact, whole-string match after `Trim()`. A small set of patterns handles
text that carries a runtime value — `Word (N)`, `Word [N]`, `NN. Name`, `LABEL: value`
and a few others — so a label only needs one entry regardless of the number beside it.

Non-Latin scripts need a font the game does not ship. The plugin registers the font
file found next to it (alphabetically first `.ttf`/`.otf`), builds a TMP font asset from
it, pre-populates the glyphs used by the translation file, and adds it to TMP's global
fallback list.

Strings the plugin could not match are collected and written to `untranslated.txt` in
the plugin folder, which is how new translation work gets found after a game update.

## Configuration

`BepInEx/config/com.noms.localizationpatch.cfg`

| Key | Default | Meaning |
|---|---|---|
| `Language` | `auto` | Language code. `auto` picks the single `<lang>.json` in the folder. |
| `ScanInterval` | `0.3` | Seconds between full text sweeps. Raise it if the sweep costs too much CPU. |

## Hotkeys

| Key | Action |
|---|---|
| `F10` | Toggle the debug overlay |
| `Ctrl+F10` | Reload the translation JSON without restarting |
| `Ctrl+F11` | Dump game strings for translation work |

## License

No obfuscation is used anywhere in this project, and nothing here talks to the network,
starts processes, or touches anything outside the game's own folder.

Reuse and adaptation for Nuclear Option mods is welcome; please credit the original.
