# Based on the AlmaLinux 10 libxkbcommon spec, updated for Hyprland
Name:           libxkbcommon
Version:        1.13.2
Release:        1.hypr%{?dist}
Summary:        X.Org X11 XKB parsing library
License:        MIT AND X11 AND MIT-CMU
URL:            https://xkbcommon.org
Source0:        https://github.com/xkbcommon/libxkbcommon/archive/xkbcommon-%{version}/%{name}-xkbcommon-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  byacc flex bison
BuildRequires:  xorg-x11-proto-devel libX11-devel
BuildRequires:  pkgconfig(wayland-client) pkgconfig(wayland-protocols)
BuildRequires:  wayland-devel
BuildRequires:  xkeyboard-config-devel
BuildRequires:  pkgconfig(xcb-xkb) >= 1.10
BuildRequires:  libxml2-devel
BuildRequires:  python3

Requires:       xkeyboard-config

%description
%{name} is the X.Org library for compiling XKB maps into formats usable by
the X Server or other display servers.

%package devel
Summary:        X.Org X11 XKB parsing development package
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
X.Org X11 XKB parsing development package

%package x11
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description x11
%{name}-x11 is the X.Org library for creating keymaps by querying the X server.

%package x11-devel
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}-x11%{?_isa} = %{version}-%{release}
%description x11-devel
X.Org X11 XKB keymap creation library development package

%package utils
Summary:        X.Org X11 XKB parsing utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description utils
%{name}-utils is a set of utilities to analyze and test XKB parsing.

%package x11-utils
Summary:        X.Org X11 XKB parsing utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-x11%{?_isa} = %{version}-%{release}
Requires:       %{name}-utils%{?_isa} = %{version}-%{release}
%description x11-utils
%{name}-x11-utils is a set of X11 utilities to analyze and test XKB parsing.

%prep
%autosetup -n %{name}-xkbcommon-%{version}

%build
%meson -Denable-docs=false -Denable-x11=true -Denable-wayland=true
%meson_build

%install
%meson_install

%files
%license LICENSE
%{_libdir}/libxkbcommon.so.0*
%{_libdir}/libxkbregistry.so.0*

%files devel
%{_libdir}/libxkbcommon.so
%{_libdir}/libxkbregistry.so
%dir %{_includedir}/xkbcommon/
%exclude %{_includedir}/xkbcommon/xkbcommon-x11.h
%{_includedir}/xkbcommon/*.h
%{_libdir}/pkgconfig/xkbcommon.pc
%{_libdir}/pkgconfig/xkbregistry.pc

%files x11
%{_libdir}/libxkbcommon-x11.so.0*

%files x11-devel
%{_libdir}/libxkbcommon-x11.so
%{_includedir}/xkbcommon/xkbcommon-x11.h
%{_libdir}/pkgconfig/xkbcommon-x11.pc

%files utils
%{_bindir}/xkbcli
%dir %{_libexecdir}/xkbcommon
%exclude %{_libexecdir}/xkbcommon/xkbcli-interactive-x11
%{_libexecdir}/xkbcommon/*
%exclude %{_mandir}/man1/xkbcli-interactive-x11.1*
%{_mandir}/man1/xkbcli*.1*
%{_datadir}/bash-completion/completions/xkbcli

%files x11-utils
%{_libexecdir}/xkbcommon/xkbcli-interactive-x11
%{_mandir}/man1/xkbcli-interactive-x11.1*

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 1.13.2-1.hypr
- Update to 1.13.2 (Hyprland requires >= 1.11), ABI compatible (soname .0)
