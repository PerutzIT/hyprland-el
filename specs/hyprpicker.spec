%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprpicker
Version:        0.4.8
Release:        1%{?dist}
Summary:        Wlroots-compatible Wayland color picker
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpicker
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprwayland-scanner >= 0.4.0
BuildRequires:  hyprutils-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.37
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(libjpeg)
Recommends:     wl-clipboard

%description
A wlroots-compatible Wayland color picker that does not suck.

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
%{_bindir}/hyprpicker
%{_mandir}/man1/hyprpicker.1*

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
