%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprpaper
Version:        0.8.5
Release:        1%{?dist}
Summary:        Blazing fast wallpaper utility for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpaper
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprwayland-scanner >= 0.4.0
BuildRequires:  hyprlang-devel >= 0.6.0
BuildRequires:  hyprutils-devel
BuildRequires:  hyprtoolkit-devel >= 0.4.1
BuildRequires:  hyprwire-devel
BuildRequires:  hyprgraphics-devel
BuildRequires:  aquamarine-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  systemd-rpm-macros

%description
Hyprpaper is a blazing fast wayland wallpaper utility with IPC controls.

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
%{_bindir}/hyprpaper
%{_userunitdir}/hyprpaper.service

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
