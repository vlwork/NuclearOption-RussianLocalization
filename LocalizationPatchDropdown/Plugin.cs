using System;
using System.Collections.Generic;
using System.Reflection;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using TMPro;
using UnityEngine.UI;

namespace LocalizationPatchDropdown
{
    // Addon for LocalizationPatch — adds dropdown option translation that the
    // TMP_Text.text setter hook misses. Calls LocalizationPatch's Translate()
    // via reflection so we stay in sync with its dictionary.
    [BepInPlugin("com.noms.localizationpatch.dropdown", "LocalizationPatch Dropdown Addon", "1.0.0")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log;
        static MethodInfo _translate;

        void Awake()
        {
            Log = Logger;

            if (!TryResolveTranslate())
            {
                Log.LogWarning("LocalizationPatch.Plugin.Translate not found — addon disabled. " +
                               "Make sure LocalizationPatch.dll is installed in the same plugins folder.");
                return;
            }

            new Harmony("com.noms.localizationpatch.dropdown").PatchAll();
            Log.LogInfo("LocalizationPatch Dropdown Addon v1.0.0 loaded.");
        }

        static bool TryResolveTranslate()
        {
            foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                string name;
                try { name = asm.GetName().Name; } catch { continue; }
                if (name != "LocalizationPatch") continue;

                Type t = null;
                try { t = asm.GetType("KoreanPatch.Plugin", throwOnError: false); } catch { }
                if (t == null) continue;

                _translate = t.GetMethod("Translate",
                    BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public);
                if (_translate != null) return true;
            }
            return false;
        }

        internal static string Translate(string s)
        {
            if (_translate == null || string.IsNullOrEmpty(s)) return s;
            try { return (string)_translate.Invoke(null, new object[] { s }); }
            catch { return s; }
        }
    }

    [HarmonyPatch(typeof(TMP_Dropdown), nameof(TMP_Dropdown.AddOptions), new Type[] { typeof(List<string>) })]
    internal static class Patch_TMP_Dropdown_AddOptions_Strings
    {
        static void Prefix(List<string> options)
        {
            if (options == null) return;
            for (int i = 0; i < options.Count; i++)
                options[i] = Plugin.Translate(options[i]);
        }
    }

    [HarmonyPatch(typeof(TMP_Dropdown), nameof(TMP_Dropdown.AddOptions), new Type[] { typeof(List<TMP_Dropdown.OptionData>) })]
    internal static class Patch_TMP_Dropdown_AddOptions_OptionData
    {
        static void Prefix(List<TMP_Dropdown.OptionData> options)
        {
            if (options == null) return;
            foreach (var o in options)
                if (o != null && !string.IsNullOrEmpty(o.text))
                    o.text = Plugin.Translate(o.text);
        }
    }

    [HarmonyPatch(typeof(Dropdown), nameof(Dropdown.AddOptions), new Type[] { typeof(List<string>) })]
    internal static class Patch_UI_Dropdown_AddOptions_Strings
    {
        static void Prefix(List<string> options)
        {
            if (options == null) return;
            for (int i = 0; i < options.Count; i++)
                options[i] = Plugin.Translate(options[i]);
        }
    }

    [HarmonyPatch(typeof(Dropdown), nameof(Dropdown.AddOptions), new Type[] { typeof(List<Dropdown.OptionData>) })]
    internal static class Patch_UI_Dropdown_AddOptions_OptionData
    {
        static void Prefix(List<Dropdown.OptionData> options)
        {
            if (options == null) return;
            foreach (var o in options)
                if (o != null && !string.IsNullOrEmpty(o.text))
                    o.text = Plugin.Translate(o.text);
        }
    }
}
