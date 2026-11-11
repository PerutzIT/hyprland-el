%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprsunset
Version:        0.4.0
Release:        1%{?dist}
Summary:        Blue light filter for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprsunset
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprwayland-scanner >= 0.4.0
BuildRequires:  hyprland-protocols-devel >= 0.4.0
BuildRequires:  hyprlang-devel
BuildRequires:  hyprutils-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  systemd-rpm-macros

%description
An application to enable a blue-light filter on Hyprland.

%prep
%autosetup

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
# some projects install user units into lib64 or the wrong prefix
if [ -d %{buildroot}%{_libdir}/systemd/user ]; then install -d %{buildroot}%{_userunitdir}; mv %{buildroot}%{_libdir}/systemd/user/* %{buildroot}%{_userunitdir}/; rm -rf %{buildroot}%{_libdir}/systemd; fi

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprsunset
%{_userunitdir}/hyprsunset.service

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
