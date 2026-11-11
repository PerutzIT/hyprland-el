%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprwire
Version:        0.3.1
Release:        1%{?dist}
Summary:        Fast and consistent wire protocol for IPC
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwire
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprutils-devel >= 0.9.0
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(pugixml)

%description
A fast and consistent wire protocol for IPC, used by Hyprland and hyprctl.

%package devel
Summary:        Development files and scanner for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
Development files and hyprwire-scanner for %{name}.

%prep
%autosetup

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprwire.so.*

%files devel
%{_bindir}/hyprwire-scanner
%{_includedir}/hyprwire/
%{_libdir}/libhyprwire.so
%{_libdir}/pkgconfig/hyprwire*.pc
%{_libdir}/cmake/hyprwire-scanner/

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
