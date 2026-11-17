Name:           hyprland-desktop
Version:        2.1.0
Release:        1%{?dist}
Summary:        Complete, preconfigured Hyprland desktop for Enterprise Linux
License:        MIT
URL:            https://github.com/PerutzIT/hyprland-el
# Generated from specs/hyprland-desktop/ by .copr/Makefile or scripts/build-one.sh
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  librsvg2-tools
BuildRequires:  python3

# compositor and hypr ecosystem
Requires:       hyprland
Requires:       hyprland-plugins
Requires:       xdg-desktop-portal-hyprland
Requires:       xdg-desktop-portal-gtk
Requires:       hyprpaper
Requires:       hypridle
Requires:       hyprlock
Requires:       hyprpolkitagent
Requires:       hyprlauncher
Requires:       hyprland-guiutils
Requires:       hyprshutdown
Requires:       hyprpicker
Requires:       hyprsunset
# bar, notifications, screenshots, clipboard, media
Requires:       waybar
Requires:       mako
Requires:       libnotify
Requires:       grim
Requires:       slurp
Requires:       wl-clipboard
Requires:       jq
Requires:       playerctl
Requires:       brightnessctl
Requires:       pipewire
Requires:       wireplumber
Requires:       pipewire-pulseaudio
# terminal, toolkit integration, fonts, look
Requires:       kitty
Requires:       less
Requires:       glib2
Requires:       xdg-utils
Requires:       xdg-user-dirs
Requires:       qt6-qtwayland
Requires:       adwaita-icon-theme
Requires:       jetbrains-mono-fonts
Requires:       fontawesome-6-free-fonts
Requires:       fontawesome-6-brands-fonts
Requires:       polkit
Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       gtk3
Requires:       gtk-layer-shell
Requires:       librsvg2-tools
Requires:       procps-ng
Requires:       util-linux-core
Requires:       NetworkManager-tui

# small useful desktop applications, installed by default but removable
Recommends:     nautilus
Recommends:     firefox
Recommends:     pavucontrol
Recommends:     nm-connection-editor
Recommends:     btop

# optional, not installed by default (dnf install <name>):
# Qt theme integration, extra hypr tools, nicer icons
Suggests:       hyprqt6engine
Suggests:       hyprland-qt-support
Suggests:       hyprpwcenter
Suggests:       hyprsysteminfo
Suggests:       papirus-icon-theme
Suggests:       qt5-qtwayland

%description
Meta package and default configuration that turns the Hyprland compositor into
a complete, easy to use desktop:

- title bars with close / maximize / minimize buttons (hyprbars), windows can
  be moved by their title bar and resized at their borders
- real minimize: minimized windows are restored from the taskbar
- status bar with workspaces, taskbar, clock, tray, audio, network, battery
- "Tiefsee" glass look (translucent windows with blur, floating bar islands)
  plus seven more colour themes, each with a matching generated wallpaper
- desktop icons (home, trash, terminal, settings, ~/Desktop content)
- the "Hyprland-Einstellungen" app (SUPER+I) for theme, wallpaper, title bars,
  gaps, effects, layout, bar, keyboard, mouse, displays and power settings
- lock screen, idle handling, notifications, polkit agent, screen sharing,
  launcher, screenshots, clipboard and a key binding cheat sheet (SUPER+F1)

The configuration is installed system wide in /etc/xdg/hypr and is used by
every user who does not have an own ~/.config/hypr/hyprland.lua.

%prep
%autosetup -n %{name}

%build
PYTHONPATH=python python3 -I -c 'import sys; sys.path.insert(0, "python"); import json; from hypr_el import wallpapers; open("hypr-el-default.svg", "w").write(wallpapers.svg(json.load(open("themes/catppuccin-mocha.json"))))'
rsvg-convert -w 3840 -h 2160 hypr-el-default.svg -o hypr-el-default.png

%install
install -Dpm 0644 hypr/hyprland.lua    %{buildroot}%{_sysconfdir}/xdg/hypr/hyprland.lua
install -Dpm 0644 hypr/hyprpaper.conf  %{buildroot}%{_sysconfdir}/xdg/hypr/hyprpaper.conf
install -Dpm 0644 hypr/hypridle.conf   %{buildroot}%{_sysconfdir}/xdg/hypr/hypridle.conf
install -Dpm 0644 hypr/hyprlock.conf   %{buildroot}%{_sysconfdir}/xdg/hypr/hyprlock.conf
install -Dpm 0644 hypr/hyprtoolkit.conf %{buildroot}%{_sysconfdir}/xdg/hypr/hyprtoolkit.conf

install -dm 0755 %{buildroot}%{_datadir}/hypr-el/themes %{buildroot}%{_datadir}/hypr-el/python/hypr_el
install -pm 0644 themes/*.json          %{buildroot}%{_datadir}/hypr-el/themes/
install -pm 0644 python/hypr_el/*.py    %{buildroot}%{_datadir}/hypr-el/python/hypr_el/
install -pm 0644 keybindings.txt        %{buildroot}%{_datadir}/hypr-el/keybindings.txt

install -Dpm 0644 hypr-el-default.png %{buildroot}%{_datadir}/backgrounds/hypr-el/hypr-el-default.png
install -Dpm 0644 hypr-el-default.svg %{buildroot}%{_datadir}/backgrounds/hypr-el/hypr-el-default.svg
install -Dpm 0644 data/io.github.perutzit.HyprElSettings.desktop \
    %{buildroot}%{_datadir}/applications/io.github.perutzit.HyprElSettings.desktop

for f in bin/*; do
    install -Dpm 0755 "$f" %{buildroot}%{_bindir}/$(basename "$f")
done

%files
%dir %{_sysconfdir}/xdg/hypr
%config(noreplace) %{_sysconfdir}/xdg/hypr/hyprland.lua
%config(noreplace) %{_sysconfdir}/xdg/hypr/hyprpaper.conf
%config(noreplace) %{_sysconfdir}/xdg/hypr/hypridle.conf
%config(noreplace) %{_sysconfdir}/xdg/hypr/hyprlock.conf
%config(noreplace) %{_sysconfdir}/xdg/hypr/hyprtoolkit.conf
%{_datadir}/hypr-el/
%{_datadir}/backgrounds/hypr-el/
%{_datadir}/applications/io.github.perutzit.HyprElSettings.desktop
%{_bindir}/hypr-el-*

%changelog
* Tue Nov 17 2026 Hypr-EL <hypr-el@localhost> - 2.1.0-1
- New default theme "Tiefsee" (glass windows, blur, misty night wallpaper)
- Bar as floating islands; fix the clock format
- Title bar buttons larger, always coloured and labelled, on every window
- Desktop icons (hypr-el-desktop), smoother slide animations
- Settings: desktop icons and active window opacity

* Tue Nov 17 2026 Hypr-EL <hypr-el@localhost> - 2.0.0-1
- Usability rework: title bars with close/maximize/minimize (hyprbars),
  real minimize/restore via the taskbar, resize at window borders
- Calmer default look; seven colour themes with generated wallpapers
- New settings app "Hyprland-Einstellungen" (SUPER+I)
- Restore the GNOME window button layout emptied by 1.x

* Thu Nov 12 2026 Hypr-EL <hypr-el@localhost> - 1.0.0-3
- Slim down: Qt theme engine, Qt5, Papirus, Noto fonts, mpv and fastfetch are
  optional now (about 100 MB instead of about 380 MB on top of GNOME)

* Thu Nov 12 2026 Hypr-EL <hypr-el@localhost> - 1.0.0-2
- Keyboard layout: use the user's GNOME input sources first, then localectl,
  then the console keymap; ALT+SHIFT switches between several layouts

* Thu Nov 12 2026 Hypr-EL <hypr-el@localhost> - 1.0.0-1
- Initial release: complete preconfigured Hyprland desktop
