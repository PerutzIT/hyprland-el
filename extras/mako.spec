Name:           mako
Version:        1.11.0
Release:        1%{?dist}
Summary:        Lightweight Wayland notification daemon
License:        MIT
URL:            https://github.com/emersion/mako
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  scdoc
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
Provides:       desktop-notification-daemon

%description
mako is a lightweight notification daemon for Wayland compositors.

%prep
%autosetup

%build
%meson -Dsd-bus-provider=libsystemd -Dicons=enabled -Dman-pages=enabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/mako
%{_bindir}/makoctl
%{_mandir}/man1/mako*.1*
%{_mandir}/man5/mako.5*
%{_datadir}/dbus-1/services/fr.emersion.mako.service

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
