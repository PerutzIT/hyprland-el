%global spdlog_ver 1.15.2
%global spdlog_wrap 1.15.2-3

Name:           waybar
Version:        0.16.0
Release:        1%{?dist}
Summary:        Highly customizable Wayland bar for Sway and Hyprland
License:        MIT AND BSD-3-Clause
URL:            https://github.com/Alexays/Waybar
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# EPEL10 only has spdlog 1.14; waybar needs >= 1.15.2 -> bundled (static) via meson wrap, offline
Source1:        https://github.com/gabime/spdlog/archive/refs/tags/v%{spdlog_ver}.tar.gz#/spdlog-%{spdlog_ver}.tar.gz
Source2:        https://wrapdb.mesonbuild.com/v2/spdlog_%{spdlog_wrap}/get_patch#/spdlog_%{spdlog_wrap}_patch.zip

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(fmt) >= 8.1.1
BuildRequires:  pkgconfig(gtkmm-3.0)
BuildRequires:  pkgconfig(giomm-2.4)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(sigc++-2.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0) >= 0.9.0
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbregistry)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(playerctl) >= 2.0.0
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  unzip
Provides:       bundled(spdlog) = %{spdlog_ver}
Recommends:     fontawesome-fonts-all
Recommends:     (pavucontrol or hyprpwcenter)

%description
Highly customizable Wayland bar for Sway and wlroots/Hyprland based
compositors, with a native Hyprland module (workspaces, window title, ...).

%prep
%autosetup -n Waybar-%{version}
mkdir -p subprojects/packagecache
cp %{SOURCE1} %{SOURCE2} subprojects/packagecache/

%build
%meson --wrap-mode=nodownload --force-fallback-for=spdlog \
       -Dspdlog:default_library=static -Dspdlog:tests=disabled -Dspdlog:std_format=disabled \
       -Dexperimental=true -Dtests=disabled -Dman-pages=enabled \
       -Dmpd=disabled -Dsndio=disabled -Djack=disabled -Dcava=disabled \
       -Dwireplumber=disabled -Dgps=disabled -Dwwan=disabled
%meson_build

%install
%meson_install
# don't ship the bundled static spdlog
rm -rf %{buildroot}%{_includedir}/spdlog %{buildroot}%{_libdir}/libspdlog.a %{buildroot}%{_libdir}/pkgconfig/spdlog.pc

%files
%license LICENSE
%doc README.md
%{_bindir}/waybar
%dir %{_sysconfdir}/xdg/waybar
%config(noreplace) %{_sysconfdir}/xdg/waybar/config.jsonc
%config(noreplace) %{_sysconfdir}/xdg/waybar/style.css
%{_mandir}/man5/waybar*.5*
%{_userunitdir}/waybar.service

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
