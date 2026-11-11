%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           xdg-desktop-portal-hyprland
Version:        1.5.0
Release:        1%{?dist}
Summary:        xdg-desktop-portal backend for Hyprland (screen sharing, screenshots, global shortcuts)
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/xdg-desktop-portal-hyprland
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprwayland-scanner >= 0.4.2
BuildRequires:  hyprland-protocols-devel >= 0.8.0
BuildRequires:  hyprlang-devel >= 0.2.0
BuildRequires:  hyprutils-devel >= 0.2.6
BuildRequires:  hyprtoolkit-devel >= 0.6.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.39
BuildRequires:  pkgconfig(libpipewire-0.3) >= 1.1.82
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0.0
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  libglvnd-devel
BuildRequires:  systemd-rpm-macros
Requires:       xdg-desktop-portal
Requires:       pipewire
Recommends:     hyprland-guiutils
Recommends:     slurp
Recommends:     grim
Enhances:       hyprland

%description
xdg-desktop-portal backend for Hyprland: screen sharing (PipeWire),
screenshots, global shortcuts and the screen/window share picker.

%prep
%autosetup

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
# some projects install user units into lib64 or the wrong prefix
if [ -d %{buildroot}%{_libdir}/systemd/user ]; then install -d %{buildroot}%{_userunitdir}; mv %{buildroot}%{_libdir}/systemd/user/* %{buildroot}%{_userunitdir}/; rm -rf %{buildroot}%{_libdir}/systemd; fi

%post
%systemd_user_post %{name}.service
%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%doc README.md
%{_libexecdir}/xdg-desktop-portal-hyprland
%{_bindir}/hyprland-share-picker
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_userunitdir}/xdg-desktop-portal-hyprland.service

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
