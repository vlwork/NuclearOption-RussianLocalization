using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System;
using System.IO;
using System.Collections.Generic;
using System.Reflection;
using System.Runtime.InteropServices;
using BepInEx.Configuration;
using UnityEngine.TextCore;
using UnityEngine.TextCore.LowLevel;

namespace KoreanPatch
{
    [BepInPlugin("com.noms.localizationpatch", "Localization Patch", "3.5.0")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log;
        internal static Plugin Instance;
        internal static Harmony HarmonyInstance;

        // Language config
        private ConfigEntry<string> languageConfig;
        internal static string CurrentLanguage = "ko";

        // Translation data
        internal static Dictionary<string, string> Translations = new Dictionary<string, string>();
        internal static HashSet<string> TranslationKeys = new HashSet<string>();
        internal static bool FontReady = false;
        internal static bool Enabled = true;

        // Korean font
        internal static TMP_FontAsset KoreanFontAsset;
        private static HashSet<int> patchedFonts = new HashSet<int>();

        // FontEngine redirect: proxy Font → file path loading
        internal static Font koreanProxyFont;
        internal static string koreanFontFilePath;

        // Recursion guard
        /// <summary>Set only while we assign text ourselves, so the setter hooks skip our own writes.</summary>
        internal static bool isPatching = false;

        /// <summary>Guards the periodic sweep against overlapping itself.</summary>
        private bool scanning = false;

        // Config
        private string translationFilePath;
        private bool showUI = false;
        private Rect windowRect = new Rect(20, 100, 380, 300);
        private int translatedCount = 0;
        private int missedCount = 0;
        private HashSet<string> untranslatedStrings = new HashSet<string>();

        // Styles
        private GUIStyle boxStyle, labelStyle, headerStyle, buttonStyle;
        private bool stylesInit = false;

        // Font status for UI
        private string fontStatusText = "Initializing...";

        // Periodic font scan
        private float lastFontScanTime = 0f;
        private const float FONT_SCAN_INTERVAL = 5f;
        private int totalFontsPatched = 0;

        // Helper MonoBehaviour — bypasses BepInEx lifecycle issues
        private static FrameHelper frameHelper;

        // Scene text scan — translates prefab/inspector text that bypasses setter patches
        private float lastTextScanTime = 0f;
        private float lastAutoExportTime = 0f;
        private int lastExportedCount = 0;
        private static float textScanInterval = 0.3f;
        private int lastSceneIndex = -1;
        private HashSet<int> translatedInstances = new HashSet<int>();

        private void Awake()
        {
            Log = Logger;
            Instance = this;

            // Language config
            languageConfig = Config.Bind("General", "Language", "auto",
                "Language code: auto (auto-detect from .json files), or specify manually (ko, de, ru, es, fr, tr, ja, zh, etc.)");
            CurrentLanguage = languageConfig.Value.ToLower().Trim();

            textScanInterval = Config.Bind("General", "ScanInterval", 0.3f,
                "Seconds between full scene text scans. Lower = untranslated text is caught sooner, " +
                "at the cost of more CPU. Text is also translated the moment its component is enabled, " +
                "so this mainly catches text that changes while already on screen.").Value;

            string pluginDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);

            // Auto-detect: find any 2-3 letter language .json file in the plugin folder
            if (CurrentLanguage == "auto")
            {
                CurrentLanguage = "ko"; // fallback
                // First check well-known languages in priority order
                foreach (string lang in new[] { "ko", "de", "ru", "es", "fr", "tr", "ja", "zh", "pt", "it", "pl", "nl", "ar", "th", "vi" })
                {
                    if (File.Exists(Path.Combine(pluginDir, $"{lang}.json")))
                    {
                        CurrentLanguage = lang;
                        break;
                    }
                }
                // If none found, scan for any 2-3 letter .json file
                if (!File.Exists(Path.Combine(pluginDir, $"{CurrentLanguage}.json")))
                {
                    foreach (string file in Directory.GetFiles(pluginDir, "*.json"))
                    {
                        string name = Path.GetFileNameWithoutExtension(file);
                        if (name.Length >= 2 && name.Length <= 3 && name != "en_template")
                        {
                            CurrentLanguage = name;
                            break;
                        }
                    }
                }
                Log.LogInfo($"Auto-detected language: {CurrentLanguage}");
            }

            translationFilePath = Path.Combine(pluginDir, $"{CurrentLanguage}.json");

            LoadTranslations();

            // IMPORTANT: Apply Harmony patches BEFORE font setup
            // This ensures FontEngine.LoadFontFace redirect is active when CreateFontAsset runs
            HarmonyInstance = new Harmony("com.noms.localizationpatch");
            ApplyHarmonyPatches();

            // Set up special font if translations contain non-Latin characters
            // (Korean, Cyrillic, CJK, Thai, Arabic, etc.)
            if (NeedsCustomFont())
            {
                SetupKoreanFont();

                // Initial scan: patch all currently loaded TMP fonts
                if (FontReady) PatchAllLoadedFonts();
            }

            // Create a standalone helper GameObject for Update() — BepInEx's MonoBehaviour lifecycle
            // is broken on some systems (Update/coroutines never fire). A separate GO bypasses this.
            try
            {
                var helperGo = new GameObject("LocalizationPatch_FrameHelper");
                UnityEngine.Object.DontDestroyOnLoad(helperGo);
                helperGo.hideFlags = HideFlags.HideAndDontSave;
                frameHelper = helperGo.AddComponent<FrameHelper>();
                Log.LogInfo("FrameHelper created on standalone GameObject");
            }
            catch (Exception e)
            {
                Log.LogWarning($"FrameHelper creation failed: {e.Message} — falling back to plugin Update()");
            }

            // Also register scene load callback as additional safety net
            UnityEngine.SceneManagement.SceneManager.sceneLoaded += OnSceneLoaded;

            Log.LogInfo($"Localization Patch v3.5.0 loaded — lang={CurrentLanguage}, {Translations.Count} translations, Font: {fontStatusText}");
        }

        /// <summary>
        /// Apply Harmony patches individually with try-catch for each.
        /// PatchAll() fails if ANY patch target doesn't exist, so we apply manually.
        /// </summary>
        private void ApplyHarmonyPatches()
        {
            int applied = 0;

            // FontEngine redirect — CRITICAL for font creation
            try
            {
                var targetMethod = typeof(FontEngine).GetMethod("LoadFontFace",
                    BindingFlags.Static | BindingFlags.Public,
                    null, new Type[] { typeof(Font), typeof(int) }, null);

                if (targetMethod != null)
                {
                    var prefix = typeof(FontEngine_LoadFontFace_Redirect).GetMethod("Prefix",
                        BindingFlags.Static | BindingFlags.NonPublic);
                    HarmonyInstance.Patch(targetMethod, prefix: new HarmonyMethod(prefix));
                    applied++;
                    Log.LogInfo("Patched: FontEngine.LoadFontFace(Font, int) redirect");
                }
                else
                {
                    Log.LogWarning("FontEngine.LoadFontFace(Font, int) not found — redirect unavailable");
                }
            }
            catch (Exception e) { Log.LogWarning($"FontEngine patch failed: {e.Message}"); }

            // TMP_Text.text setter
            try
            {
                var targetMethod = typeof(TMP_Text).GetProperty("text")?.GetSetMethod();
                if (targetMethod != null)
                {
                    var prefix = typeof(TMP_Text_SetText_Patch).GetMethod("Prefix",
                        BindingFlags.Static | BindingFlags.NonPublic);
                    HarmonyInstance.Patch(targetMethod, prefix: new HarmonyMethod(prefix));
                    applied++;
                    Log.LogInfo("Patched: TMP_Text.text setter");
                }
            }
            catch (Exception e) { Log.LogWarning($"TMP_Text.text patch failed: {e.Message}"); }

            // Text.text setter (legacy UI)
            try
            {
                var targetMethod = typeof(Text).GetProperty("text")?.GetSetMethod();
                if (targetMethod != null)
                {
                    var prefix = typeof(UIText_SetText_Patch).GetMethod("Prefix",
                        BindingFlags.Static | BindingFlags.NonPublic);
                    HarmonyInstance.Patch(targetMethod, prefix: new HarmonyMethod(prefix));
                    applied++;
                    Log.LogInfo("Patched: Text.text setter");
                }
            }
            catch (Exception e) { Log.LogWarning($"Text.text patch failed: {e.Message}"); }

            // TMP_Text.SetText(string) — may not exist in this TMP version
            try
            {
                var targetMethod = typeof(TMP_Text).GetMethod("SetText",
                    BindingFlags.Instance | BindingFlags.Public,
                    null, new Type[] { typeof(string) }, null);

                if (targetMethod != null)
                {
                    var prefix = typeof(TMP_Text_SetTextMethod_Patch).GetMethod("Prefix",
                        BindingFlags.Static | BindingFlags.NonPublic);
                    HarmonyInstance.Patch(targetMethod, prefix: new HarmonyMethod(prefix));
                    applied++;
                    Log.LogInfo("Patched: TMP_Text.SetText(string)");
                }
                else
                {
                    Log.LogInfo("TMP_Text.SetText(string) not found — skipping (this is OK)");
                }
            }
            catch (Exception e) { Log.LogWarning($"TMP_Text.SetText patch failed: {e.Message}"); }

            // OnEnable on the concrete TMP components. Most UI text is authored in prefabs and
            // never goes through a setter at runtime, so without this it stays English until the
            // next sweep — visible as a flash of English whenever a panel opens.
            foreach (var tmpType in new[] { typeof(TextMeshProUGUI), typeof(TextMeshPro) })
            {
                try
                {
                    var targetMethod = tmpType.GetMethod("OnEnable",
                        BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);

                    if (targetMethod != null)
                    {
                        var postfix = typeof(TMP_OnEnable_Patch).GetMethod("Postfix",
                            BindingFlags.Static | BindingFlags.NonPublic);
                        HarmonyInstance.Patch(targetMethod, postfix: new HarmonyMethod(postfix));
                        applied++;
                        Log.LogInfo($"Patched: {tmpType.Name}.OnEnable — instant translation on show");
                    }
                    else
                    {
                        Log.LogInfo($"{tmpType.Name}.OnEnable not found — skipping");
                    }
                }
                catch (Exception e) { Log.LogWarning($"{tmpType.Name}.OnEnable patch failed: {e.Message}"); }
            }

            Log.LogInfo($"Harmony: {applied} patches applied successfully");
        }

        private void OnDestroy()
        {
            HarmonyInstance?.UnpatchSelf();
            if (loadedFontPath != null)
                RemoveFontResourceEx(loadedFontPath, FR_PRIVATE, IntPtr.Zero);
        }

        /// <summary>
        /// Called by FrameHelper.Update() every frame — runs on a standalone GameObject
        /// that bypasses BepInEx's broken MonoBehaviour lifecycle.
        /// </summary>
        internal void DoPerFrameLogic()
        {
            // Primary: F10 (may conflict with Windows/game); Alt: F9
            if (Input.GetKeyDown(KeyCode.F10) || Input.GetKeyDown(KeyCode.F9))
            {
                showUI = !showUI;
                Log.LogInfo($"UI toggle: {showUI}");
            }

            if (Input.GetKey(KeyCode.LeftControl) && Input.GetKeyDown(KeyCode.F10))
            {
                LoadTranslations();
                translatedInstances.Clear();
                Log.LogInfo($"Translations reloaded: {Translations.Count} entries");
            }

            // Ctrl+F11 = Extract game data (tips, encyclopedia descriptions)
            if (Input.GetKey(KeyCode.LeftControl) && Input.GetKeyDown(KeyCode.F11))
            {
                ExtractGameData();
            }

            // Auto-export untranslated strings every 30 seconds
            if (Time.time - lastAutoExportTime > 30f)
            {
                lastAutoExportTime = Time.time;
                Log.LogInfo($"[AutoExport] translated={translatedCount}, missed={missedCount}, untranslated={untranslatedStrings.Count}");
                if (untranslatedStrings.Count > lastExportedCount)
                {
                    ExportUntranslated();
                    lastExportedCount = untranslatedStrings.Count;
                }
            }

            // Periodically scan for new TMP fonts and add Korean fallback
            if (FontReady && Time.time - lastFontScanTime > FONT_SCAN_INTERVAL)
            {
                lastFontScanTime = Time.time;
                PatchAllLoadedFonts();
            }

            // Scene text scan — translate prefab text that was set via Unity Inspector
            if (Enabled && Time.time - lastTextScanTime > textScanInterval)
            {
                lastTextScanTime = Time.time;

                // Reset cache on scene change
                int currentScene = UnityEngine.SceneManagement.SceneManager.GetActiveScene().buildIndex;
                if (currentScene != lastSceneIndex)
                {
                    lastSceneIndex = currentScene;
                    translatedInstances.Clear();
                    Log.LogInfo($"Scene changed to index {currentScene}, resetting text scan cache");
                }

                ScanAndTranslateAllText();
            }
        }

        private void OnSceneLoaded(UnityEngine.SceneManagement.Scene scene, UnityEngine.SceneManagement.LoadSceneMode mode)
        {
            Log.LogInfo($"Scene loaded: {scene.name} (index {scene.buildIndex})");
            translatedInstances.Clear();
            lastSceneIndex = scene.buildIndex;
            lastTextScanTime = -999f;
        }

        #region Translation Loading

        private void LoadTranslations()
        {
            Translations.Clear();
            TranslationKeys.Clear();

            if (!File.Exists(translationFilePath))
            {
                Log.LogWarning($"Translation file not found: {translationFilePath}");
                return;
            }

            try
            {
                string json = File.ReadAllText(translationFilePath, System.Text.Encoding.UTF8);
                ParseSimpleJson(json);
                foreach (var key in Translations.Keys)
                    TranslationKeys.Add(key);
                Log.LogInfo($"Loaded {Translations.Count} translations from {CurrentLanguage}.json");
            }
            catch (Exception e)
            {
                Log.LogError($"Failed to load translations: {e.Message}");
            }
        }

        private void ParseSimpleJson(string json)
        {
            var lines = json.Split('\n');
            var cleanLines = new List<string>();
            foreach (var line in lines)
            {
                string trimmed = line.TrimStart();
                if (!trimmed.StartsWith("//"))
                    cleanLines.Add(line);
            }
            json = string.Join("\n", cleanLines);

            int i = 0;
            while (i < json.Length && json[i] != '{') i++;
            i++;

            while (i < json.Length)
            {
                while (i < json.Length && char.IsWhiteSpace(json[i])) i++;
                if (i >= json.Length || json[i] == '}') break;

                string key = ReadJsonString(json, ref i);
                if (key == null) break;

                while (i < json.Length && json[i] != ':') i++;
                i++;

                string value = ReadJsonString(json, ref i);
                if (value == null) break;

                if (!string.IsNullOrEmpty(key) && value != null)
                    Translations[key] = value;

                while (i < json.Length && (char.IsWhiteSpace(json[i]) || json[i] == ',')) i++;
            }
        }

        private string ReadJsonString(string json, ref int i)
        {
            while (i < json.Length && json[i] != '"') i++;
            if (i >= json.Length) return null;
            i++;

            var sb = new System.Text.StringBuilder();
            while (i < json.Length && json[i] != '"')
            {
                if (json[i] == '\\' && i + 1 < json.Length)
                {
                    i++;
                    switch (json[i])
                    {
                        case 'n': sb.Append('\n'); break;
                        case 't': sb.Append('\t'); break;
                        case '"': sb.Append('"'); break;
                        case '\\': sb.Append('\\'); break;
                        case 'u':
                            if (i + 4 < json.Length)
                            {
                                string hex = json.Substring(i + 1, 4);
                                sb.Append((char)Convert.ToInt32(hex, 16));
                                i += 4;
                            }
                            break;
                        default: sb.Append(json[i]); break;
                    }
                }
                else
                {
                    sb.Append(json[i]);
                }
                i++;
            }
            if (i < json.Length) i++;
            return sb.ToString();
        }

        #endregion

        /// <summary>
        /// Check if loaded translations contain characters that need a custom font.
        /// Latin-script languages (German, Spanish, French, etc.) don't need font replacement.
        /// </summary>
        private bool NeedsCustomFont()
        {
            foreach (var value in Translations.Values)
            {
                foreach (char c in value)
                {
                    if (c >= 0xAC00 && c <= 0xD7AF) return true; // Korean Hangul syllables
                    if (c >= 0x3131 && c <= 0x318E) return true; // Hangul compatibility jamo
                    if (c >= 0x0400 && c <= 0x04FF) return true; // Cyrillic
                    if (c >= 0x4E00 && c <= 0x9FFF) return true; // CJK Unified
                    if (c >= 0x3040 && c <= 0x30FF) return true; // Japanese Hiragana/Katakana
                    if (c >= 0x0E00 && c <= 0x0E7F) return true; // Thai
                    if (c >= 0x0600 && c <= 0x06FF) return true; // Arabic
                }
            }
            Log.LogInfo("Translations use Latin script only — skipping custom font setup");
            return false;
        }

        #region Korean Font

        [DllImport("gdi32.dll")]
        private static extern int AddFontResourceEx(string lpszFilename, uint fl, IntPtr pdv);

        [DllImport("gdi32.dll")]
        private static extern int RemoveFontResourceEx(string lpszFilename, uint fl, IntPtr pdv);

        private const uint FR_PRIVATE = 0x10;

        private string loadedFontPath = null;

        /// <summary>
        /// Find the font file to use. Scans plugin folder for any .ttf/.otf file.
        /// Users just drop their font file in — no renaming needed.
        /// </summary>
        private string FindFontFile(string pluginDir)
        {
            string found = null;
            foreach (string file in Directory.GetFiles(pluginDir))
            {
                string ext = Path.GetExtension(file).ToLower();
                if (ext == ".ttf" || ext == ".otf")
                {
                    if (found == null || string.Compare(Path.GetFileName(file), Path.GetFileName(found), StringComparison.OrdinalIgnoreCase) < 0)
                        found = file;
                }
            }
            if (found != null)
                Log.LogInfo($"Using font: {Path.GetFileName(found)}");
            return found;
        }

        private void SetupKoreanFont()
        {
            try
            {
                string pluginDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                string fontPath = FindFontFile(pluginDir);

                Log.LogInfo($"Unity version: {Application.unityVersion}");

                // === Step 1: Diagnostics - test FontEngine ===
                var feInit = FontEngine.InitializeFontEngine();
                Log.LogInfo($"FontEngine.InitializeFontEngine: {feInit}");

                // === Step 2: Try loading font from file via FontEngine directly ===
                if (fontPath != null && File.Exists(fontPath))
                {
                    // Register with Windows
                    int regResult = AddFontResourceEx(fontPath, FR_PRIVATE, IntPtr.Zero);
                    Log.LogInfo($"AddFontResourceEx: result={regResult}");
                    loadedFontPath = fontPath;

                    // Test direct file loading
                    var fileLoadResult = FontEngine.LoadFontFace(fontPath, 36);
                    Log.LogInfo($"FontEngine.LoadFontFace(filePath): {fileLoadResult}");

                    if (fileLoadResult == FontEngineError.Success)
                    {
                        var faceInfo = FontEngine.GetFaceInfo();
                        Log.LogInfo($"Font face loaded: {faceInfo.familyName} {faceInfo.styleName}, {faceInfo.pointSize}pt");

                        // Create proxy using actual registered font name (not Arial)
                        // AddFontResourceEx registered the font with Windows, so CreateDynamicFontFromOSFont
                        // can find it by family name. This ensures TMP dynamic glyph population
                        // uses correct metrics without needing the redirect hack.
                        koreanFontFilePath = fontPath;
                        string fontFamily = faceInfo.familyName;
                        koreanProxyFont = Font.CreateDynamicFontFromOSFont(fontFamily, 36);
                        if (koreanProxyFont == null)
                        {
                            Log.LogWarning($"CreateDynamicFontFromOSFont(\"{fontFamily}\") failed, falling back to Arial proxy");
                            koreanProxyFont = Font.CreateDynamicFontFromOSFont("Arial", 24);
                        }
                        else
                        {
                            Log.LogInfo($"Created OS font from registered name: {fontFamily}");
                        }

                        // Try CreateFontAsset first (uses real font if proxy matched)
                        KoreanFontAsset = TMP_FontAsset.CreateFontAsset(
                            koreanProxyFont, 36, 4,
                            GlyphRenderMode.SDFAA,
                            4096, 4096);

                        if (KoreanFontAsset != null)
                        {
                            // Ensure faceInfo is from the actual font file
                            FontEngine.LoadFontFace(fontPath, 36);
                            KoreanFontAsset.faceInfo = FontEngine.GetFaceInfo();
                            Log.LogInfo("CreateFontAsset succeeded with registered font!");
                        }
                        else
                        {
                            Log.LogWarning("CreateFontAsset returned null, trying manual creation...");
                            KoreanFontAsset = TryManualFontCreation(fontPath);
                        }
                    }
                    else
                    {
                        // File loading failed — try byte array then manual creation
                        Log.LogWarning("File path loading failed, trying byte array...");
                        byte[] fontData = File.ReadAllBytes(fontPath);
                        var byteLoadResult = FontEngine.LoadFontFace(fontData, 36);
                        Log.LogInfo($"FontEngine.LoadFontFace(bytes): {byteLoadResult}");

                        if (byteLoadResult == FontEngineError.Success)
                        {
                            var faceInfo2 = FontEngine.GetFaceInfo();
                            koreanFontFilePath = fontPath;
                            koreanProxyFont = Font.CreateDynamicFontFromOSFont(faceInfo2.familyName, 36)
                                           ?? Font.CreateDynamicFontFromOSFont("Arial", 24);
                            KoreanFontAsset = TryManualFontCreation(fontPath);
                        }
                    }
                }
                else
                {
                    Log.LogError($"No font file found in plugin folder. Place font.ttf/font.otf or Pretendard-Regular.otf in: {pluginDir}");
                }

                // === Step 4: Fallback — find existing Korean-capable font in game ===
                if (KoreanFontAsset == null)
                {
                    Log.LogInfo("Searching for existing Korean-capable font in game...");
                    KoreanFontAsset = FindExistingKoreanFont();
                }

                // === Result ===
                if (KoreanFontAsset != null)
                {
                    string fontFileName = Path.GetFileNameWithoutExtension(fontPath);
                    KoreanFontAsset.name = $"LocalizationPatch_{fontFileName}";
                    KoreanFontAsset.atlasPopulationMode = AtlasPopulationMode.Dynamic;
                    UnityEngine.Object.DontDestroyOnLoad(KoreanFontAsset);

                    // Pre-populate characters from translations
                    PrePopulateFromTranslations();

                    // Add to TMP global fallback
                    AddToGlobalFallback();

                    FontReady = true;
                    fontStatusText = $"Ready ({fontFileName})";
                    Log.LogInfo($"Custom TMP font ready ({fontFileName})! Atlas: {KoreanFontAsset.atlasTexture?.width}x{KoreanFontAsset.atlasTexture?.height}");
                }
                else
                {
                    Log.LogError("All font creation methods failed!");
                    fontStatusText = "Font creation failed";
                    LogDiagnostics();
                }
            }
            catch (Exception e)
            {
                Log.LogError($"Font setup error: {e}");
                fontStatusText = $"Error: {e.Message}";
            }
        }

        /// <summary>
        /// Manually create a TMP_FontAsset when CreateFontAsset returns null.
        /// Uses FontEngine file loading + ScriptableObject.CreateInstance.
        /// </summary>
        private TMP_FontAsset TryManualFontCreation(string fontPath)
        {
            try
            {
                // Ensure font face is loaded from file
                FontEngine.InitializeFontEngine();
                var loadResult = FontEngine.LoadFontFace(fontPath, 36);
                if (loadResult != FontEngineError.Success)
                {
                    Log.LogWarning($"Manual creation: FontEngine.LoadFontFace failed: {loadResult}");
                    return null;
                }

                var faceInfo = FontEngine.GetFaceInfo();
                Log.LogInfo($"Manual creation: face={faceInfo.familyName}, pointSize={faceInfo.pointSize}");

                // Create font asset instance
                var fontAsset = ScriptableObject.CreateInstance<TMP_FontAsset>();

                // Set face info (public setter)
                fontAsset.faceInfo = faceInfo;

                // Set source font file via reflection (internal setter)
                SetFieldValue(fontAsset, "m_SourceFontFile", koreanProxyFont);

                // Set atlas properties via reflection (internal setters)
                SetFieldValue(fontAsset, "m_AtlasWidth", 4096);
                SetFieldValue(fontAsset, "m_AtlasHeight", 4096);
                SetFieldValue(fontAsset, "m_AtlasPadding", 4);
                SetFieldValue(fontAsset, "m_AtlasRenderMode", GlyphRenderMode.SDFAA);

                // Atlas population mode (public setter)
                fontAsset.atlasPopulationMode = AtlasPopulationMode.Dynamic;

                // Create atlas texture
                var atlas = new Texture2D(4096, 4096, TextureFormat.Alpha8, false);
                atlas.name = "KoreanPatch_Atlas";
                fontAsset.atlasTextures = new Texture2D[] { atlas };

                // Find SDF shader from existing game fonts
                Shader sdfShader = FindGameSdfShader();
                if (sdfShader == null)
                {
                    sdfShader = Shader.Find("TextMeshPro/Distance Field");
                    if (sdfShader == null)
                        sdfShader = Shader.Find("TextMeshPro/Mobile/Distance Field");
                }

                if (sdfShader != null)
                {
                    var material = new Material(sdfShader);
                    material.name = "KoreanPatch_Material";
                    material.SetTexture(ShaderUtilities.ID_MainTex, atlas);
                    fontAsset.material = material;
                    Log.LogInfo($"Manual creation: shader={sdfShader.name}");
                }
                else
                {
                    Log.LogWarning("Manual creation: no SDF shader found!");
                    return null;
                }

                // Initialize glyph and character tables via reflection
                SetFieldValue(fontAsset, "m_GlyphTable", new List<Glyph>());
                SetFieldValue(fontAsset, "m_CharacterTable", new List<TMP_Character>());

                // Initialize free/used glyph rects
                SetFieldValue(fontAsset, "m_FreeGlyphRects", new List<GlyphRect>
                {
                    new GlyphRect(0, 0, 4096 - 4, 4096 - 4) // Full atlas minus padding
                });
                SetFieldValue(fontAsset, "m_UsedGlyphRects", new List<GlyphRect>());

                // Set atlas texture index
                SetFieldValue(fontAsset, "m_AtlasTextureIndex", 0);

                // Initialize internal dictionaries by calling ReadFontAssetDefinition
                try
                {
                    var readDef = typeof(TMP_FontAsset).GetMethod("ReadFontAssetDefinition",
                        BindingFlags.Public | BindingFlags.Instance);
                    readDef?.Invoke(fontAsset, null);
                    Log.LogInfo("Manual creation: ReadFontAssetDefinition called");
                }
                catch (Exception re)
                {
                    Log.LogWarning($"ReadFontAssetDefinition failed: {re.Message}");
                }

                Log.LogInfo("Manual TMP_FontAsset created successfully");
                return fontAsset;
            }
            catch (Exception e)
            {
                Log.LogError($"Manual font creation failed: {e}");
                return null;
            }
        }

        /// <summary>
        /// Find an existing TMP font in the game that can render Korean.
        /// </summary>
        private TMP_FontAsset FindExistingKoreanFont()
        {
            try
            {
                var allFonts = Resources.FindObjectsOfTypeAll<TMP_FontAsset>();
                Log.LogInfo($"Scanning {allFonts.Length} TMP fonts for Korean support...");

                foreach (var font in allFonts)
                {
                    if (font == null) continue;

                    // Check if font has Korean characters
                    if (font.HasCharacter('가'))
                    {
                        Log.LogInfo($"  Found Korean-capable font: {font.name}");
                        return font;
                    }

                    // Check fallback fonts
                    if (font.fallbackFontAssetTable != null)
                    {
                        foreach (var fb in font.fallbackFontAssetTable)
                        {
                            if (fb != null && fb.HasCharacter('가'))
                            {
                                Log.LogInfo($"  Found Korean-capable fallback font: {fb.name} (from {font.name})");
                                return fb;
                            }
                        }
                    }
                }

                // Try dynamic population on existing fonts
                foreach (var font in allFonts)
                {
                    if (font == null || font.atlasPopulationMode != AtlasPopulationMode.Dynamic) continue;
                    try
                    {
                        if (font.TryAddCharacters("가"))
                        {
                            Log.LogInfo($"  Font '{font.name}' can dynamically add Korean!");
                            return font;
                        }
                    }
                    catch { }
                }

                Log.LogWarning("No existing Korean-capable font found in game");
            }
            catch (Exception e)
            {
                Log.LogWarning($"Korean font search failed: {e.Message}");
            }
            return null;
        }

        private Shader FindGameSdfShader()
        {
            var allFonts = Resources.FindObjectsOfTypeAll<TMP_FontAsset>();
            foreach (var font in allFonts)
            {
                if (font?.material?.shader != null)
                    return font.material.shader;
            }
            return null;
        }

        /// <summary>
        /// Extract all unique Korean characters from translations and pre-populate the atlas.
        /// </summary>
        private void PrePopulateFromTranslations()
        {
            if (KoreanFontAsset == null) return;
            try
            {
                var koreanChars = new HashSet<char>();
                foreach (var value in Translations.Values)
                {
                    foreach (char c in value)
                    {
                        if (c >= 0xAC00 && c <= 0xD7AF) koreanChars.Add(c); // Hangul syllables
                        else if (c >= 0x3131 && c <= 0x318E) koreanChars.Add(c); // Hangul jamo
                        else if (c >= 0x0400 && c <= 0x04FF) koreanChars.Add(c); // Cyrillic
                        else if (c >= 0x4E00 && c <= 0x9FFF) koreanChars.Add(c); // CJK
                        else if (c >= 0x3040 && c <= 0x30FF) koreanChars.Add(c); // Japanese
                        else if (c >= 0x0E00 && c <= 0x0E7F) koreanChars.Add(c); // Thai
                        else if (c >= 0x0600 && c <= 0x06FF) koreanChars.Add(c); // Arabic
                    }
                }

                if (koreanChars.Count == 0) return;

                string allKorean = new string(new List<char>(koreanChars).ToArray());
                Log.LogInfo($"Pre-populating {allKorean.Length} unique Korean chars from translations...");

                if (KoreanFontAsset.TryAddCharacters(allKorean, out string missing))
                {
                    Log.LogInfo($"Pre-populated ALL {allKorean.Length} Korean glyphs successfully!");
                }
                else
                {
                    int loaded = allKorean.Length - (missing?.Length ?? 0);
                    Log.LogInfo($"Pre-populated {loaded}/{allKorean.Length} glyphs ({missing?.Length ?? 0} missing)");
                }
            }
            catch (Exception e)
            {
                Log.LogWarning($"Glyph pre-population failed: {e.Message}");
            }
        }

        private void AddToGlobalFallback()
        {
            try
            {
                var fallbackProp = typeof(TMP_Settings).GetProperty("fallbackFontAssets",
                    BindingFlags.Public | BindingFlags.Static);
                if (fallbackProp != null)
                {
                    var list = fallbackProp.GetValue(null) as List<TMP_FontAsset>;
                    if (list != null && !list.Contains(KoreanFontAsset))
                    {
                        list.Add(KoreanFontAsset);
                        Log.LogInfo("Added Korean font to TMP global fallback list");
                    }
                }
            }
            catch (Exception e)
            {
                Log.LogWarning($"Could not set global fallback: {e.Message}");
            }
        }

        internal static void PatchAllLoadedFonts()
        {
            if (!FontReady || KoreanFontAsset == null) return;

            try
            {
                var allFonts = Resources.FindObjectsOfTypeAll<TMP_FontAsset>();
                int newlyPatched = 0;

                foreach (var font in allFonts)
                {
                    if (font == null || font == KoreanFontAsset) continue;

                    int fontId = font.GetInstanceID();
                    if (patchedFonts.Contains(fontId)) continue;

                    try
                    {
                        var fallbackList = font.fallbackFontAssetTable;
                        if (fallbackList == null)
                        {
                            fallbackList = new List<TMP_FontAsset>();
                            font.fallbackFontAssetTable = fallbackList;
                        }

                        if (!fallbackList.Contains(KoreanFontAsset))
                        {
                            fallbackList.Add(KoreanFontAsset);
                            newlyPatched++;
                        }
                        patchedFonts.Add(fontId);
                    }
                    catch { }
                }

                if (newlyPatched > 0)
                {
                    Instance.totalFontsPatched += newlyPatched;
                    Log.LogInfo($"Patched {newlyPatched} new TMP fonts with Korean fallback (total: {Instance.totalFontsPatched})");
                }
            }
            catch (Exception e)
            {
                Log.LogWarning($"Font scan error: {e.Message}");
            }
        }

        internal static void EnsureKoreanFallback(TMP_Text textComponent)
        {
            if (!FontReady || KoreanFontAsset == null || textComponent == null) return;
            if (textComponent.font == null) return;

            int fontId = textComponent.font.GetInstanceID();
            if (patchedFonts.Contains(fontId)) return;

            try
            {
                var fallbackList = textComponent.font.fallbackFontAssetTable;
                if (fallbackList == null)
                {
                    fallbackList = new List<TMP_FontAsset>();
                    textComponent.font.fallbackFontAssetTable = fallbackList;
                }

                if (!fallbackList.Contains(KoreanFontAsset))
                {
                    fallbackList.Add(KoreanFontAsset);
                    patchedFonts.Add(fontId);
                }
                else
                {
                    patchedFonts.Add(fontId);
                }
            }
            catch { }
        }

        private void LogDiagnostics()
        {
            try
            {
                var allFonts = Resources.FindObjectsOfTypeAll<TMP_FontAsset>();
                Log.LogInfo($"=== Diagnostics ===");
                Log.LogInfo($"TMP fonts in game: {allFonts.Length}");
                foreach (var f in allFonts)
                {
                    if (f != null)
                        Log.LogInfo($"  - {f.name} (atlas: {f.atlasTexture?.width}x{f.atlasTexture?.height}, mode: {f.atlasPopulationMode}, chars: {f.characterTable?.Count ?? 0})");
                }

                string[] osFonts = Font.GetOSInstalledFontNames();
                Log.LogInfo($"OS fonts: {osFonts.Length}");
                // Look for Korean fonts specifically
                foreach (var fn in osFonts)
                {
                    string lower = fn.ToLower();
                    if (lower.Contains("malgun") || lower.Contains("gothic") || lower.Contains("nanum") ||
                        lower.Contains("gulim") || lower.Contains("batang") || lower.Contains("pretendard"))
                        Log.LogInfo($"  Korean font: {fn}");
                }
            }
            catch { }
        }

        // Helper: set private/internal field via reflection
        private static void SetFieldValue(object obj, string fieldName, object value)
        {
            var field = obj.GetType().GetField(fieldName,
                BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Public);
            if (field != null)
                field.SetValue(obj, value);
            else
                Log.LogWarning($"Field '{fieldName}' not found on {obj.GetType().Name}");
        }

        #endregion

        #region Translation Logic

        /// <summary>
        /// Scan ALL active TMP_Text and Text components and translate their current text.
        /// This catches text set via Unity Inspector/prefabs that bypasses our setter patches.
        /// </summary>
        /// <summary>
        /// Translate one TMP component in place.
        ///
        /// Called both by the periodic sweep and by the OnEnable hook — a panel that has just
        /// been shown gets translated in the same frame instead of flashing English until the
        /// next sweep comes around.
        /// </summary>
        internal void TranslateTmpComponent(TMP_Text tmp)
        {
            if (tmp == null || tmp.gameObject == null) return;

            string current = tmp.text;
            if (string.IsNullOrEmpty(current)) return;

            int id = tmp.GetInstanceID();
            string trimmed = current.Trim();

            // Skip if already translated and text hasn't been reset to English
            if (translatedInstances.Contains(id))
            {
                if (!TranslationKeys.Contains(trimmed) && TryPatternMatch(trimmed) == null)
                {
                    // Usually this is our own translated output being re-scanned. But panels
                    // that page through content (the encyclopedia) reuse the same component,
                    // so it can equally be a *new* English string we have no entry for.
                    // RecordUntranslated ignores anything non-ASCII, which separates the two.
                    RecordUntranslated(trimmed);
                    return;
                }
                // text was reset to English — remove from cache and re-translate below
                translatedInstances.Remove(id);
            }

            // Skip DialogueBox title — translating it breaks the Ok button
            if (IsDialogueBoxTitle(tmp)) return;

            string translated = TranslationKeys.Contains(trimmed)
                ? Translations[trimmed]
                : TryPatternMatch(trimmed);

            if (translated != null)
            {
                translatedInstances.Add(id);
                // Identity entries (designations kept in English) would otherwise reassign the
                // same string every sweep, forcing a needless TMP mesh rebuild.
                if (translated != current)
                {
                    isPatching = true;
                    try { tmp.text = translated; }
                    finally { isPatching = false; }
                }
                if (FontReady && ContainsKorean(translated))
                    EnsureKoreanFallback(tmp);
            }
            else
            {
                RecordUntranslated(trimmed);
            }
        }

        /// <summary>
        /// Periodic safety net for text the setter hooks never see (prefab-authored strings,
        /// or text swapped in by code paths we do not patch).
        ///
        /// This deliberately does NOT hold <see cref="isPatching"/> for its whole run. It used
        /// to, and that was the cause of visible flicker: the flag makes the setter hooks pass
        /// text through untranslated, so anything the game assigned during a sweep showed up in
        /// English and only got corrected on the next sweep. The flag is now held only around
        /// our own assignments, which is all the re-entrancy guard was ever needed for.
        /// </summary>
        private void ScanAndTranslateAllText()
        {
            if (scanning) return;
            scanning = true;
            try
            {
                // Scan TMP_Text components
                var tmpTexts = Resources.FindObjectsOfTypeAll<TMP_Text>();
                foreach (var tmp in tmpTexts)
                    TranslateTmpComponent(tmp);

                // Scan legacy Text components
                var uiTexts = Resources.FindObjectsOfTypeAll<Text>();
                foreach (var txt in uiTexts)
                {
                    if (txt == null || txt.gameObject == null) continue;
                    int id = txt.GetInstanceID();

                    string current = txt.text;
                    if (string.IsNullOrEmpty(current)) continue;

                    string trimmed = current.Trim();

                    if (translatedInstances.Contains(id))
                    {
                        if (!TranslationKeys.Contains(trimmed) && TryPatternMatch(trimmed) == null)
                            continue;
                        translatedInstances.Remove(id);
                    }

                    string translated = null;
                    if (TranslationKeys.Contains(trimmed))
                        translated = Translations[trimmed];
                    else
                        translated = TryPatternMatch(trimmed);

                    if (translated != null)
                    {
                        translatedInstances.Add(id);
                        if (translated != current)
                        {
                            isPatching = true;
                            try { txt.text = translated; }
                            finally { isPatching = false; }
                        }
                    }
                    else
                    {
                        RecordUntranslated(trimmed);
                    }
                }
            }
            catch (Exception e)
            {
                Log.LogWarning($"Text scan error: {e.Message}");
            }
            finally
            {
                scanning = false;
            }
        }

        /// <summary>
        /// Record a string the scene scan could not translate.
        ///
        /// The scan — not the text-setter hook — is what actually translates most of the UI,
        /// but it used to drop its misses on the floor, so untranslated.txt only ever showed
        /// the handful of strings that happened to go through a setter. After a game update
        /// that is exactly the list we need, so collect here too.
        ///
        /// Only plain-ASCII text is recorded: anything already carrying Korean/Cyrillic/Arabic
        /// characters is our own output being re-scanned, not a missing entry.
        /// </summary>
        private void RecordUntranslated(string trimmed)
        {
            if (string.IsNullOrEmpty(trimmed)) return;
            // Encyclopedia unit descriptions run to ~400 characters; a 200 cap silently
            // hid every one of them from collection.
            if (trimmed.Length < 2 || trimmed.Length > 2000) return;
            if (IsNumericOrSymbol(trimmed)) return;
            if (IsMeasurementOnly(trimmed)) return;
            if (untranslatedStrings.Count >= 10000) return;

            bool hasAsciiLetter = false;
            foreach (char c in trimmed)
            {
                if (c > 127) return;  // already localized output, or non-Latin source
                if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) hasAsciiLetter = true;
            }
            if (!hasAsciiLetter) return;

            if (untranslatedStrings.Add(trimmed))
                missedCount++;
        }

        internal static string Translate(string original)
        {
            if (!Enabled || string.IsNullOrEmpty(original)) return original;

            string trimmed = original.Trim();
            if (TranslationKeys.Contains(trimmed))
            {
                Instance.translatedCount++;
                return Translations[trimmed];
            }

            // Pattern matching: "Category (N)" → "번역된카테고리 (N)"
            string patternResult = TryPatternMatch(trimmed);
            if (patternResult != null)
            {
                Instance.translatedCount++;
                return patternResult;
            }

            Instance.RecordUntranslated(trimmed);

            return original;
        }

        /// <summary>
        /// Try pattern matching for strings with suffixes like "(37)" or prefixes like "01. "
        /// </summary>
        private static string TryPatternMatch(string text)
        {
            // Pattern 1: "Word (N)" / "Word [N]" → "번역 (N)" — filter tags and list counts
            foreach (var bracket in new[] { new[] { " (", ")" }, new[] { " [", "]" } })
            {
                int start = text.LastIndexOf(bracket[0], StringComparison.Ordinal);
                if (start > 0 && text.EndsWith(bracket[1], StringComparison.Ordinal))
                {
                    string prefix = text.Substring(0, start);
                    string suffix = text.Substring(start); // " (37)" / " [2]"
                    if (TranslationKeys.Contains(prefix))
                        return Translations[prefix] + suffix;
                }
            }

            // Pattern 2: "NN. Word" → "NN. 번역" — numbered mission names
            if (text.Length > 3)
            {
                int dotIdx = text.IndexOf(". ");
                if (dotIdx >= 1 && dotIdx <= 3)
                {
                    string numPrefix = text.Substring(0, dotIdx + 2); // "01. "
                    string missionName = text.Substring(dotIdx + 2);
                    if (TranslationKeys.Contains(missionName))
                        return numPrefix + Translations[missionName];
                }
            }

            // Pattern 3: "Free Flight - MapName" → "자유 비행 - MapName"
            int dashIdx = text.IndexOf(" - ");
            if (dashIdx > 0)
            {
                string beforeDash = text.Substring(0, dashIdx);
                string afterDash = text.Substring(dashIdx + 3);
                if (TranslationKeys.Contains(beforeDash))
                {
                    string translatedBefore = Translations[beforeDash];
                    if (TranslationKeys.Contains(afterDash))
                        return translatedBefore + " - " + Translations[afterDash];
                    return translatedBefore + " - " + afterDash;
                }
            }

            // Pattern 4: "Tutorial N - Description" → "translated N - Description"
            if (text.StartsWith("Tutorial ") && text.Contains(" - "))
            {
                int tDash = text.IndexOf(" - ");
                string afterTDash = text.Substring(tDash + 3);
                string tutNum = text.Substring(9, tDash - 9); // "1", "2", etc.
                string tutWord = TranslationKeys.Contains("Tutorial") ? Translations["Tutorial"] : "Tutorial";
                if (TranslationKeys.Contains(afterTDash))
                    return tutWord + " " + tutNum + " - " + Translations[afterTDash];
                return tutWord + " " + tutNum + " - " + afterTDash;
            }

            // Pattern 5: "PALA/BDF UnitType ($price)" → "PALA 번역 ($price)"
            if (text.StartsWith("PALA ") || text.StartsWith("BDF "))
            {
                string faction = text.StartsWith("PALA ") ? "PALA " : "BDF ";
                string rest = text.Substring(faction.Length);
                // Strip price suffix like " ($45.9m)"
                int priceStart = rest.LastIndexOf(" ($");
                if (priceStart > 0 && rest.EndsWith(")"))
                {
                    string unitName = rest.Substring(0, priceStart);
                    string priceSuffix = rest.Substring(priceStart);
                    if (TranslationKeys.Contains(unitName))
                        return faction + Translations[unitName] + priceSuffix;
                }
                // Without price suffix
                if (TranslationKeys.Contains(rest))
                    return faction + Translations[rest];
            }

            // Pattern 6: "Buy AircraftName" → "translated AircraftName"
            if (text.StartsWith("Buy "))
            {
                string buyWord = TranslationKeys.Contains("Buy") ? Translations["Buy"] : "Buy";
                return buyWord + " " + text.Substring(4);
            }

            // Pattern 7: "Label: Value" → "번역: Value"
            // Readouts pair a fixed label with a live value, so only the label is looked up:
            // "Max Players: 8", "HE: 400kg", "RNG : 1.2km", "SPD : 648km/h".
            // The entry may be stored with the colon ("Max Players:") or without it ("HE"),
            // and the game is inconsistent about a space before the colon — handle all of it.
            int colonIdx = text.IndexOf(':');
            if (colonIdx > 0 && colonIdx < 30 && colonIdx < text.Length - 1)
            {
                string withColon = text.Substring(0, colonIdx + 1);
                if (TranslationKeys.Contains(withColon))
                    return Translations[withColon] + text.Substring(colonIdx + 1);

                string label = withColon.Substring(0, colonIdx).TrimEnd();
                if (label.Length > 0 && TranslationKeys.Contains(label))
                {
                    // keep whatever sat between the label and the colon
                    string gap = text.Substring(label.Length, colonIdx - label.Length);
                    return Translations[label] + gap + text.Substring(colonIdx);
                }
            }

            return null;
        }

        /// <summary>Unit tokens that only ever accompany a number, never a label worth translating.</summary>
        private static readonly HashSet<string> MeasurementUnits = new HashSet<string>(
            StringComparer.OrdinalIgnoreCase)
        {
            "m", "km", "cm", "mm", "nmi", "ft", "s", "ms", "min", "h",
            "g", "kg", "t", "kt", "lb", "lbs", "tnt",
            "km/h", "m/s", "mph", "kts", "rpm", "px", "fps",
            "kw", "mw", "w", "kn", "kj", "b", "k", "x", "%",
        };

        /// <summary>
        /// True for readouts that are nothing but a number and its unit — "$1.25m", "1060km/h",
        /// "0.25kg TNT", "x 120". The encyclopedia is full of these and they flooded
        /// untranslated.txt, burying the strings that actually need a translator.
        /// Anything with a real word in it ("40mm GMG", "25mm Autocannon") is kept.
        /// </summary>
        private static bool IsMeasurementOnly(string s)
        {
            bool sawDigit = false;
            foreach (var token in s.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries))
            {
                string t = token.TrimStart('$', '+', '-', '~', '(').TrimEnd(')', ',', '.');
                if (t.Length == 0) continue;

                // split "12.7mm" into its numeric head and unit tail
                int i = 0;
                while (i < t.Length && (char.IsDigit(t[i]) || t[i] == '.' || t[i] == ',')) i++;
                string head = t.Substring(0, i);
                string tail = t.Substring(i);

                if (head.Length > 0) sawDigit = true;
                if (tail.Length == 0) continue;                 // pure number
                if (!MeasurementUnits.Contains(tail)) return false;  // a real word — keep it
            }
            return sawDigit;
        }

        private static bool IsNumericOrSymbol(string s)
        {
            foreach (char c in s)
            {
                if (char.IsLetter(c)) return false;
            }
            return true;
        }

        internal static bool ContainsKorean(string s)
        {
            foreach (char c in s)
            {
                if (c >= 0xAC00 && c <= 0xD7AF) return true; // Hangul
                if (c >= 0x0400 && c <= 0x04FF) return true; // Cyrillic
                if (c >= 0x4E00 && c <= 0x9FFF) return true; // CJK
                if (c >= 0x3040 && c <= 0x30FF) return true; // Japanese
                if (c >= 0x0E00 && c <= 0x0E7F) return true; // Thai
                if (c >= 0x0600 && c <= 0x06FF) return true; // Arabic
            }
            return false;
        }

        internal void ExportUntranslated()
        {
            string exportPath = Path.Combine(
                Path.GetDirectoryName(translationFilePath),
                "untranslated.txt");

            var sorted = new List<string>(untranslatedStrings);
            sorted.Sort();

            using (var writer = new StreamWriter(exportPath, false, System.Text.Encoding.UTF8))
            {
                writer.WriteLine($"// Untranslated strings found in game ({sorted.Count} entries)");
                writer.WriteLine("// Copy these to ko.json and add Korean translations");
                writer.WriteLine();
                foreach (var s in sorted)
                {
                    string escaped = s.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n");
                    writer.WriteLine($"\"{escaped}\": \"\",");
                }
            }

            Log.LogInfo($"Exported {sorted.Count} untranslated strings to untranslated.txt");
        }

        /// <summary>
        /// Extract game data: hints CSV, encyclopedia descriptions, etc.
        /// Triggered by Ctrl+F11
        /// </summary>
        internal void ExtractGameData()
        {
            string outputDir = Path.GetDirectoryName(translationFilePath);
            var sb = new System.Text.StringBuilder();
            sb.AppendLine("// ========== EXTRACTED GAME DATA ==========");
            sb.AppendLine($"// Extraction time: {DateTime.Now}");
            sb.AppendLine();

            int totalExtracted = 0;

            // 1. Extract hints CSV from HintsTipsDisplay
            try
            {
                sb.AppendLine("// ========== DID YOU KNOW? HINTS ==========");
                var hintDisplays = Resources.FindObjectsOfTypeAll<MonoBehaviour>();
                foreach (var mb in hintDisplays)
                {
                    if (mb.GetType().Name != "HintsTipsDisplay") continue;

                    // Get hintsCSV field
                    var csvField = mb.GetType().GetField("hintsCSV",
                        BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                    if (csvField != null)
                    {
                        var textAsset = csvField.GetValue(mb) as TextAsset;
                        if (textAsset != null && !string.IsNullOrEmpty(textAsset.text))
                        {
                            sb.AppendLine($"// Raw CSV ({textAsset.text.Length} chars):");
                            sb.AppendLine(textAsset.text);
                            sb.AppendLine();

                            // Parse CSV lines
                            sb.AppendLine("// --- Parsed Hints for ko.json ---");
                            var lines = textAsset.text.Split('\n');
                            foreach (var line in lines)
                            {
                                if (string.IsNullOrWhiteSpace(line)) continue;
                                // CSV format is likely: id,type,text
                                var parts = ParseCSVLine(line);
                                if (parts.Count >= 3)
                                {
                                    string hintType = parts[1].Trim();
                                    string hintText = parts[2].Trim();
                                    if (!string.IsNullOrEmpty(hintText) && hintText.Length > 1)
                                    {
                                        string escaped = hintText.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n");
                                        sb.AppendLine($"// Type: {hintType}");
                                        sb.AppendLine($"\"{escaped}\": \"\",");
                                        totalExtracted++;
                                    }
                                }
                                else if (parts.Count >= 2)
                                {
                                    string hintText = parts[parts.Count - 1].Trim();
                                    if (!string.IsNullOrEmpty(hintText) && hintText.Length > 1)
                                    {
                                        string escaped = hintText.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n");
                                        sb.AppendLine($"\"{escaped}\": \"\",");
                                        totalExtracted++;
                                    }
                                }
                            }
                            Log.LogInfo($"Extracted {lines.Length} hint lines from CSV");
                        }
                        else
                            sb.AppendLine("// hintsCSV TextAsset is null or empty");
                    }
                    else
                        sb.AppendLine("// hintsCSV field not found");
                    break;
                }
            }
            catch (Exception e)
            {
                sb.AppendLine($"// Error extracting hints: {e.Message}");
                Log.LogWarning($"Hint extraction error: {e.Message}");
            }

            sb.AppendLine();

            // 2. Extract encyclopedia unit descriptions
            try
            {
                sb.AppendLine("// ========== ENCYCLOPEDIA DESCRIPTIONS ==========");
                var allSOs = Resources.FindObjectsOfTypeAll<ScriptableObject>();
                foreach (var so in allSOs)
                {
                    if (so.GetType().Name != "Encyclopedia") continue;

                    // Get all list fields (aircraft, vehicles, ships, buildings, missiles)
                    string[] listFields = { "aircraft", "vehicles", "ships", "buildings", "missiles", "scenery", "otherUnits" };
                    foreach (var fieldName in listFields)
                    {
                        var field = so.GetType().GetField(fieldName,
                            BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                        if (field == null) continue;

                        var list = field.GetValue(so) as System.Collections.IList;
                        if (list == null) continue;

                        sb.AppendLine($"// --- {fieldName} ({list.Count} entries) ---");
                        foreach (var item in list)
                        {
                            if (item == null) continue;
                            // UnitDefinition has name/description fields
                            var nameField = item.GetType().GetField("name",
                                BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                            var descField = item.GetType().GetField("description",
                                BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);

                            // Also try property
                            string unitName = null;
                            string unitDesc = null;

                            if (nameField != null)
                                unitName = nameField.GetValue(item) as string;
                            if (descField != null)
                                unitDesc = descField.GetValue(item) as string;

                            // Try properties if fields didn't work
                            if (unitName == null)
                            {
                                var nameProp = item.GetType().GetProperty("name",
                                    BindingFlags.Public | BindingFlags.Instance);
                                if (nameProp != null)
                                    unitName = nameProp.GetValue(item) as string;
                            }
                            if (unitDesc == null)
                            {
                                var descProp = item.GetType().GetProperty("description",
                                    BindingFlags.Public | BindingFlags.Instance);
                                if (descProp != null)
                                    unitDesc = descProp.GetValue(item) as string;
                            }

                            // Also search for "jsonKey" which might be the display name
                            var jsonKeyField = item.GetType().GetField("jsonKey",
                                BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                            string jsonKey = null;
                            if (jsonKeyField != null)
                                jsonKey = jsonKeyField.GetValue(item) as string;

                            // Try to get displayName
                            var displayNameField = item.GetType().GetField("displayName",
                                BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                            string displayName = null;
                            if (displayNameField != null)
                                displayName = displayNameField.GetValue(item) as string;

                            sb.AppendLine($"// Unit: {unitName ?? "(null)"} | JsonKey: {jsonKey ?? "(null)"} | DisplayName: {displayName ?? "(null)"}");

                            if (!string.IsNullOrEmpty(unitDesc))
                            {
                                string escaped = unitDesc.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n").Replace("\r", "");
                                sb.AppendLine($"\"{escaped}\": \"\",");
                                totalExtracted++;
                            }
                            else
                            {
                                sb.AppendLine("// (no description)");
                            }
                        }
                    }
                    break;
                }
            }
            catch (Exception e)
            {
                sb.AppendLine($"// Error extracting encyclopedia: {e.Message}");
                Log.LogWarning($"Encyclopedia extraction error: {e.Message}");
            }

            // 3. Also dump all fields of UnitDefinition type to understand structure
            try
            {
                sb.AppendLine();
                sb.AppendLine("// ========== UNIT DEFINITION STRUCTURE ==========");
                var allSOs = Resources.FindObjectsOfTypeAll<ScriptableObject>();
                foreach (var so in allSOs)
                {
                    string typeName = so.GetType().Name;
                    if (typeName.Contains("Definition") && so.GetType().BaseType != null)
                    {
                        sb.AppendLine($"// Type: {typeName} (Base: {so.GetType().BaseType.Name})");
                        foreach (var f in so.GetType().GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance))
                        {
                            object val = null;
                            try { val = f.GetValue(so); } catch { }
                            string valStr = val != null ? val.ToString() : "(null)";
                            if (valStr.Length > 200) valStr = valStr.Substring(0, 200) + "...";
                            sb.AppendLine($"//   {f.FieldType.Name} {f.Name} = {valStr}");
                        }
                        break; // Just dump one to understand structure
                    }
                }
            }
            catch (Exception e)
            {
                sb.AppendLine($"// Error: {e.Message}");
            }

            string outputPath = Path.Combine(outputDir, "extracted_gamedata.txt");
            File.WriteAllText(outputPath, sb.ToString(), System.Text.Encoding.UTF8);
            Log.LogInfo($"Game data extracted! {totalExtracted} entries saved to extracted_gamedata.txt");
        }

        /// <summary>
        /// Simple CSV line parser that handles quoted fields
        /// </summary>
        private static List<string> ParseCSVLine(string line)
        {
            var result = new List<string>();
            bool inQuotes = false;
            var current = new System.Text.StringBuilder();

            for (int i = 0; i < line.Length; i++)
            {
                char c = line[i];
                if (c == '"')
                {
                    inQuotes = !inQuotes;
                }
                else if (c == ',' && !inQuotes)
                {
                    result.Add(current.ToString());
                    current.Clear();
                }
                else
                {
                    current.Append(c);
                }
            }
            result.Add(current.ToString());
            return result;
        }

        #endregion

        #region Harmony Patches

        /// <summary>
        /// CRITICAL: Redirect FontEngine.LoadFontFace(Font, int) to use file path
        /// when the Font is our Korean proxy font. This makes CreateFontAsset and
        /// TryAddCharacters work with our Pretendard font loaded from file.
        /// </summary>
        static class FontEngine_LoadFontFace_Redirect
        {
            static bool redirecting = false;

            static bool Prefix(Font font, int pointSize, ref FontEngineError __result)
            {
                if (redirecting) return true;
                if (koreanProxyFont == null || font != koreanProxyFont || koreanFontFilePath == null)
                    return true;

                redirecting = true;
                try
                {
                    __result = FontEngine.LoadFontFace(koreanFontFilePath, pointSize);
                    Log.LogInfo($"FontEngine redirect: LoadFontFace(proxy, {pointSize}) → LoadFontFace(file) = {__result}");
                }
                catch (Exception e)
                {
                    Log.LogWarning($"FontEngine redirect failed: {e.Message}");
                    return true; // Fall through to original
                }
                finally
                {
                    redirecting = false;
                }
                return false; // Skip original method
            }
        }

        // Patch TMP_Text.text setter — main text interception point
        /// <summary>
        /// Postfix on TextMeshProUGUI/TextMeshPro.OnEnable — translate the component the moment
        /// it is shown, so prefab-authored text never flashes English.
        /// </summary>
        static class TMP_OnEnable_Patch
        {
            static void Postfix(TMP_Text __instance)
            {
                if (isPatching || !Enabled || Instance == null) return;
                // TranslateTmpComponent raises isPatching around its own assignment,
                // so nothing extra is needed here.
                try { Instance.TranslateTmpComponent(__instance); }
                catch { }
            }
        }

        static class TMP_Text_SetText_Patch
        {
            static void Prefix(TMP_Text __instance, ref string value)
            {
                if (isPatching || !Enabled || string.IsNullOrEmpty(value)) return;
                if (IsDialogueBoxTitle(__instance)) return; // Don't translate dialog titles
                isPatching = true;
                try
                {
                    string translated = Translate(value);
                    if (translated != value)
                    {
                        value = translated;
                        if (FontReady && ContainsKorean(translated))
                            EnsureKoreanFallback(__instance);
                    }
                }
                finally { isPatching = false; }
            }
        }

        // Patch Text.text setter (legacy UI)
        static class UIText_SetText_Patch
        {
            static void Prefix(Text __instance, ref string value)
            {
                if (isPatching || !Enabled || string.IsNullOrEmpty(value)) return;
                isPatching = true;
                try
                {
                    string translated = Translate(value);
                    if (translated != value)
                        value = translated;
                }
                finally { isPatching = false; }
            }
        }

        // Patch TMP_Text.SetText(string) method (may not exist in all TMP versions)
        static class TMP_Text_SetTextMethod_Patch
        {
            static void Prefix(TMP_Text __instance, ref string sourceText)
            {
                if (isPatching || !Enabled || string.IsNullOrEmpty(sourceText)) return;
                if (IsDialogueBoxTitle(__instance)) return;
                isPatching = true;
                try
                {
                    string translated = Translate(sourceText);
                    if (translated != sourceText)
                    {
                        sourceText = translated;
                        if (FontReady && ContainsKorean(translated))
                            EnsureKoreanFallback(__instance);
                    }
                }
                finally { isPatching = false; }
            }
        }

        /// <summary>
        /// Check if TMP_Text instance is a DialogueBox title field.
        /// DialogueBoxObjective.OnButtonPressed(title) uses the title string as a key,
        /// so translating it breaks the Ok button callback.
        /// </summary>
        static FieldInfo _fDialogTitleText;
        static bool _fDialogTitleTextCached;

        static bool IsDialogueBoxTitle(TMP_Text instance)
        {
            if (instance == null) return false;
            var dialogueBox = instance.GetComponentInParent<DialogueBox>();
            if (dialogueBox == null) return false;
            if (!_fDialogTitleTextCached)
            {
                _fDialogTitleTextCached = true;
                _fDialogTitleText = typeof(DialogueBox).GetField("titleText",
                    BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            }
            if (_fDialogTitleText == null) return false;
            var titleText = _fDialogTitleText.GetValue(dialogueBox) as TMP_Text;
            return instance == titleText;
        }

        #endregion

        #region GUI

        private void InitStyles()
        {
            if (stylesInit) return;
            boxStyle = new GUIStyle(GUI.skin.box);
            Texture2D bg = new Texture2D(1, 1);
            bg.SetPixel(0, 0, new Color(0.1f, 0.12f, 0.18f, 0.97f));
            bg.Apply();
            boxStyle.normal.background = bg;

            labelStyle = new GUIStyle(GUI.skin.label) { fontSize = 12 };
            labelStyle.normal.textColor = Color.white;

            headerStyle = new GUIStyle(GUI.skin.label)
            {
                fontSize = 14,
                fontStyle = FontStyle.Bold,
                alignment = TextAnchor.MiddleCenter
            };
            headerStyle.normal.textColor = new Color(0.7f, 0.85f, 1f);

            buttonStyle = new GUIStyle(GUI.skin.button) { fontSize = 12 };
            stylesInit = true;
        }

        private void OnGUI()
        {
            InitStyles();
            if (showUI)
                windowRect = GUI.Window(9997, windowRect, DrawWindow, "", boxStyle);
        }

        private void DrawWindow(int id)
        {
            GUILayout.BeginVertical();
            GUILayout.Label($"Localization Patch v3.5.0 ({CurrentLanguage})", headerStyle);
            GUILayout.Space(5);

            GUILayout.BeginHorizontal();
            GUILayout.Label("Patch:", labelStyle, GUILayout.Width(80));
            if (GUILayout.Button(Enabled ? "ON" : "OFF", buttonStyle, GUILayout.Width(60)))
                Enabled = !Enabled;
            GUILayout.EndHorizontal();

            GUILayout.Space(5);
            GUILayout.Label($"Entries loaded: {Translations.Count}", labelStyle);
            GUILayout.Label($"Applied: {translatedCount} / Missing: {missedCount}", labelStyle);
            GUILayout.Label($"Font: {fontStatusText}", labelStyle);
            GUILayout.Label($"Patched game fonts: {totalFontsPatched}", labelStyle);

            GUILayout.Space(10);
            if (GUILayout.Button("Reload translations (Ctrl+F10)", buttonStyle))
            {
                LoadTranslations();
            }

            if (GUILayout.Button("Export untranslated strings", buttonStyle))
            {
                ExportUntranslated();
            }

            GUILayout.Space(5);
            GUIStyle helpStyle = new GUIStyle(labelStyle) { fontSize = 10 };
            helpStyle.normal.textColor = Color.gray;
            GUILayout.Label("F10 = toggle panel", helpStyle);
            GUILayout.Label("Ctrl+F10 = reload translations", helpStyle);
            GUILayout.Label("Ctrl+F11 = extract game data", helpStyle);

            GUILayout.EndVertical();
            GUI.DragWindow();
        }

        #endregion
    }

    /// <summary>
    /// Standalone MonoBehaviour on its own GameObject.
    /// Bypasses BepInEx's MonoBehaviour lifecycle issues where Update()/coroutines
    /// never fire on some systems.
    /// </summary>
    internal class FrameHelper : MonoBehaviour
    {
        private bool logged = false;

        private void Update()
        {
            if (!logged)
            {
                logged = true;
                Plugin.Log?.LogInfo($"FrameHelper.Update() running (frame {Time.frameCount})");
            }

            // Debug: log any function key press to verify input system works
            if (Input.GetKeyDown(KeyCode.F9)) Plugin.Log?.LogInfo("[DEBUG] F9 detected");
            if (Input.GetKeyDown(KeyCode.F10)) Plugin.Log?.LogInfo("[DEBUG] F10 detected");
            if (Input.GetKeyDown(KeyCode.F12)) Plugin.Log?.LogInfo("[DEBUG] F12 detected");
            if (Input.anyKeyDown) Plugin.Log?.LogInfo($"[DEBUG] Any key: {Input.inputString}");

            Plugin.Instance?.DoPerFrameLogic();
        }
    }
}
