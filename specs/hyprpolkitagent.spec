%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprpolkitagent
Version:        0.2.0
Release:        1%{?dist}
Summary:        Polkit authentication agent for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpolkitagent
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprutils-devel
BuildRequires:  hyprtoolkit-devel
BuildRequires:  hyprgraphics-devel
BuildRequires:  hyprlang-devel
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(sdbus-c++) >= 2
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  systemd-rpm-macros
Requires:       polkit

%description
A simple polkit authentication agent for Hyprland, written with hyprtoolkit.

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
%{_libexecdir}/hyprpolkitagent
%{_userunitdir}/hyprpolkitagent.service
%{_datadir}/dbus-1/services/org.hyprland.hyprpolkitagent.service

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
