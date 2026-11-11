%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprcursor
Version:        0.1.14
Release:        1%{?dist}
Summary:        Hyprland cursor format, library and utilities
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprcursor
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprlang-devel >= 0.4.2
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  tomlplusplus-devel

%description
The hyprland cursor format, library and utilities.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
Development files for %{name}.

%prep
%autosetup

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md docs/
%{_bindir}/hyprcursor-util
%{_libdir}/libhyprcursor.so.*

%files devel
%{_includedir}/hyprcursor.hpp
%{_includedir}/hyprcursor/
%{_libdir}/libhyprcursor.so
%{_libdir}/pkgconfig/hyprcursor.pc

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
