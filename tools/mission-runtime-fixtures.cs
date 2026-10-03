// Offline fixtures only / автономные проверки, не имитация выполненного теста в игре.
// Production definitions are extracted verbatim; only Unity/game producers are mocked.
using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Runtime.CompilerServices;
using HarmonyLib;

namespace KoreanPatch
{
    public class Plugin
    {
        internal static bool Enabled = true;
        internal static Plugin Instance = new Plugin();
        internal static Harmony HarmonyInstance;
        internal static TestLog Log = new TestLog();
        internal static Dictionary<string, string> Translations = new Dictionary<string, string>();
        internal static HashSet<string> TranslationKeys = new HashSet<string>();
        internal int translatedCount;
        private void RecordUntranslated(string text) { }
        internal bool InstallForTests() { return PatchMissionMessageProducer(); }
        internal void LoadForTests(string path)
        {
            Translations.Clear();
            TranslationKeys.Clear();
            ParseSimpleJson(File.ReadAllText(path, System.Text.Encoding.UTF8));
            foreach (string key in Translations.Keys) TranslationKeys.Add(key);
        }
        // @PRODUCTION_DEFINITIONS@
    }

    internal class TestLog
    {
        public void LogInfo(string value) { }
        public void LogWarning(string value) { throw new Exception(value); }
    }
}

public class FactionHQ { }

// The local copy/network split, faction filter and display-only method mirror inspected IL.
public class MissionMessages
{
    public readonly List<string> Display = new List<string>();
    public string NetworkPayload;
    public FactionHQ NetworkFaction;
    public bool NetworkSound;
    public bool IsServer;
    public FactionHQ LocalFaction;
    public int Sounds;

    [MethodImpl(MethodImplOptions.NoInlining)]
    private void ShowMessgeLocal(string message, bool playsound, FactionHQ filterFaction)
    {
        if (filterFaction == null || Object.ReferenceEquals(filterFaction, LocalFaction))
        {
            Display.Add(message);
            if (playsound) Sounds++;
        }
    }

    public void ShowMessage(string message, bool playsound, FactionHQ faction, bool sendToClients)
    {
        ShowMessgeLocal(message, playsound, faction);
        if (sendToClients)
        {
            NetworkPayload = message;
            NetworkFaction = faction;
            NetworkSound = playsound;
        }
    }

    public void ReceiveRpc(string message, bool playsound, FactionHQ faction)
    {
        if (!IsServer) ShowMessgeLocal(message, playsound, faction);
    }

    public void Chat(string message) { Display.Add(message); }
    public void Join(string name, string color) { Display.Add("<color=#" + color + ">" + name + " joined the game</color>"); }
    public string Feed() { return String.Join("\n", Display.ToArray()); }
}

internal class Outcome
{
    public string UniqueName;
    public string Message;
    public void Complete(MissionMessages producer)
    {
        producer.ShowMessage(Message, false, null, true);
    }
}

internal static class RuntimeTests
{
    private static readonly string[][] Pairs = new string[][]
    {
        // @REVIEWED_PAIRS@
    };
    private static int passed;

    private static void Equal(object actual, object expected, string reason)
    {
        if (!Object.Equals(actual, expected)) throw new Exception(reason + ": expected " + expected + ", got " + actual);
    }

    private static void Test(string name, Action action)
    {
        action();
        passed++;
        Console.WriteLine("PASS: " + name);
    }

    [MethodImpl(MethodImplOptions.NoInlining)]
    public static int Run(string localization)
    {
        KoreanPatch.Plugin.Instance.LoadForTests(localization);
        KoreanPatch.Plugin.HarmonyInstance = new Harmony("localization.mission.offline.fixture");
        try
        {
            Test("actual production registration targets only the private display producer", delegate {
                Equal(KoreanPatch.Plugin.Instance.InstallForTests(), true, "registration");
                MethodInfo target = typeof(MissionMessages).GetMethod("ShowMessgeLocal", BindingFlags.NonPublic | BindingFlags.Instance);
                Patches info = Harmony.GetPatchInfo(target);
                Equal(info.Prefixes.Count, 1, "prefix count");
                Equal(info.Postfixes.Count, 0, "no postfix");
                Equal(info.Transpilers.Count, 0, "no transpiler");
                Equal(info.Prefixes[0].PatchMethod.Name, "Prefix", "prefix method");
                Equal(info.Prefixes[0].PatchMethod.DeclaringType.Name, "MissionMessages_Local_Patch", "production prefix");
                foreach (MethodBase patched in Harmony.GetAllPatchedMethods()) Equal(patched, target, "no chat/network/feed hook");
            });
            Test("all 13 exact reviewed messages translate through the real Harmony prefix", delegate {
                foreach (string[] item in Pairs)
                {
                    MissionMessages producer = new MissionMessages();
                    producer.ShowMessage(item[0], false, null, true);
                    Equal(producer.Display[0], item[1], "reviewed translation");
                    Equal(producer.NetworkPayload, item[0], "original network source");
                }
            });
            Test("exact K92 message and both K92 callsigns preserved", delegate {
                string[] k92 = Array.Find(Pairs, delegate(string[] p) { return p[0].Contains("preparing to seize"); });
                Equal(KoreanPatch.Plugin.TranslateMissionMessage(k92[0]), k92[1], "K92 translation");
                Equal(k92[1].Split(new string[] { "K92" }, StringSplitOptions.None).Length, 3, "two K92 tokens");
            });
            Test("real Translate and producer are idempotent for every reviewed Russian value", delegate {
                foreach (string[] item in Pairs)
                {
                    Equal(KoreanPatch.Plugin.Translate(item[1]), item[1], "TMP second pass");
                    Equal(KoreanPatch.Plugin.TranslateMissionMessage(item[1]), item[1], "second producer pass");
                }
            });
            Test("unknown messages, UI patterns, wrappers and layout remain unchanged", delegate {
                foreach (string value in new string[] { "Unknown mission K92 {0}\n<color=#FFFFFFFF>A-19</color>", "Buy UnknownAircraft", "Tutorial 99 - Unknown", " " + Pairs[0][0], Pairs[0][0] + "\n", "<b>" + Pairs[0][0] + "</b>", null, "" })
                {
                    MissionMessages producer = new MissionMessages();
                    producer.ShowMessage(value, false, null, false);
                    Equal(producer.Display[0], value, "exact allowlist boundary");
                }
            });
            Test("all protected identities stay unchanged in both paths", delegate {
                foreach (string identity in new string[] { "Continue", "IR Flares", "Radar Countermeasures", "M12 Jackknife" })
                {
                    Equal(KoreanPatch.Plugin.Translate(identity), identity, "existing dictionary identity");
                    Equal(KoreanPatch.Plugin.TranslateMissionMessage(identity), identity, "producer identity");
                }
            });
            Test("chat, even a reviewed literal or joined-the-game phrase, is not intercepted", delegate {
                MissionMessages producer = new MissionMessages();
                foreach (string value in new string[] { Pairs[0][0], "Player joined the game", "Pilot: " + Pairs[5][0] })
                {
                    producer.Chat(value);
                    Equal(producer.Display[producer.Display.Count - 1], value, "chat untouched by producer hook");
                }
            });
            Test("deferred join notice keeps exact dynamic name and color bytes", delegate {
                MissionMessages producer = new MissionMessages();
                producer.Join("[TAG] Continue <b>K92</b>", "12Ab34Cd");
                Equal(producer.Display[0], "<color=#12Ab34Cd>[TAG] Continue <b>K92</b> joined the game</color>", "join not rewritten");
            });
            Test("independent mission translations survive composition with an English notice", delegate {
                MissionMessages producer = new MissionMessages();
                producer.ShowMessage(Pairs[0][0], false, null, false);
                producer.ShowMessage(Pairs[5][0], false, null, false);
                producer.Join("Pilot", "FFFFFFFF");
                string expected = Pairs[0][1] + "\n" + Pairs[5][1] + "\n<color=#FFFFFFFF>Pilot joined the game</color>";
                Equal(producer.Feed(), expected, "before-feed composition");
                Equal(KoreanPatch.Plugin.Translate(producer.Feed()), expected, "existing whole-feed pass");
            });
            Test("host/client local copies leave network payload and routing arguments English/intact", delegate {
                FactionHQ faction = new FactionHQ();
                MissionMessages host = new MissionMessages { IsServer = true, LocalFaction = faction };
                host.ShowMessage(Pairs[5][0], true, faction, true);
                host.ReceiveRpc(host.NetworkPayload, host.NetworkSound, host.NetworkFaction);
                Equal(host.Display.Count, 1, "host RPC guard avoids second display");
                Equal(host.Sounds, 1, "sound intact");
                Equal(host.NetworkPayload, Pairs[5][0], "payload not localized");
                Equal(host.NetworkFaction, faction, "faction identity intact");
                MissionMessages client = new MissionMessages { LocalFaction = faction };
                client.ReceiveRpc(host.NetworkPayload, host.NetworkSound, host.NetworkFaction);
                Equal(client.Display[0], Pairs[5][1], "client local translation");
                KoreanPatch.Plugin.Enabled = false;
                MissionMessages englishClient = new MissionMessages { LocalFaction = faction };
                englishClient.ReceiveRpc(host.NetworkPayload, false, faction);
                Equal(englishClient.Display[0], Pairs[5][0], "other client's own language policy");
                KoreanPatch.Plugin.Enabled = true;
            });
            Test("faction rejection and sound selection remain intact", delegate {
                MissionMessages producer = new MissionMessages();
                producer.ShowMessage(Pairs[0][0], true, new FactionHQ(), false);
                Equal(producer.Display.Count, 0, "faction filter");
                Equal(producer.Sounds, 0, "filtered sound");
            });
            Test("mission source and functional key remain unchanged even when spelling matches", delegate {
                Outcome outcome = new Outcome { Message = Pairs[0][0], UniqueName = Pairs[0][0] };
                MissionMessages producer = new MissionMessages();
                outcome.Complete(producer);
                Equal(outcome.UniqueName, Pairs[0][0], "functional identifier");
                Equal(outcome.Message, Pairs[0][0], "stored source");
                Equal(producer.Display[0], Pairs[0][1], "display only");
            });
            Test("disabled, uninitialized and missing-dictionary paths fail open", delegate {
                KoreanPatch.Plugin.Enabled = false;
                Equal(KoreanPatch.Plugin.TranslateMissionMessage(Pairs[0][0]), Pairs[0][0], "disabled");
                KoreanPatch.Plugin.Enabled = true;
                KoreanPatch.Plugin saved = KoreanPatch.Plugin.Instance;
                KoreanPatch.Plugin.Instance = null;
                Equal(KoreanPatch.Plugin.TranslateMissionMessage(Pairs[0][0]), Pairs[0][0], "uninitialized");
                KoreanPatch.Plugin.Instance = saved;
                KoreanPatch.Plugin.TranslationKeys.Remove(Pairs[0][0]);
                Equal(KoreanPatch.Plugin.TranslateMissionMessage(Pairs[0][0]), Pairs[0][0], "missing source");
                KoreanPatch.Plugin.TranslationKeys.Add(Pairs[0][0]);
            });
            Console.WriteLine("Runtime Harmony fixtures: " + passed + " passed; no live game executed.");
            return 0;
        }
        finally { KoreanPatch.Plugin.HarmonyInstance.UnpatchSelf(); }
    }
}

internal static class Program
{
    public static int Main(string[] args)
    {
        try
        {
            if (args.Length != 2) throw new ArgumentException("Harmony path and ru.json path required");
            // Resolve the existing dependency in place; no game/third-party DLL is copied.
            AppDomain.CurrentDomain.AssemblyResolve += delegate(object sender, ResolveEventArgs e) {
                if (new AssemblyName(e.Name).Name == "0Harmony") return Assembly.LoadFrom(args[0]);
                return null;
            };
            return RuntimeTests.Run(args[1]);
        }
        catch (Exception e) { Console.Error.WriteLine(e); return 1; }
    }
}
