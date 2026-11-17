-- ============================================================================
--  hyprland-el desktop  ·  system default configuration  (/etc/xdg/hypr)
--
--  Change settings with the "Hyprland-Einstellungen" app (SUPER+I) – it writes
--  ~/.config/hypr-el/settings.json and regenerates ~/.config/hypr-el/settings.lua,
--  which this file reads.
--
--  For full control: `hypr-el-setup --copy` puts a copy of this file into
--  ~/.config/hypr/hyprland.lua, which then takes precedence.
--  Wiki: https://wiki.hypr.land/configuring/      All key bindings: SUPER+F1
-- ============================================================================

local HOME   = os.getenv("HOME") or ""
local XDGCFG = os.getenv("XDG_CONFIG_HOME") or (HOME .. "/.config")
local ELCFG  = XDGCFG .. "/hypr-el"

local function exists(path)
    local f = io.open(path, "r")
    if f then f:close() return true end
    return false
end

-------------------------------------------------------------------------------
-- settings (defaults = theme "Tiefsee"; overridden by hypr-el-settings)
-------------------------------------------------------------------------------
local S = {
    theme = {
        dark = true, bg = "#090d14", base = "#111823", surface = "#1a2431", overlay = "#2a3a4e",
        muted = "#5b6f86", fg = "#cdd9e5", fg_dim = "#93a7bb", accent = "#6aa9c9", accent2 = "#8ccbe6",
        red = "#e06c75", green = "#8fc5a3", yellow = "#e5c07b", blue = "#6aa9c9", magenta = "#b49ddb",
        cyan = "#7fd1d9", orange = "#e0a370",
    },
    titlebars = true, gaps_in = 4, gaps_out = 10, rounding = 8, border_size = 2,
    blur = true, shadows = true, animations = true, active_opacity = 0.96, inactive_opacity = 0.88,
    layout = "dwindle", float_new_windows = false, focus_follows_mouse = true,
    kb_layout = "us", kb_variant = "", numlock = true, mouse_sensitivity = 0.0,
    mouse_natural_scroll = false, touchpad_natural_scroll = true, tap_to_click = true,
    monitors = {}, terminal = "kitty", file_manager = "nautilus", browser = "firefox",
}
do
    local ok, user = pcall(dofile, ELCFG .. "/settings.lua")
    if ok and type(user) == "table" then
        for k, v in pairs(user) do S[k] = v end
    end
end
local T = S.theme

-- "#rrggbb" -> "rgba(rrggbbaa)"
local function col(hex, alpha)
    return string.format("rgba(%s%02x)", hex:sub(2), math.floor((alpha or 1) * 255 + 0.5))
end

------------------
---- MONITORS ----
------------------

for _, m in ipairs(S.monitors or {}) do
    hl.monitor({ output = m.output, mode = m.mode, position = m.position or "auto", scale = m.scale or "auto" })
end
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })

---------------------
---- MY PROGRAMS ----
---------------------

local function have(bin)
    return os.execute("command -v " .. bin .. " >/dev/null 2>&1") == true
end

local terminal = S.terminal
if terminal == "kitty" and not exists(XDGCFG .. "/kitty/kitty.conf") then
    terminal = "kitty --config " .. ELCFG .. "/kitty.conf"
end
local fileManager = have(S.file_manager) and S.file_manager or terminal
local browser     = have(S.browser) and S.browser or "xdg-open https://"
local menu        = "hyprlauncher"

-------------------
---- AUTOSTART ----
-------------------

hl.on("hyprland.start", function()
    hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP XDG_SESSION_TYPE HYPRLAND_INSTANCE_SIGNATURE GTK_THEME ADW_DEBUG_COLOR_SCHEME QT_QPA_PLATFORM QT_QPA_PLATFORMTHEME")
    -- wallpaper, bar, notifications, idle/lock, polkit agent, theme
    hl.exec_cmd("hypr-el-session start")
end)

-------------------------------
---- ENVIRONMENT VARIABLES ----
-------------------------------

hl.env("XCURSOR_THEME", "Adwaita")
hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("QT_QPA_PLATFORM", "wayland;xcb")
if exists("/usr/lib64/qt6/plugins/platformthemes/libhyprqt6engine.so") then
    hl.env("QT_QPA_PLATFORMTHEME", "hyprqt6engine")
end
hl.env("GDK_BACKEND", "wayland,x11,*")
-- dark/light GTK4 + libadwaita apps according to the theme
hl.env("ADW_DEBUG_COLOR_SCHEME", T.dark and "prefer-dark" or "prefer-light")
hl.env("GTK_THEME", T.dark and "Adwaita:dark" or "Adwaita")
hl.env("SDL_VIDEODRIVER", "wayland,x11")
hl.env("MOZ_ENABLE_WAYLAND", "1")
hl.env("ELECTRON_OZONE_PLATFORM_HINT", "auto")

-----------------------
---- LOOK AND FEEL ----
-----------------------

hl.config({
    general = {
        gaps_in     = S.gaps_in,
        gaps_out    = S.gaps_out,
        border_size = S.border_size,
        col = {
            active_border   = { colors = { col(T.accent, 0.9), col(T.accent2, 0.5) }, angle = 45 },
            inactive_border = col(T.overlay, 0.45),
        },
        resize_on_border        = true,
        extend_border_grab_area = 12,
        hover_icon_on_border    = true,
        layout = S.layout,
    },

    decoration = {
        rounding       = S.rounding,
        rounding_power = 2,
        active_opacity   = S.active_opacity,
        inactive_opacity = S.inactive_opacity,
        shadow = {
            enabled      = S.shadows,
            range        = 12,
            render_power = 3,
            color        = T.dark and 0x55000000 or 0x30000000,
        },
        blur = {
            enabled   = S.blur,
            size      = 7,
            passes    = 3,
            noise     = 0.015,
            contrast  = 0.95,
            brightness = 0.85,
            vibrancy  = 0.2,
            popups    = true,
            xray      = false,
        },
    },

    animations = { enabled = S.animations },

    dwindle   = { preserve_split = true },
    master    = { new_status = "master" },
    scrolling = { fullscreen_on_one_column = true },

    misc = {
        force_default_wallpaper  = 0,
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        focus_on_activate        = true,
        animate_manual_resizes   = true,
        animate_mouse_windowdragging = true,
        mouse_move_enables_dpms  = true,
        key_press_enables_dpms   = true,
        middle_click_paste       = true,
    },
    layers = { allow_new_top_layers_over_existing_fullscreen = true },
})

hl.curve("easeOutQuint", { type = "bezier", points = { {0.23, 1},  {0.32, 1} } })
hl.curve("linear",       { type = "bezier", points = { {0, 0},     {1, 1}    } })
hl.curve("almostLinear", { type = "bezier", points = { {0.5, 0.5}, {0.75, 1} } })
hl.curve("quick",        { type = "bezier", points = { {0.15, 0},  {0.1, 1}  } })
hl.curve("easy",         { type = "spring", mass = 1, stiffness = 238.1191, damping = 24.21279333 })

hl.curve("wind",         { type = "bezier", points = { {0.05, 0.9}, {0.1, 1.05} } })
hl.curve("winIn",        { type = "bezier", points = { {0.1, 1.1},  {0.1, 1.1}  } })
hl.curve("winOut",       { type = "bezier", points = { {0.3, -0.3}, {0, 1}      } })

hl.animation({ leaf = "global",        enabled = true, speed = 10,   bezier = "default" })
hl.animation({ leaf = "border",        enabled = true, speed = 5.39, bezier = "easeOutQuint" })
hl.animation({ leaf = "windows",       enabled = true, speed = 6,    bezier = "wind",   style = "slide" })
hl.animation({ leaf = "windowsIn",     enabled = true, speed = 6,    bezier = "winIn",  style = "slide" })
hl.animation({ leaf = "windowsOut",    enabled = true, speed = 5,    bezier = "winOut", style = "slide" })
hl.animation({ leaf = "windowsMove",   enabled = true, speed = 5,    bezier = "wind",   style = "slide" })
hl.animation({ leaf = "fadeIn",        enabled = true, speed = 1.73, bezier = "almostLinear" })
hl.animation({ leaf = "fadeOut",       enabled = true, speed = 1.46, bezier = "almostLinear" })
hl.animation({ leaf = "fade",          enabled = true, speed = 3.03, bezier = "quick" })
hl.animation({ leaf = "layers",        enabled = true, speed = 3.81, bezier = "easeOutQuint" })
hl.animation({ leaf = "layersIn",      enabled = true, speed = 4,    bezier = "easeOutQuint", style = "slide" })
hl.animation({ leaf = "layersOut",     enabled = true, speed = 1.5,  bezier = "linear",       style = "fade" })
hl.animation({ leaf = "workspaces",    enabled = true, speed = 5,    bezier = "wind",   style = "slidefade 20%" })
hl.animation({ leaf = "specialWorkspace", enabled = true, speed = 4, bezier = "wind", style = "slidefadevert 20%" })

---------------------------------------------------------------
---- TITLE BARS (hyprbars plugin from hyprland-plugins)    ----
---------------------------------------------------------------

local HYPRBARS = "/usr/lib64/hyprland/plugins/hyprbars.so"
local haveBars = exists(HYPRBARS)
if haveBars then
    hl.plugin.load(HYPRBARS)
    hl.config({
        plugin = {
            hyprbars = {
                enabled           = S.titlebars,
                bar_height        = 32,
                bar_color         = col(T.base, 0.92),
                ["col.text"]      = col(T.fg_dim),
                bar_text_font     = "Sans",
                bar_text_size     = 10,
                bar_text_weight   = "medium",
                bar_text_align    = "left",
                bar_padding       = 12,
                bar_button_padding = 10,
                bar_part_of_window = true,
                bar_precedence_over_border = true,
                bar_blur          = true,
                icon_on_hover     = false,
                on_double_click   = "hyprctl eval 'hypr_el.toggle_maximize()'",
            },
        },
    })
end

-------------------------------------------------------------
---- WINDOW ACTIONS: minimize / restore / maximize       ----
-------------------------------------------------------------
-- Hyprland has no minimized state of its own. hypr-el keeps minimized
-- windows on the hidden special workspace "minimized"; the taskbar in the
-- bar (click), SUPER+SHIFT+H or the minimize button bring them back.

local MINWS = "special:minimized"
hypr_el = {}

local function sel(w) return "address:" .. tostring(w.address) end

local function isMinimized(w)
    return w and w.workspace and w.workspace.name == MINWS
end

function hypr_el.minimize(w)
    w = w or hl.get_active_window()
    if not w or isMinimized(w) then return end
    hl.dispatch(hl.dsp.window.move({ workspace = MINWS, follow = false, window = sel(w) }))
end

function hypr_el.restore(w)
    if not isMinimized(w) then return end
    local ws = hl.get_active_workspace()
    hl.dispatch(hl.dsp.window.move({ workspace = ws and ws.id or 1, follow = true, window = sel(w) }))
    local sp = hl.get_active_special_workspace()
    if sp and sp.name == MINWS then
        hl.dispatch(hl.dsp.workspace.toggle_special("minimized"))
    end
    hl.dispatch(hl.dsp.focus({ window = sel(w) }))
end

function hypr_el.restore_last()
    local last
    for _, w in ipairs(hl.get_windows() or {}) do
        if isMinimized(w) and (not last or (w.focus_history_id or 0) < (last.focus_history_id or 0)) then
            last = w
        end
    end
    if last then hypr_el.restore(last) end
end

function hypr_el.toggle_maximize()
    hl.dispatch(hl.dsp.window.fullscreen({ mode = "maximized", action = "toggle" }))
end

-- taskbar "minimize" (right click) and other foreign-toplevel requests
hl.on("window.minimize", function(w, state)
    if state then hypr_el.minimize(w) else hypr_el.restore(w) end
end)

-- activating a minimized window (taskbar click, notifications, ...) restores it
hl.on("window.active", function(w)
    if isMinimized(w) then hypr_el.restore(w) end
end)

if haveBars and hl.plugin.hyprbars and hl.plugin.hyprbars.add_button then
    -- buttons are added right to left: close, maximize, minimize
    -- buttons are drawn right to left: close, maximize, minimize (always visible, with icons)
    hl.plugin.hyprbars.add_button({ bg_color = col(T.red),     fg_color = col(T.bg), size = 18, icon = "✕",
        action = "hyprctl dispatch 'hl.dsp.window.close()'" })
    hl.plugin.hyprbars.add_button({ bg_color = col(T.yellow),  fg_color = col(T.bg), size = 18, icon = "□",
        action = "hyprctl eval 'hypr_el.toggle_maximize()'" })
    hl.plugin.hyprbars.add_button({ bg_color = col(T.green),   fg_color = col(T.bg), size = 18, icon = "–",
        action = "hyprctl eval 'hypr_el.minimize()'" })

    -- every normal window gets the same bar (GTK apps keep their header bar below it);
    -- only the screen-share picker and the desktop stay bare
    hl.window_rule({
        name  = "no-titlebar",
        match = { class = "^(hyprland-share-picker|hypr-el-desktop)$" },
        ["hyprbars:no_bar"] = true,
    })
end

---------------
---- INPUT ----
---------------

hl.config({
    input = {
        kb_layout  = S.kb_layout,
        kb_variant = S.kb_variant,
        kb_options = S.kb_layout:find(",") and "grp:alt_shift_toggle" or "",
        numlock_by_default = S.numlock,
        repeat_rate  = 30,
        repeat_delay = 300,
        follow_mouse = S.focus_follows_mouse and 1 or 2,
        sensitivity  = S.mouse_sensitivity,
        natural_scroll = S.mouse_natural_scroll,
        touchpad = {
            natural_scroll       = S.touchpad_natural_scroll,
            tap_to_click         = S.tap_to_click,
            disable_while_typing = true,
        },
    },
    cursor = { hide_on_key_press = false },
})

hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })

---------------------
---- KEYBINDINGS ----
---------------------
-- SUPER + F1 shows the full list.

local mod = "SUPER"

-- apps
hl.bind(mod .. " + Return",     hl.dsp.exec_cmd(terminal))
hl.bind(mod .. " + T",          hl.dsp.exec_cmd(terminal))
hl.bind(mod .. " + E",          hl.dsp.exec_cmd(fileManager))
hl.bind(mod .. " + B",          hl.dsp.exec_cmd(browser))
hl.bind(mod .. " + SPACE",      hl.dsp.exec_cmd(menu))
hl.bind(mod .. " + R",          hl.dsp.exec_cmd(menu))
hl.bind(mod .. " + I",          hl.dsp.exec_cmd("hypr-el-settings"))
hl.bind(mod .. " + F1",         hl.dsp.exec_cmd("hypr-el-keys"))
hl.bind(mod .. " + L",          hl.dsp.exec_cmd("hypr-el-lock"))
hl.bind(mod .. " + Escape",     hl.dsp.exec_cmd("hyprshutdown"))
hl.bind(mod .. " + SHIFT + T",  hl.dsp.exec_cmd("hypr-el-settings --next-theme"))
hl.bind(mod .. " + SHIFT + C",  hl.dsp.exec_cmd("hyprpicker -a -n"))
hl.bind(mod .. " + N",          hl.dsp.exec_cmd("makoctl dismiss -a"))

-- screenshots
hl.bind("Print",                hl.dsp.exec_cmd("hypr-el-screenshot area"))
hl.bind(mod .. " + SHIFT + S",  hl.dsp.exec_cmd("hypr-el-screenshot area"))
hl.bind("SHIFT + Print",        hl.dsp.exec_cmd("hypr-el-screenshot screen"))
hl.bind(mod .. " + Print",      hl.dsp.exec_cmd("hypr-el-screenshot window"))

-- windows (familiar shortcuts first)
hl.bind("ALT + F4",             hl.dsp.window.close())
hl.bind(mod .. " + Q",          hl.dsp.window.close())
hl.bind(mod .. " + H",          function() hypr_el.minimize() end)
hl.bind(mod .. " + SHIFT + H",  function() hypr_el.restore_last() end)
hl.bind(mod .. " + up",         function() hypr_el.toggle_maximize() end)
hl.bind(mod .. " + F",          hl.dsp.window.fullscreen())
hl.bind(mod .. " + V",          hl.dsp.window.float({ action = "toggle" }))
hl.bind(mod .. " + C",          hl.dsp.window.center())
hl.bind(mod .. " + P",          hl.dsp.window.pin())
hl.bind(mod .. " + J",          hl.dsp.layout("togglesplit"))
hl.bind(mod .. " + G",          hl.dsp.group.toggle())
hl.bind(mod .. " + Tab",        hl.dsp.group.next())
hl.bind("ALT + Tab",            hl.dsp.window.cycle_next())

-- focus with SUPER + arrows (up = maximize, see above), move with SUPER + SHIFT
hl.bind(mod .. " + left",          hl.dsp.focus({ direction = "left" }))
hl.bind(mod .. " + right",         hl.dsp.focus({ direction = "right" }))
hl.bind(mod .. " + down",          hl.dsp.focus({ direction = "down" }))
hl.bind(mod .. " + ALT + up",      hl.dsp.focus({ direction = "up" }))
for _, d in ipairs({ "left", "right", "up", "down" }) do
    hl.bind(mod .. " + SHIFT + " .. d, hl.dsp.window.move({ direction = d }))
end
hl.bind(mod .. " + CTRL + left",  hl.dsp.window.resize({ x = -50, y = 0,   relative = true }), { repeating = true })
hl.bind(mod .. " + CTRL + right", hl.dsp.window.resize({ x = 50,  y = 0,   relative = true }), { repeating = true })
hl.bind(mod .. " + CTRL + up",    hl.dsp.window.resize({ x = 0,   y = -50, relative = true }), { repeating = true })
hl.bind(mod .. " + CTRL + down",  hl.dsp.window.resize({ x = 0,   y = 50,  relative = true }), { repeating = true })

-- workspaces
for i = 1, 10 do
    local key = i % 10
    hl.bind(mod .. " + " .. key,         hl.dsp.focus({ workspace = i }))
    hl.bind(mod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end
hl.bind(mod .. " + Page_Down",  hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mod .. " + Page_Up",    hl.dsp.focus({ workspace = "e-1" }))
hl.bind(mod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))
hl.bind(mod .. " + S",          hl.dsp.workspace.toggle_special("scratchpad"))
hl.bind(mod .. " + ALT + S",    hl.dsp.window.move({ workspace = "special:scratchpad" }))

-- mouse: SUPER + left drag = move, SUPER + right drag = resize
hl.bind(mod .. " + mouse:272", hl.dsp.window.drag(),   { mouse = true })
hl.bind(mod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

-- media and brightness keys
hl.bind("XF86AudioRaiseVolume",  hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume",  hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",         hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),     { locked = true })
hl.bind("XF86AudioMicMute",      hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),   { locked = true })
hl.bind("XF86MonBrightnessUp",   hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"),                  { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"),                  { locked = true, repeating = true })
hl.bind("XF86AudioNext",         hl.dsp.exec_cmd("playerctl next"),       { locked = true })
hl.bind("XF86AudioPause",        hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPlay",         hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev",         hl.dsp.exec_cmd("playerctl previous"),   { locked = true })

--------------------------------
---- WINDOWS AND WORKSPACES ----
--------------------------------

hl.window_rule({ name = "suppress-maximize-events", match = { class = ".*" }, suppress_event = "maximize" })

hl.window_rule({
    name  = "fix-xwayland-drags",
    match = { class = "^$", title = "^$", xwayland = true, float = true, fullscreen = false, pin = false },
    no_focus = true,
})

if S.float_new_windows then
    hl.window_rule({ name = "float-everything", match = { class = ".*" }, float = true })
end

hl.window_rule({
    name  = "float-tools",
    match = { class = "^(org\\.pulseaudio\\.pavucontrol|pavucontrol|nm-connection-editor|hyprland-share-picker|hyprpwcenter|hyprsysteminfo|org\\.gnome\\.Calculator|xdg-desktop-portal-gtk|hypr-el-nmtui|hypr-el-btop)$" },
    float  = true,
    size   = "960 640",
    center = true,
})
hl.window_rule({ name = "hypr-el-settings", match = { class = "^(io\\.github\\.perutzit\\.HyprElSettings)$" }, float = true, size = "1060 760", center = true })
hl.window_rule({ name = "hypr-el-keys",     match = { class = "^(hypr-el-keys)$" },     float = true, size = "980 760",  center = true })
hl.window_rule({ name = "float-dialogs", match = { title = "^(Open File|Save File|Save As|Open Folder|File Upload|Datei öffnen|Datei speichern|Speichern unter|Ordner öffnen)(.*)$" }, float = true, center = true })
hl.window_rule({ name = "pip", match = { title = "^(Picture-in-Picture|Bild-im-Bild)$" }, float = true, pin = true, size = "640 360", move = "monitor_w-660 monitor_h-380" })
hl.window_rule({ name = "move-hyprland-run", match = { class = "hyprland-run" }, move = "20 monitor_h-120", float = true })

-- frosted glass behind bar, notifications and launcher
hl.layer_rule({ name = "blur-waybar",   match = { namespace = "^waybar$" },        blur = true, ignore_alpha = 0.3 })
hl.layer_rule({ name = "blur-mako",     match = { namespace = "^notifications$" }, blur = true, ignore_alpha = 0.3 })
hl.layer_rule({ name = "blur-launcher", match = { namespace = "^hyprlauncher$" },  blur = true, ignore_alpha = 0.3 })
hl.layer_rule({ name = "desktop-icons", match = { namespace = "^hypr-el-desktop$" }, no_anim = true })
