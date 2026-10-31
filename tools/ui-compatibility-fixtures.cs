// Offline Unity stand-ins; production methods are injected verbatim. / Без запуска игры.
using System;
using System.Collections.Generic;
using System.Reflection;
using System.Runtime.CompilerServices;
using HarmonyLib;
using UnityEngine;
using TMPro;

namespace UnityEngine
{
    public class GameObject { public bool activeInHierarchy = true; }
    public class Component
    {
        public GameObject gameObject = new GameObject();
        public List<Component> Ancestors = new List<Component>();
        public T GetComponentInParent<T>(bool includeInactive) where T : Component { return (T)GetComponentInParent(typeof(T), includeInactive); }
        public Component GetComponentInParent(Type type, bool includeInactive) { return Ancestors.Find(c => (includeInactive || c.gameObject.activeInHierarchy) && type.IsInstanceOfType(c)); }
        public int GetInstanceID() { return RuntimeHelpers.GetHashCode(this); }
    }
    public static class Resources
    {
        public static TMP_Text[] Texts = new TMP_Text[0];
        public static T[] FindObjectsOfTypeAll<T>() { return (T[])(object)Texts; }
    }
}
namespace TMPro
{
    public class TMP_Text : Component
    {
        private string backing;
        public bool enabled = true;
        public string text
        {
            [MethodImpl(MethodImplOptions.NoInlining)] get { return backing; }
            [MethodImpl(MethodImplOptions.NoInlining)] set { backing = value; }
        }
        [MethodImpl(MethodImplOptions.NoInlining)]
        public void SetText(string sourceText, bool syncTextInputBox = true) { backing = sourceText; LastSync = syncTextInputBox; }
        public bool LastSync;
        [MethodImpl(MethodImplOptions.NoInlining)] public void OnEnable() { }
    }
    public class TMP_InputField : Component { public TMP_Text textComponent; }
}
public class MissionMessages { }
public class MessageUI : Component { public TMP_Text messageText; public TMP_Text killFeedText; }
public class LeaderboardPlayerEntry : Component { public TMP_Text textName; }
namespace NuclearOption.Chat
{
    public class ChatSuggestionItemUI : Component { }
    public class ChatHoverCardUI : Component { public TMP_Text nameText; }
    public class AllowBanListItem : Component { public TMP_Text nameText; }
    public class ChatAutocompleteEngine { public string Header; }
    public class ChatAutocompleteUI : Component
    {
        public TMP_Text headerTitle = new TMP_Text();
        public TMP_Text headerCount = new TMP_Text();
        [MethodImpl(MethodImplOptions.NoInlining)]
        public void SetHeader(ChatAutocompleteEngine engine, int count)
        {
            headerTitle.SetText(engine.Header, false);
            headerCount.SetText(count.ToString(), false);
        }
    }
}
public class MissingHeader { public void SetHeader(string value, int count) { } }
public class WrongHeaderReturn { public int SetHeader(NuclearOption.Chat.ChatAutocompleteEngine engine, int count) { return 1; } }

namespace KoreanPatch
{
    public class Plugin
    {
        internal static string CurrentLanguage = "ru";
        internal static bool Enabled = true, isPatching = false, FontReady = false;
        internal static Plugin Instance = new Plugin();
        internal static Harmony HarmonyInstance;
        internal static Dictionary<string, string> Translations = new Dictionary<string, string>();
        internal static HashSet<string> TranslationKeys = new HashSet<string>();
        private HashSet<int> translatedInstances = new HashSet<int>();
        internal int translatedCount, misses, fits;
        internal static TestLog Log = new TestLog();
        private void RecordUntranslated(string text) { misses++; }
        private static bool IsDialogueBoxTitle(TMP_Text text) { return false; }
        private static bool ContainsKorean(string text) { return true; }
        private static void EnsureKoreanFallback(TMP_Text text) { }
        private void ApplySelectiveAutoFit(TMP_Text text, string value) { fits++; }
        internal void FastScan() { FastScanTmpTextAndFit(); }
        internal static MethodInfo Target(Type type, Type engine) { return FindChatHeaderTarget(type, engine); }
        internal bool InstallHeader() { return PatchChatAutocompleteHeader(); }
        // @PRODUCTION_DEFINITIONS@
    }
    public class TestLog { public void LogInfo(string text) { } public void LogWarning(string text) { throw new Exception(text); } }
}

// @BASELINE_PROBE@
public static class Tests
{
    static void Equal(object actual, object expected, string label)
    { if (!object.Equals(actual, expected)) throw new Exception(label + ": " + actual + " != " + expected); }
    static void CheckPaths(TMP_Text text, bool protectedText)
    {
        string expected = protectedText ? "Commands" : "Команды";
        text.text = "Commands";
        Equal(text.text, expected, "setter");
        text.SetText("Commands", false);
        Equal(text.text, "Commands", "arbitrary optional bool SetText is not patched");
        Equal(text.LastSync, false, "sync flag unchanged");
        // Bypass setters just as StringBuilder/serialized text does.
        typeof(TMP_Text).GetField("backing", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(text, "Commands");
        text.OnEnable();
        Equal(text.text, expected, "real OnEnable prefix/postfix");
        typeof(TMP_Text).GetField("backing", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(text, "Commands");
        KoreanPatch.Plugin.Instance.TranslateTmpComponent(text);
        Equal(text.text, expected, "periodic/OnEnable component path");
        Resources.Texts = new[] { text };
        int before = KoreanPatch.Plugin.Instance.fits;
        KoreanPatch.Plugin.Instance.FastScan();
        Equal(KoreanPatch.Plugin.Instance.fits - before, protectedText ? 0 : 1, "fitting protection");
    }
    public static int Main(string[] args)
    {
        try
        {
            var harmony = new Harmony("localization.ui.offline.fixture");
            try
            {
                var plugin = typeof(KoreanPatch.Plugin);
                KoreanPatch.Plugin.HarmonyInstance = harmony;
                KoreanPatch.Plugin.Translations.Add("Commands", "Команды");
                KoreanPatch.Plugin.TranslationKeys.Add("Commands");
                var baselineInput = new TMP_InputField(); var baselineBody = new TMP_Text();
                baselineInput.textComponent = baselineBody; baselineBody.Ancestors.Add(baselineInput);
                baselineBody.text = "Multiplayer";
                BaselineProbe.Instance.TranslateTmpComponent(baselineBody);
                Equal(baselineBody.text, "Мультиплеер", "baseline reproduces modification of editable input");
                var prefix = plugin.GetNestedType("TMP_Text_SetText_Patch", BindingFlags.NonPublic).GetMethod("Prefix", BindingFlags.Static | BindingFlags.NonPublic);
                harmony.Patch(typeof(TMP_Text).GetProperty("text").GetSetMethod(), prefix: new HarmonyMethod(prefix));
                var enablePatch = plugin.GetNestedType("TMP_OnEnable_Patch", BindingFlags.NonPublic);
                harmony.Patch(typeof(TMP_Text).GetMethod("OnEnable"),
                    prefix: new HarmonyMethod(enablePatch.GetMethod("Prefix", BindingFlags.Static | BindingFlags.NonPublic)),
                    postfix: new HarmonyMethod(enablePatch.GetMethod("Postfix", BindingFlags.Static | BindingFlags.NonPublic)));
                KoreanPatch.Plugin.CurrentLanguage = "de";
                Equal(KoreanPatch.Plugin.Instance.InstallHeader(), false, "non-Russian registration unchanged");
                KoreanPatch.Plugin.CurrentLanguage = "ru";
                Equal(KoreanPatch.Plugin.Instance.InstallHeader(), true, "real production header registration");
                Equal(Harmony.GetPatchInfo(typeof(TMP_Text).GetMethod("SetText")), null, "no new global SetText patch");
                var autocomplete = new NuclearOption.Chat.ChatAutocompleteUI();
                var engine = new NuclearOption.Chat.ChatAutocompleteEngine();
                foreach (string value in new[] { "Commands", "Mention player", "Suggestions" })
                {
                    if (!KoreanPatch.Plugin.TranslationKeys.Contains(value))
                    { KoreanPatch.Plugin.TranslationKeys.Add(value); KoreanPatch.Plugin.Translations.Add(value, "RU:" + value); }
                    engine.Header = value; autocomplete.SetHeader(engine, 7);
                    Equal(autocomplete.headerTitle.text, KoreanPatch.Plugin.Translations[value], "exact header translated immediately");
                    Equal(autocomplete.headerCount.text, "7", "numeric count unchanged");
                    Equal(autocomplete.headerTitle.LastSync, false, "header sync flag unchanged");
                }
                foreach (string value in new[] { "/help", "Commands for /kick", "Unknown header", "@Commands", " Commands " })
                { engine.Header = value; autocomplete.SetHeader(engine, 8); Equal(autocomplete.headerTitle.text, value, "unknown/command/argument header unchanged"); }
                KoreanPatch.Plugin.Enabled = false; engine.Header = "Commands"; autocomplete.SetHeader(engine, 1);
                Equal(autocomplete.headerTitle.text, "Commands", "disabled header bypass"); KoreanPatch.Plugin.Enabled = true;
                KoreanPatch.Plugin.CurrentLanguage = "de"; autocomplete.SetHeader(engine, 1);
                Equal(autocomplete.headerTitle.text, "Commands", "non-Russian header bypass"); KoreanPatch.Plugin.CurrentLanguage = "ru";
                CheckPaths(new TMP_Text(), false);
                var input = new TMP_InputField(); var body = new TMP_Text(); input.textComponent = body; body.Ancestors.Add(input);
                CheckPaths(body, true);
                input.gameObject.activeInHierarchy = body.gameObject.activeInHierarchy = false;
                CheckPaths(body, true);
                input.gameObject.activeInHierarchy = body.gameObject.activeInHierarchy = true;
                var placeholder = new TMP_Text(); placeholder.Ancestors.Add(input); CheckPaths(placeholder, false);
                var suggestion = new TMP_Text(); suggestion.Ancestors.Add(new NuclearOption.Chat.ChatSuggestionItemUI()); CheckPaths(suggestion, true);
                var hover = new NuclearOption.Chat.ChatHoverCardUI(); var hoverName = new TMP_Text(); hover.nameText = hoverName; hoverName.Ancestors.Add(hover); CheckPaths(hoverName, true);
                var hoverLabel = new TMP_Text(); hoverLabel.Ancestors.Add(hover); CheckPaths(hoverLabel, false);
                var ban = new NuclearOption.Chat.AllowBanListItem(); var banName = new TMP_Text(); ban.nameText = banName; banName.Ancestors.Add(ban); CheckPaths(banName, true);
                var leaderboard = new LeaderboardPlayerEntry(); var playerName = new TMP_Text(); leaderboard.textName = playerName; playerName.Ancestors.Add(leaderboard); CheckPaths(playerName, true);
                var messageUI = new MessageUI(); var feed = new TMP_Text(); messageUI.messageText = feed; feed.Ancestors.Add(messageUI); CheckPaths(feed, true);
                var kills = new TMP_Text(); messageUI.killFeedText = kills; kills.Ancestors.Add(messageUI); CheckPaths(kills, true);
                var header = new TMP_Text(); header.Ancestors.Add(messageUI); CheckPaths(header, false);
                foreach (string payload in new[] { "/help", "/kick @Commands reason", "@Commands", "Buy M12 Jackknife", "Commands: hello", "Enemy tanks cresting the ridge to the south!", new string('Я', 300) })
                {
                    foreach (var display in new[] { body, feed, suggestion, hoverName, banName, playerName })
                    {
                        display.text = payload; display.OnEnable(); KoreanPatch.Plugin.Instance.TranslateTmpComponent(display);
                        Equal(display.text, payload, "protected player content bytes");
                    }
                }
                int misses = KoreanPatch.Plugin.Instance.misses;
                typeof(TMP_Text).GetField("backing", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(body, "Private unknown message");
                KoreanPatch.Plugin.Instance.TranslateTmpComponent(body);
                Equal(KoreanPatch.Plugin.Instance.misses, misses, "private text not collected");
                KoreanPatch.Plugin.CurrentLanguage = "de"; CheckPaths(body, false); KoreanPatch.Plugin.CurrentLanguage = "ru";
                var engineType = typeof(NuclearOption.Chat.ChatAutocompleteEngine);
                Equal(KoreanPatch.Plugin.Target(null, engineType), null, "missing UI type skipped");
                Equal(KoreanPatch.Plugin.Target(typeof(NuclearOption.Chat.ChatAutocompleteUI), null), null, "missing engine type skipped");
                Equal(KoreanPatch.Plugin.Target(typeof(MissingHeader), engineType), null, "missing signature skipped");
                Equal(KoreanPatch.Plugin.Target(typeof(WrongHeaderReturn), engineType), null, "wrong return skipped");
                Console.WriteLine("PASS: baseline input defect; narrow real Harmony header producer; no global SetText(bool) patch; input/placeholder/player-name/suggestion/feed guards; unchanged commands, arguments, counts, non-Russian and missing targets.");
            }
            finally { harmony.UnpatchSelf(); }
            return 0;
        }
        catch (Exception e) { Console.Error.WriteLine(e); return 1; }
    }
}
