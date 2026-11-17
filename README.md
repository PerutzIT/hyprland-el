# Hyprland for Enterprise Linux 10 (hypr-el)

RPM packaging of the complete [Hyprland](https://hypr.land) ecosystem for
**RHEL 10 and its rebuilds** (AlmaLinux 10, Rocky Linux 10, CentOS Stream 10).

Every package is the **unmodified upstream release**. Changes were made only where
EL10 is missing something, and each one is a small, documented patch that does nothing
on a newer toolchain (see [Patches](#el10-patches)).

## What you get

| Layer | Packages |
|---|---|
| EL10 base updates | `wayland-protocols` 1.50, `libxkbcommon` 1.13.2 (ABI-compatible update), `lua5.5` (parallel to the system Lua 5.4), `muparser`, `glaze` |
| Hypr libraries | `hyprutils`, `hyprlang`, `hyprcursor`, `hyprgraphics`, `hyprwayland-scanner`, `hyprland-protocols`, `hyprwire`, `aquamarine`, `hyprtoolkit` |
| Compositor | `hyprland` 0.57.2 (Hyprland, hyprctl, hyprpm, start-hyprland), `hyprland-devel` (plugin headers), `hyprland-plugins` (official plugins: hyprbars, hyprfocus, borders-plus-plus, csgo-vulkan-fix) |
| Ecosystem | `xdg-desktop-portal-hyprland`, `hyprpaper`, `hypridle`, `hyprlock`, `hyprsunset`, `hyprpicker`, `hyprlauncher`, `hyprpolkitagent`, `hyprland-guiutils`, `hyprshutdown`, `hyprpwcenter`, `hyprsysteminfo`, `hyprland-qt-support`, `hyprqt6engine` |
| Extras (not in EPEL) | `waybar`, `gtk-layer-shell`, `mako`, `grim`, `slurp`, `playerctl`, `brightnessctl` |
| Complete desktop | `hyprland-desktop`: meta package, ready-to-use configuration, 7 themes, settings app |

Everything else (kitty, dolphin, wl-clipboard, pipewire, qt6-qtwayland, …) comes
from AlmaLinux, CRB and EPEL.

## Toolchain

Hyprland ≥ 0.57 needs C++26, which the EL10 system GCC 14 does not support.
The C++ packages are therefore built with **gcc-toolset-15** through the EL10
`%{?enable_gcctoolset15}` macro. The resulting binaries link only against the
system `libstdc++.so.6`, because gcc-toolset links newer symbols in statically.
So gcc-toolset is **not** needed at runtime.

`hyprpm` builds plugins on the user's machine, so `/usr/bin/hyprpm` is a small
wrapper that turns on gcc-toolset-15 before it runs the real binary in
`/usr/libexec/hyprland/hyprpm`. `hyprland-devel` pulls in everything plugin
builds need.

## Plugins

The official plugins from [hyprwm/hyprland-plugins](https://github.com/hyprwm/hyprland-plugins)
are packaged as `hyprland-plugins` (built against the exact `hyprland` package, installed to
`/usr/lib64/hyprland/plugins/`). Load one in the Lua config with
`hl.plugin.load("/usr/lib64/hyprland/plugins/hyprbars.so")`.

Any other plugin is installed the usual way with **hyprpm**. Nothing EL-specific is needed:

```bash
sudo dnf install hyprland-devel          # compiler, cmake/meson, all headers
hyprpm update                            # fetches Hyprland headers for the exact running commit
hyprpm add https://github.com/hyprwm/hyprland-plugins
hyprpm enable hyprbars
hyprpm reload
```

Add `hyprpm reload -n` to your autostart so plugins load on login.

Our build reports the exact upstream commit (`hyprctl version`), so `hyprpm`
picks up the same headers and commit pins as on any other distribution.
`/usr/bin/hyprpm` is a small wrapper that does two things. It turns on gcc-toolset-15,
because plugins are C++26. It also adds `/usr/include/lua5.5` to the include path,
because Hyprland's headers include `<lua.h>` without declaring Lua in `hyprland.pc`.
On EL, Lua 5.5 lives in its own directory next to the system Lua 5.4. For manual
builds, `hyprland-devel` adds `lua5.5` to the installed `hyprland.pc`.

Verified on AlmaLinux 10.2:
- All official `hyprwm/hyprland-plugins` (hyprbars, borders-plus-plus, hyprfocus,
  csgo-vulkan-fix) build through the hyprpm flow and load into the running compositor.
- All plugins listed in
  [awesome-hyprland](https://github.com/hyprland-community/awesome-hyprland#plugins)
  ship a `hyprpm.toml`, and a source scan found no C++ features that need GCC 16.
  Whether a given plugin works with Hyprland 0.57 depends on its upstream
  maintenance, just as on any other distribution.

## EL10 patches

| Package | Patch | Reason |
|---|---|---|
| hyprland | `hyprland-0001-libstdcxx15-compat.patch` | `std::ranges::starts_with` and `std::string::subview` are libstdc++ 16 features. The patch adds equivalent code behind a feature-test macro. |
| hyprtoolkit | `hyprtoolkit-0001-pango-1.54-compat.patch` | `PANGO_WRAP_NONE` needs Pango 1.56 (EL10 has 1.54). It is emulated with a single-line layout height, behind `PANGO_VERSION_CHECK`. |
| hyprsysteminfo | `hyprsysteminfo-0001-pciutils-extern-c.patch` | pciutils 3.13 `pci.h` has no `extern "C"` guards. |

Spec-level adjustments:
- `hyprtoolkit`: EL10 `iniparser-devel` ships no `.pc` file. The spec provides one at build time and uses `-liniparser` in `hyprtoolkit.pc`.
- `hyprqt6engine`: Qt 6.10 requires `GuiPrivate`/`WidgetsPrivate` to be requested explicitly.
- `hyprland`: the systemd user unit is moved from `lib64/` to `/usr/lib/systemd/user`, the build uses `NO_UWSM` because uwsm is not packaged for EL10, and `lua5.5` is added to the `Requires` of `hyprland.pc` (see [Plugins](#plugins)).
- `waybar`: bundles spdlog 1.15.2 statically through an offline meson wrap, because EPEL has 1.14.

## Binary packages (Fedora COPR)

Prebuilt packages for `epel-10-x86_64` (RHEL 10, AlmaLinux 10, Rocky Linux 10)
are built by Fedora COPR directly from this repository
([perutzit/hyprland-el](https://copr.fedorainfracloud.org/coprs/perutzit/hyprland-el/)):

```bash
sudo dnf install epel-release
sudo dnf config-manager --set-enabled crb
sudo dnf copr enable perutzit/hyprland-el
sudo dnf install hyprland-desktop     # complete desktop with settings app (or just: hyprland)
```

Maintainers: `./scripts/copr-submit.sh` creates or updates the COPR project and
submits every package in dependency order. It needs `copr-cli` and an API token in
`~/.config/copr`. COPR builds each SRPM itself from the public git checkout
(`.copr/Makefile`, method `make_srpm`).

## Building

```bash
git clone https://github.com/PerutzIT/hyprland-el.git && cd hyprland-el
sudo ./scripts/build-all.sh          # core + extras, ~30-40 min on 20 threads
sudo ./scripts/build-all.sh --core   # only Hyprland + hypr ecosystem
```

The script enables EPEL and CRB, installs the toolchain, builds every spec in
dependency order, installs each layer and publishes a local dnf repository in
`repo/el10` (configured as `/etc/yum.repos.d/hypr-el-local.repo`).

Build a single package: `./scripts/build-one.sh specs/<name>.spec [--install]`

All specs build in a clean `mock` chroot (`alma+epel-10-x86_64`, network
disabled during the build), for example:

```bash
mock -r alma+epel-10-x86_64 --chain --localrepo=/tmp/hypr-chain <SRPMs in build-all.sh order>
```

## Installing / using

```bash
sudo dnf install hyprland-desktop
```

Then pick **Hyprland** in the GDM session menu (gear icon after selecting the user) and log in
as a normal user. Everything is preconfigured:

- **Windows behave as expected:** every window has a title bar with close, maximize and
  minimize buttons (hyprbars). Drag the title bar to move a window, drag the border to resize,
  double-click the title bar to maximize. GTK4/libadwaita apps (Nautilus, …) keep their own
  header bar. Windows are tiled by default; *Settings → Fenster & Leiste → Klassischer Modus*
  makes new windows float like on other desktops.
- **Minimize really works:** minimized windows disappear and come back from the taskbar
  (click), with SUPER+SHIFT+H, or from notifications. Hyprland itself has no minimized state;
  hyprland-desktop keeps them on a hidden special workspace.
- **Bar:** launcher, workspaces, taskbar, clock with calendar, tray, media, volume, brightness,
  network, battery, settings and power menu.
- **Settings app "Hyprland-Einstellungen"** (SUPER+I or the gear in the bar): theme, wallpaper
  (own images too), title bars, gaps, rounding, borders, blur, shadows, animations, transparency,
  window layout, bar position/taskbar/clock, keyboard layouts, mouse and touchpad, display
  resolution and scale (with automatic revert), idle/lock/suspend times, default apps.
  Changes apply immediately.
- **Themes:** Catppuccin Mocha (default) and Latte, Tokyo Night, Nord, Gruvbox Dark, Rosé Pine,
  Everforest – each colours windows, bar, notifications, terminal, lock screen, launcher and
  GTK apps, and comes with its own generated wallpaper. SUPER+SHIFT+T cycles through them.
- Lock screen, idle handling, notifications, polkit agent, screen sharing portal, screenshots,
  clipboard, media keys. **SUPER+F1** shows all key bindings.

On top of an existing GNOME installation this is about 45 packages / 15 MB download.
Optional extras: `sudo dnf install hyprqt6engine hyprland-qt-support qt5-qtwayland papirus-icon-theme`.

How the configuration is organised:

| File | Role |
|---|---|
| `/etc/xdg/hypr/hyprland.lua` | system-wide Hyprland config, reads the user's settings |
| `~/.config/hypr-el/settings.json` | the user's settings (written by the settings app) |
| `~/.config/hypr-el/*` | configs generated from the settings (bar, notifications, lock, idle, wallpaper, terminal) |
| `~/.config/hypr/hyprland.lua`, `~/.config/waybar/…`, `~/.config/mako/config`, `~/.config/kitty/kitty.conf` | if present, a user's own files take precedence |

`hypr-el-setup --copy` copies the full Hyprland config to `~/.config/hypr/hyprland.lua` for hand
editing; `hypr-el-setup --reset` returns to the defaults (backups are kept).
Hyprland 0.57 uses **Lua** for its configuration; LuaLS stubs are in `/usr/share/hypr/stubs/`.

## License

The spec files and patches in this repository are MIT licensed. The packaged
software keeps its own upstream licenses.
