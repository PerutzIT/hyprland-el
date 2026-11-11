%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprwayland-scanner
Version:        0.4.6
Release:        1%{?dist}
Summary:        Hyprland implementation of wayland-scanner, in and for C++
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwayland-scanner
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(pugixml)

%description
A Hyprland implementation of wayland-scanner, in and for C++.

%prep
%autosetup

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprwayland-scanner
%{_libdir}/pkgconfig/hyprwayland-scanner.pc
%{_libdir}/cmake/hyprwayland-scanner/

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
