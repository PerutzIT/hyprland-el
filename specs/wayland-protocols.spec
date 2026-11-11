# Based on the AlmaLinux 10 wayland-protocols spec, updated for Hyprland
%global debug_package %{nil}

Name:           wayland-protocols
Version:        1.50
Release:        1.hypr%{?dist}
Summary:        Wayland protocols that adds functionality not available in the core protocol
License:        MIT
URL:            https://wayland.freedesktop.org/
Source0:        https://gitlab.freedesktop.org/wayland/%{name}/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  wayland-devel

%description
wayland-protocols contains Wayland protocols that adds functionality not
available in the Wayland core protocol.

%package devel
Summary:        Wayland protocols that adds functionality not available in the core protocol
Provides:       %{name}-static = %{version}-%{release}
BuildArch:      noarch

%description devel
wayland-protocols contains Wayland protocols that adds functionality not
available in the Wayland core protocol.

%prep
%autosetup

%build
%meson -Dtests=false
%meson_build

%install
%meson_install

%files devel
%license COPYING
%doc README.md
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/%{name}/
%{_includedir}/%{name}/

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 1.50-1.hypr
- Update to 1.50 (required by Hyprland >= 0.57)
