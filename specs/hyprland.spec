%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

%global commit      11cbc6c577b84ffb1edf4df3fc5b6128c3ae6947
%global commit_date Mon Nov 09 2026

Name:           hyprland
Version:        0.57.2
Release:        3%{?dist}
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks
# Hyprland: BSD-3-Clause; bundled udis86: BSD-2-Clause
License:        BSD-3-Clause AND BSD-2-Clause
URL:            https://github.com/hyprwm/Hyprland
Source0:        %{url}/releases/download/v%{version}/source-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        hyprpm-wrapper.sh
# EL10: gcc-toolset-15 libstdc++ lacks two C++26 features used upstream (GCC 16)
Patch0:         hyprland-0001-libstdcxx15-compat.patch

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake >= 3.30
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  git-core

BuildRequires:  aquamarine-devel >= 0.15.0
BuildRequires:  hyprcursor-devel >= 0.1.7
BuildRequires:  hyprgraphics-devel >= 0.5.1
BuildRequires:  hyprlang-devel >= 0.6.7
BuildRequires:  hyprutils-devel >= 0.14.3
BuildRequires:  hyprwire-devel
BuildRequires:  hyprland-protocols-devel >= 0.8.0
BuildRequires:  hyprwayland-scanner >= 0.3.10
BuildRequires:  glaze-devel
BuildRequires:  lua5.5-devel
BuildRequires:  muparser-devel

BuildRequires:  pkgconfig(xkbcommon) >= 1.11.0
BuildRequires:  pkgconfig(wayland-server) >= 1.22.91
BuildRequires:  pkgconfig(wayland-protocols) >= 1.49
BuildRequires:  pkgconfig(libinput) >= 1.29
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  libglvnd-devel
BuildRequires:  glslang-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  systemd-rpm-macros

Requires:       xorg-x11-server-Xwayland
Requires:       aquamarine%{?_isa} >= 0.15.0
Requires:       hyprcursor%{?_isa} >= 0.1.7
Requires:       hyprgraphics%{?_isa} >= 0.5.1
Requires:       hyprutils%{?_isa} >= 0.14.3
Requires:       libxkbcommon%{?_isa} >= 1.11.0
# default apps of the example config & ecosystem
Recommends:     xdg-desktop-portal-hyprland
Recommends:     xdg-desktop-portal-gtk
Recommends:     kitty
Recommends:     hyprlauncher
Recommends:     hyprpolkitagent
Recommends:     hyprland-guiutils
Recommends:     qt6-qtwayland
Recommends:     polkit
Recommends:     (hyprland-devel if git-core)

Provides:       bundled(udis86) = 1.7.2

%description
Hyprland is a dynamic tiling Wayland compositor based on aquamarine that
doesn't sacrifice on its looks. It supports multiple layouts, fancy effects,
has a very flexible IPC model allowing for a lot of customization, a
powerful plugin system and more.

This build is the unmodified upstream release, compiled for Enterprise Linux
(RHEL / AlmaLinux / Rocky) with gcc-toolset-15.

%package devel
Summary:        Header and protocol files for Hyprland plugin development
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{toolset}-gcc-c++
Requires:       %{toolset}-runtime
Requires:       cmake meson ninja-build make git-core pkgconfig cpio
Requires:       aquamarine-devel hyprcursor-devel hyprgraphics-devel hyprlang-devel
Requires:       hyprutils-devel hyprwire-devel hyprland-protocols-devel glaze-devel
Requires:       lua5.5-devel muparser-devel libxkbcommon-devel wayland-devel
Requires:       pkgconfig(pixman-1) pkgconfig(libdrm) pkgconfig(libinput)
Requires:       pkgconfig(pangocairo) pkgconfig(re2) pkgconfig(lcms2)
Requires:       pkgconfig(egl) pkgconfig(glesv2) libglvnd-devel

%description devel
Header and protocol files needed to build Hyprland plugins (e.g. with hyprpm).

%prep
%autosetup -p1 -n hyprland-source

%build
export GIT_COMMIT_HASH=%{commit}
export GIT_BRANCH=v%{version}
export GIT_TAG=v%{version}
export GIT_COMMIT_MESSAGE="VERSION: bump to %{version}"
export GIT_COMMIT_DATE="%{commit_date}"
export GIT_DIRTY=clean
export GIT_COMMITS=0
# uwsm is not available on EL10 -> don't ship a session entry that cannot start
%cmake -DCMAKE_BUILD_TYPE=Release -DNO_TESTS=ON -DBUILD_TESTING=OFF -DNO_UWSM=ON
%cmake_build

%install
%cmake_install
# hyprpm needs a C++26 compiler to build plugins -> wrap it so it uses gcc-toolset-15
install -d %{buildroot}%{_libexecdir}/hyprland
mv %{buildroot}%{_bindir}/hyprpm %{buildroot}%{_libexecdir}/hyprland/hyprpm
install -Dm755 %{SOURCE1} %{buildroot}%{_bindir}/hyprpm
# headers include <lua.h> but hyprland.pc doesn't declare Lua; on EL Lua 5.5 is in its own include dir
sed -i -e 's/^Requires: \(.*\)$/Requires: \1, lua5.5/' %{buildroot}%{_datadir}/pkgconfig/hyprland.pc
# upstream uses CMAKE_INSTALL_LIBDIR (lib64), systemd only searches /usr/lib/systemd/user
if [ -d %{buildroot}%{_libdir}/systemd/user ]; then
  install -d %{buildroot}%{_userunitdir}
  mv %{buildroot}%{_libdir}/systemd/user/* %{buildroot}%{_userunitdir}/
  rm -rf %{buildroot}%{_libdir}/systemd
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_bindir}/start-hyprland
%{_libexecdir}/hyprland/
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_userunitdir}/hyprland-session.target
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*
%{_datadir}/bash-completion/completions/hyprpm
%{_datadir}/fish/vendor_completions.d/hyprpm.fish
%{_datadir}/zsh/site-functions/_hyprpm

%files devel
%{_includedir}/hyprland/
%{_datadir}/pkgconfig/hyprland.pc

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 0.57.2-3
- Plugin builds: add lua5.5 to hyprland.pc Requires and the hyprpm wrapper include path

* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 0.57.2-2
- Build with NO_UWSM (uwsm not available on EL10), avoids a broken GDM session entry

* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 0.57.2-1
- Initial package for EL10 (upstream v0.57.2, unmodified)
