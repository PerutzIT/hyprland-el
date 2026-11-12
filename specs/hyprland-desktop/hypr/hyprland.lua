-- ============================================================================
--  hyprland-el desktop  ·  system default configuration
--
--  Installed as /etc/xdg/hypr/hyprland.lua by the "hyprland-desktop" package.
--  Hyprland uses this file as long as ~/.config/hypr/hyprland.lua does not
--  exist. To customise, run `hypr-el-setup --copy` and edit the copy in
--  ~/.config/hypr/. Wiki: https://wiki.hypr.land/configuring/
--
--  SUPER + F1 shows all key bindings.
-- ============================================================================

local HOME   = os.getenv("HOME") or ""
local XDGCFG = os.getenv("XDG_CONFIG_HOME") or (HOME .. "/.config")
local SHARE  = "/usr/share/hypr-el"

local function exists(path)
    local f = io.open(path, "r")
    if f then f:close() return true end
    return false
end

-- Use the user's own config file if there is one, otherwise our default.
local function cfg(user_rel, default_rel)
    if exists(XDGCFG .. "/" .. user_rel) then return nil end
    return SHARE .. "/" .. default_rel
end

local function have(bin)
    return os.execute("command -v " .. bin .. " >/dev/null 2>&1") == true
end

------------------
---- MONITORS ----
------------------

-- Every monitor at its preferred mode, placed automatically, auto scale.
-- Example for a fixed setup:
-- hl.monitor({ output = "DP-1", mode = "2560x1440@144", position = "0x0", scale = 1 })
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })

---------------------
---- MY PROGRAMS ----
---------------------

local kittyCfg    = cfg("kitty/kitty.conf", "kitty/kitty.conf")
local terminal    = kittyCfg and ("kitty --config " .. kittyCfg) or "kitty"
local fileManager = have("nautilus") and "nautilus --new-window" or (have("dolphin") and "dolphin" or terminal)
local browser     = have("firefox") and "firefox" or "xdg-open https://"
local menu        = "hyprlauncher"
local lock        = "pidof hyprlock || hyprlock"

-------------------
---- AUTOSTART ----
-------------------

hl.on("hyprland.start", function()
    -- session environment for systemd/dbus activated services (portals, polkit, ...)
    hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP XDG_SESSION_TYPE HYPRLAND_INSTANCE_SIGNATURE QT_QPA_PLATFORMTHEME")

    hl.exec_cmd("hyprpaper")
    hl.exec_cmd("hypridle")
    hl.exec_cmd("systemctl --user start hyprpolkitagent")

    local wb = cfg("waybar/config.jsonc", "waybar/config.jsonc")
    if wb and not exists(XDGCFG .. "/waybar/config") then
        hl.exec_cmd("waybar -c " .. SHARE .. "/waybar/config.jsonc -s " .. SHARE .. "/waybar/style.css")
    else
        hl.exec_cmd("waybar")
    end

    local mk = cfg("mako/config", "mako/config")
    hl.exec_cmd(mk and ("mako --config " .. mk) or "mako")

    if have("nm-applet") then hl.exec_cmd("nm-applet --indicator") end

    -- dark GTK/GNOME look for all apps, Qt follows through hyprqt6engine
    hl.exec_cmd("hypr-el-setup --theme")
    hl.exec_cmd("hypr-el-setup --welcome")
end)

-------------------------------
---- ENVIRONMENT VARIABLES ----
-------------------------------

hl.env("XCURSOR_THEME", "Adwaita")
hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("QT_QPA_PLATFORM", "wayland;xcb")
hl.env("QT_QPA_PLATFORMTHEME", "hyprqt6engine")
hl.env("QT_WAYLAND_DISABLE_WINDOWDECORATION", "1")
hl.env("GDK_BACKEND", "wayland,x11,*")
hl.env("SDL_VIDEODRIVER", "wayland,x11")
hl.env("CLUTTER_BACKEND", "wayland")
hl.env("MOZ_ENABLE_WAYLAND", "1")
hl.env("ELECTRON_OZONE_PLATFORM_HINT", "auto")

-----------------------
---- LOOK AND FEEL ----
-----------------------

hl.config({
    general = {
        gaps_in  = 6,
        gaps_out = 14,
        border_size = 3,
        col = {
            active_border   = { colors = { "rgba(33ccffff)", "rgba(00e0a8ff)", "rgba(8b5cf6ff)" }, angle = 45 },
            inactive_border = "rgba(2a2e4a99)",
        },
        resize_on_border = true,
        extend_border_grab_area = 15,
        allow_tearing = false,
        layout = "dwindle",
    },

    decoration = {
        rounding       = 12,
        rounding_power = 2.5,

        active_opacity   = 1.0,
        inactive_opacity = 0.92,

        dim_inactive = true,
        dim_strength = 0.06,

        shadow = {
            enabled      = true,
            range        = 18,
            render_power = 3,
            color        = 0x66000000,
        },

        blur = {
            enabled   = true,
            size      = 6,
            passes    = 3,
            noise     = 0.02,
            contrast  = 1.0,
            vibrancy  = 0.2,
            popups    = true,
        },
    },

    animations = {
        enabled = true,
    },
})

hl.curve("easeOutQuint",   { type = "bezier", points = { {0.23, 1},    {0.32, 1} } })
hl.curve("easeInOutCubic", { type = "bezier", points = { {0.65, 0.05}, {0.36, 1} } })
hl.curve("linear",         { type = "bezier", points = { {0, 0},       {1, 1}    } })
hl.curve("almostLinear",   { type = "bezier", points = { {0.5, 0.5},   {0.75, 1} } })
hl.curve("quick",          { type = "bezier", points = { {0.15, 0},    {0.1, 1}  } })
hl.curve("overshot",       { type = "bezier", points = { {0.05, 0.9},  {0.1, 1.08} } })
hl.curve("easy",           { type = "spring", mass = 1, stiffness = 238.1191, damping = 24.21279333 })

hl.animation({ leaf = "global",        enabled = true, speed = 10,   bezier = "default" })
hl.animation({ leaf = "border",        enabled = true, speed = 5.39, bezier = "easeOutQuint" })
hl.animation({ leaf = "borderangle",   enabled = true, speed = 60,   bezier = "linear", style = "loop" })
hl.animation({ leaf = "windows",       enabled = true, speed = 4.79, spring = "easy" })
hl.animation({ leaf = "windowsIn",     enabled = true, speed = 4.1,  spring = "easy",         style = "popin 80%" })
hl.animation({ leaf = "windowsOut",    enabled = true, speed = 1.49, bezier = "linear",       style = "popin 87%" })
hl.animation({ leaf = "fadeIn",        enabled = true, speed = 1.73, bezier = "almostLinear" })
hl.animation({ leaf = "fadeOut",       enabled = true, speed = 1.46, bezier = "almostLinear" })
hl.animation({ leaf = "fade",          enabled = true, speed = 3.03, bezier = "quick" })
hl.animation({ leaf = "layers",        enabled = true, speed = 3.81, bezier = "easeOutQuint" })
hl.animation({ leaf = "layersIn",      enabled = true, speed = 4,    bezier = "easeOutQuint", style = "slide" })
hl.animation({ leaf = "layersOut",     enabled = true, speed = 1.5,  bezier = "linear",       style = "fade" })
hl.animation({ leaf = "fadeLayersIn",  enabled = true, speed = 1.79, bezier = "almostLinear" })
hl.animation({ leaf = "fadeLayersOut", enabled = true, speed = 1.39, bezier = "almostLinear" })
hl.animation({ leaf = "workspaces",    enabled = true, speed = 4,    bezier = "overshot",     style = "slide" })
hl.animation({ leaf = "specialWorkspace", enabled = true, speed = 4, bezier = "overshot",     style = "slidevert" })
hl.animation({ leaf = "zoomFactor",    enabled = true, speed = 7,    bezier = "quick" })

-- No gaps/borders when a single tiled window is on the workspace
hl.workspace_rule({ workspace = "w[tv1]", gaps_out = 0, gaps_in = 0 })
hl.workspace_rule({ workspace = "f[1]",   gaps_out = 0, gaps_in = 0 })
hl.window_rule({ name = "no-gaps-wtv1", match = { float = false, workspace = "w[tv1]" }, border_size = 0, rounding = 0 })
hl.window_rule({ name = "no-gaps-f1",   match = { float = false, workspace = "f[1]" },   border_size = 0, rounding = 0 })

hl.config({
    dwindle   = { preserve_split = true, smart_split = false, smart_resizing = true },
    master    = { new_status = "master" },
    scrolling = { fullscreen_on_one_column = true },
})

----------------
----  MISC  ----
----------------

hl.config({
    misc = {
        force_default_wallpaper = 0,
        disable_hyprland_logo   = true,
        disable_splash_rendering = true,
        focus_on_activate       = true,
        animate_manual_resizes  = true,
        animate_mouse_windowdragging = true,
        enable_swallow          = true,
        swallow_regex           = "^(kitty)$",
        mouse_move_enables_dpms = true,
        key_press_enables_dpms  = true,
    },
    layers = {
        allow_new_top_layers_over_existing_fullscreen = true,
    },
    cursor = {
        hide_on_key_press = true,
    },
})

---------------
---- INPUT ----
---------------

-- Keyboard layout, detected in this order:
--   1. the user's GNOME setting (Settings > Keyboard, gsettings input-sources)
--   2. the system setting (localectl / X11 layout chosen in the installer)
--   3. the console keymap (/etc/vconsole.conf)
-- Several layouts are switched with ALT+SHIFT.
-- To force one, replace the detection, e.g.: kbLayout, kbVariant = "de", "nodeadkeys"
local function readCmd(cmd)
    local h = io.popen(cmd .. " 2>/dev/null")
    if not h then return "" end
    local out = h:read("*a") or ""
    h:close()
    return out
end

local function detectLayout()
    -- 1. GNOME: [('xkb', 'at'), ('xkb', 'us+intl')]
    local layouts, variants = {}, {}
    for src in readCmd("gsettings get org.gnome.desktop.input-sources sources"):gmatch("%('xkb',%s*'([^']+)'%)") do
        local l, v = src:match("^([^+]+)%+?(.*)$")
        table.insert(layouts, l)
        table.insert(variants, v or "")
    end
    if #layouts > 0 then
        return table.concat(layouts, ","), table.concat(variants, ",")
    end

    -- 2. systemd-localed
    local out = readCmd("localectl status")
    local l = out:match("X11 Layout:%s*([%w,_%-]+)")
    if l and l ~= "n" then
        local v = out:match("X11 Variant:%s*([%w,_%-]+)")
        return l, (v and v ~= "n") and v or ""
    end

    -- 3. console keymap, e.g. KEYMAP="de-latin1-nodeadkeys"
    local f = io.open("/etc/vconsole.conf", "r")
    if f then
        local km = (f:read("*a") or ""):match("KEYMAP=\"?([%w_%-]+)")
        f:close()
        if km then return km:match("^(%a+)") or "us", "" end
    end
    return "us", ""
end
local kbLayout, kbVariant = detectLayout()

hl.config({
    input = {
        kb_layout  = kbLayout,
        kb_variant = kbVariant,
        kb_options = kbLayout:find(",") and "grp:alt_shift_toggle" or "",
        numlock_by_default = true,
        repeat_rate  = 35,
        repeat_delay = 280,

        follow_mouse = 1,
        sensitivity  = 0,

        touchpad = {
            natural_scroll = true,
            tap_to_click   = true,
            disable_while_typing = true,
        },
    },
})

hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })

---------------------
---- KEYBINDINGS ----
---------------------
-- SUPER + F1 shows this list in a window (hypr-el-keys).

local mod = "SUPER"

-- apps
hl.bind(mod .. " + Return",     hl.dsp.exec_cmd(terminal))
hl.bind(mod .. " + Q",          hl.dsp.exec_cmd(terminal))
hl.bind(mod .. " + E",          hl.dsp.exec_cmd(fileManager))
hl.bind(mod .. " + B",          hl.dsp.exec_cmd(browser))
hl.bind(mod .. " + R",          hl.dsp.exec_cmd(menu))
hl.bind(mod .. " + SPACE",      hl.dsp.exec_cmd(menu))
hl.bind(mod .. " + F1",         hl.dsp.exec_cmd("hypr-el-keys"))
hl.bind(mod .. " + L",          hl.dsp.exec_cmd(lock))
hl.bind(mod .. " + M",          hl.dsp.exec_cmd("command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()'"))
hl.bind(mod .. " + SHIFT + C",  hl.dsp.exec_cmd("hyprpicker -a -n"))
hl.bind(mod .. " + N",          hl.dsp.exec_cmd("makoctl dismiss -a"))
hl.bind(mod .. " + SHIFT + N",  hl.dsp.exec_cmd("makoctl restore"))
hl.bind(mod .. " + SHIFT + W",  hl.dsp.exec_cmd("pkill -SIGUSR1 waybar"))   -- show/hide bar

-- screenshots (saved to ~/Pictures/Screenshots and copied to the clipboard)
hl.bind("Print",                hl.dsp.exec_cmd("hypr-el-screenshot area"))
hl.bind("SHIFT + Print",        hl.dsp.exec_cmd("hypr-el-screenshot screen"))
hl.bind(mod .. " + Print",      hl.dsp.exec_cmd("hypr-el-screenshot window"))
hl.bind(mod .. " + SHIFT + S",  hl.dsp.exec_cmd("hypr-el-screenshot area"))

-- windows
hl.bind(mod .. " + C",          hl.dsp.window.close())
hl.bind(mod .. " + W",          hl.dsp.window.close())
hl.bind(mod .. " + F",          hl.dsp.window.fullscreen())
hl.bind(mod .. " + SHIFT + F",  hl.dsp.window.fullscreen({ mode = "maximized" }))
hl.bind(mod .. " + V",          hl.dsp.window.float({ action = "toggle" }))
hl.bind(mod .. " + SHIFT + V",  hl.dsp.window.center())
hl.bind(mod .. " + P",          hl.dsp.window.pseudo())
hl.bind(mod .. " + SHIFT + P",  hl.dsp.window.pin())
hl.bind(mod .. " + J",          hl.dsp.layout("togglesplit"))
hl.bind("ALT + Tab",            hl.dsp.window.cycle_next())

-- groups (tabs)
hl.bind(mod .. " + G",          hl.dsp.group.toggle())
hl.bind(mod .. " + Tab",        hl.dsp.group.next())
hl.bind(mod .. " + SHIFT + Tab",hl.dsp.group.prev())

-- focus / move / resize with arrows
for _, d in ipairs({ "left", "right", "up", "down" }) do
    hl.bind(mod .. " + " .. d,              hl.dsp.focus({ direction = d }))
    hl.bind(mod .. " + SHIFT + " .. d,      hl.dsp.window.move({ direction = d }))
end
hl.bind(mod .. " + CTRL + left",  hl.dsp.window.resize({ x = -40, y = 0,   relative = true }), { repeating = true })
hl.bind(mod .. " + CTRL + right", hl.dsp.window.resize({ x = 40,  y = 0,   relative = true }), { repeating = true })
hl.bind(mod .. " + CTRL + up",    hl.dsp.window.resize({ x = 0,   y = -40, relative = true }), { repeating = true })
hl.bind(mod .. " + CTRL + down",  hl.dsp.window.resize({ x = 0,   y = 40,  relative = true }), { repeating = true })

-- workspaces
for i = 1, 10 do
    local key = i % 10
    hl.bind(mod .. " + " .. key,          hl.dsp.focus({ workspace = i }))
    hl.bind(mod .. " + SHIFT + " .. key,  hl.dsp.window.move({ workspace = i }))
    hl.bind(mod .. " + ALT + " .. key,    hl.dsp.window.move({ workspace = i, follow = false }))
end
hl.bind(mod .. " + Page_Down",           hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mod .. " + Page_Up",             hl.dsp.focus({ workspace = "e-1" }))
hl.bind(mod .. " + mouse_down",           hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mod .. " + mouse_up",             hl.dsp.focus({ workspace = "e-1" }))

-- scratchpad
hl.bind(mod .. " + S",          hl.dsp.workspace.toggle_special("magic"))
hl.bind(mod .. " + ALT + S",    hl.dsp.window.move({ workspace = "special:magic" }))

-- mouse
hl.bind(mod .. " + mouse:272",  hl.dsp.window.drag(),   { mouse = true })
hl.bind(mod .. " + mouse:273",  hl.dsp.window.resize(), { mouse = true })

-- media and brightness keys (also work on the lock screen)
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

-- resize mode: SUPER+ALT+R, then arrows, Escape/Return to leave
hl.bind(mod .. " + ALT + R", hl.dsp.submap("resize"))
hl.define_submap("resize", function()
    hl.bind("right",  hl.dsp.window.resize({ x = 30,  y = 0,   relative = true }), { repeating = true })
    hl.bind("left",   hl.dsp.window.resize({ x = -30, y = 0,   relative = true }), { repeating = true })
    hl.bind("up",     hl.dsp.window.resize({ x = 0,   y = -30, relative = true }), { repeating = true })
    hl.bind("down",   hl.dsp.window.resize({ x = 0,   y = 30,  relative = true }), { repeating = true })
    hl.bind("escape", hl.dsp.submap("reset"))
    hl.bind("Return", hl.dsp.submap("reset"))
end)

--------------------------------
---- WINDOWS AND WORKSPACES ----
--------------------------------

hl.window_rule({ name = "suppress-maximize-events", match = { class = ".*" }, suppress_event = "maximize" })

hl.window_rule({
    name  = "fix-xwayland-drags",
    match = { class = "^$", title = "^$", xwayland = true, float = true, fullscreen = false, pin = false },
    no_focus = true,
})

-- small tools float, centred
hl.window_rule({
    name  = "float-tools",
    match = { class = "^(org.pulseaudio.pavucontrol|pavucontrol|nm-connection-editor|blueman-manager|hyprland-share-picker|hyprpwcenter|hyprsysteminfo|org.gnome.Calculator|xdg-desktop-portal-gtk)$" },
    float = true,
    size  = "900 600",
    center = true,
})

-- key binding cheat sheet
hl.window_rule({ name = "hypr-el-keys", match = { class = "^(hypr-el-keys)$" }, float = true, size = "1000 760", center = true })
hl.window_rule({ name = "hypr-el-tui",  match = { class = "^(hypr-el-nmtui|hypr-el-btop)$" }, float = true, size = "1100 720", center = true })

-- file chooser / dialogs
hl.window_rule({ name = "float-dialogs", match = { title = "^(Open File|Save File|Save As|Open Folder|File Upload|Datei öffnen|Datei speichern)(.*)$" }, float = true, center = true })

-- picture in picture
hl.window_rule({ name = "pip", match = { title = "^(Picture-in-Picture|Bild-im-Bild)$" }, float = true, pin = true, size = "640 360", move = "monitor_w-660 monitor_h-380" })

hl.window_rule({ name = "move-hyprland-run", match = { class = "hyprland-run" }, move = "20 monitor_h-120", float = true })

-- frosted glass behind the bar, notifications and launcher
hl.layer_rule({ name = "blur-waybar",   match = { namespace = "^waybar$" },        blur = true, ignore_alpha = 0.2 })
hl.layer_rule({ name = "blur-mako",     match = { namespace = "^notifications$" }, blur = true, ignore_alpha = 0.2 })
hl.layer_rule({ name = "blur-launcher", match = { namespace = "^hyprlauncher$" },  blur = true, ignore_alpha = 0.2 })
