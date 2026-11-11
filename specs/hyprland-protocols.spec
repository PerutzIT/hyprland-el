%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprland-protocols
Version:        0.8.0
Release:        1%{?dist}
Summary:        Wayland protocol extensions for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-protocols
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildArch:      noarch
%global debug_package %{nil}

%description
Wayland protocol extensions for Hyprland.

%package devel
Summary:        Wayland protocol extensions for Hyprland
%description devel
Wayland protocol extensions for Hyprland (XML files and pkg-config).

%prep
%autosetup

%build
%cmake
%cmake_build

%install
%cmake_install

%files devel
%license LICENSE
%doc README.md
%{_datadir}/hyprland-protocols/
%{_datadir}/pkgconfig/hyprland-protocols.pc

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
