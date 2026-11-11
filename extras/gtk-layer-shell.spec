Name:           gtk-layer-shell
Version:        0.10.1
Release:        1%{?dist}
Summary:        Library to create desktop components for Wayland using the Layer Shell protocol
License:        LGPL-3.0-or-later AND MIT
URL:            https://github.com/wmww/gtk-layer-shell
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  vala
BuildRequires:  pkgconfig(gtk+-wayland-3.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)

%description
A library to write GTK 3 applications that use the Layer Shell protocol
(status bars, docks, notifications, ...) on Wayland compositors such as Hyprland.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
Development files for %{name}.

%prep
%autosetup

%build
%meson -Dexamples=false -Ddocs=false -Dtests=false
%meson_build

%install
%meson_install

%files
%license LICENSE_LGPL.txt LICENSE_MIT.txt
%doc README.md CHANGELOG.md
%{_libdir}/libgtk-layer-shell.so.0*
%{_libdir}/girepository-1.0/GtkLayerShell-0.1.typelib

%files devel
%{_includedir}/gtk-layer-shell/
%{_libdir}/libgtk-layer-shell.so
%{_libdir}/pkgconfig/gtk-layer-shell-0.pc
%{_datadir}/gir-1.0/GtkLayerShell-0.1.gir
%{_datadir}/vala/vapi/gtk-layer-shell-0.*

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
