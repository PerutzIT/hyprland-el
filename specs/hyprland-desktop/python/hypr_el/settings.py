"""hyprland-el settings: defaults, loading and saving (~/.config/hypr-el/settings.json)."""
import copy
import glob
import json
import os

SHARE = os.environ.get("HYPR_EL_SHARE", "/usr/share/hypr-el")
CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
CACHE_HOME = os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
CFG_DIR = os.path.join(CONFIG_HOME, "hypr-el")
SETTINGS_FILE = os.path.join(CFG_DIR, "settings.json")
WALLPAPER_CACHE = os.path.join(CACHE_HOME, "hypr-el", "wallpapers")

DEFAULTS = {
    # appearance
    "theme": "tiefsee",
    "wallpaper": "",              # "" = the theme's own wallpaper, otherwise a file path
    "titlebars": True,
    "gaps_in": 4,
    "gaps_out": 10,
    "rounding": 8,
    "border_size": 2,
    "blur": True,
    "shadows": True,
    "animations": True,
    "active_opacity": 0.96,
    "inactive_opacity": 0.88,
    "terminal_opacity": 0.85,
    "desktop_icons": True,
    # windows / behaviour
    "layout": "dwindle",          # dwindle | master | scrolling
    "float_new_windows": False,
    "focus_follows_mouse": True,
    # bar
    "bar_position": "top",        # top | bottom
    "bar_taskbar": True,
    "clock_24h": True,
    "clock_seconds": False,
    # input
    "kb_layouts": [],             # [] = detect from GNOME / localectl
    "kb_variants": [],
    "numlock": True,
    "mouse_sensitivity": 0.0,
    "mouse_natural_scroll": False,
    "touchpad_natural_scroll": True,
    "tap_to_click": True,
    # monitors: { "DP-1": {"mode": "2560x1440@144", "scale": "1"} }
    "monitors": {},
    # power (minutes, 0 = never)
    "idle_dim": 4,
    "idle_lock": 5,
    "idle_screen_off": 6,
    "idle_suspend": 0,
    # apps
    "terminal": "kitty",
    "file_manager": "nautilus",
    "browser": "firefox",
}


def load():
    s = copy.deepcopy(DEFAULTS)
    try:
        with open(SETTINGS_FILE) as f:
            user = json.load(f)
        if isinstance(user, dict):
            s.update({k: v for k, v in user.items() if k in DEFAULTS})
    except (OSError, ValueError):
        pass
    return s


def save(s):
    os.makedirs(CFG_DIR, exist_ok=True)
    diff = {k: v for k, v in s.items() if k in DEFAULTS and v != DEFAULTS[k]}
    tmp = SETTINGS_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(diff, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, SETTINGS_FILE)


def themes():
    out = {}
    files = sorted(glob.glob(os.path.join(SHARE, "themes", "*.json")),
                   key=lambda f: (os.path.basename(f) != DEFAULTS["theme"] + ".json", f))
    for f in files:
        try:
            with open(f) as fh:
                t = json.load(fh)
            out[t["id"]] = t
        except (OSError, ValueError, KeyError):
            continue
    return out


def theme(s):
    ts = themes()
    return ts.get(s.get("theme")) or ts.get(DEFAULTS["theme"]) or next(iter(ts.values()))
