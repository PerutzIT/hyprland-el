Name:           playerctl
Version:        2.4.1
Release:        1%{?dist}
Summary:        MPRIS media player command-line controller and library
License:        LGPL-3.0-or-later
URL:            https://github.com/altdesktop/playerctl
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)

%description
Command-line utility and library for controlling media players that
implement the MPRIS D-Bus interface (used by media keys and waybar).

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
Development files for %{name}.

%prep
%autosetup

%build
%meson -Dgtk-doc=false -Dintrospection=true -Dbash-completions=true -Dzsh-completions=true
%meson_build

%install
%meson_install
rm -f %{buildroot}%{_libdir}/libplayerctl.a

%files
%license COPYING
%doc README.md CHANGELOG.md
%{_bindir}/playerctl
%{_bindir}/playerctld
%{_libdir}/libplayerctl.so.2*
%{_libdir}/girepository-1.0/Playerctl-2.0.typelib
%{_mandir}/man1/playerctl.1*
%{_datadir}/dbus-1/services/org.mpris.MediaPlayer2.playerctld.service
%{_datadir}/bash-completion/completions/playerctl.bash
%{_datadir}/zsh/site-functions/_playerctl

%files devel
%{_includedir}/playerctl/
%{_libdir}/libplayerctl.so
%{_libdir}/pkgconfig/playerctl.pc
%{_datadir}/gir-1.0/Playerctl-2.0.gir

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
