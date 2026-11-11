%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprland-guiutils
Version:        0.2.2
Release:        1%{?dist}
Summary:        Hyprland GUI utilities (dialogs, welcome app, donate screen, update screen)
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-guiutils
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprlang-devel >= 0.6.0
BuildRequires:  hyprutils-devel >= 0.10.2
BuildRequires:  hyprtoolkit-devel >= 0.4.0
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)
Obsoletes:      hyprland-qtutils < 0.2

%description
Hyprland GUI utilities (successor of hyprland-qtutils): hyprland-dialog,
hyprland-welcome, hyprland-donate-screen, hyprland-update-screen, ...

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
%{_bindir}/hyprland-*

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
