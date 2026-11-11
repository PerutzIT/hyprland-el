%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprland-qt-support
Version:        0.1.0
Release:        1%{?dist}
Summary:        Qt6 QML style provider for Hypr* apps
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-qt-support
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprlang-devel >= 0.6.0
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  qt6-qtbase-private-devel

%description
A Qt6 QML style provider for Hypr* Qt apps.

%prep
%autosetup

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DINSTALL_QMLDIR=%{_qt6_qmldir}
%cmake_build

%install
%cmake_install
# upstream hardcodes lib/ for the backing libraries
if [ -d %{buildroot}%{_prefix}/lib ] && [ "%{_lib}" != "lib" ]; then mv %{buildroot}%{_prefix}/lib/libhyprland-quick-style*.so %{buildroot}%{_libdir}/; fi
# some projects install user units into lib64 or the wrong prefix
if [ -d %{buildroot}%{_libdir}/systemd/user ]; then install -d %{buildroot}%{_userunitdir}; mv %{buildroot}%{_libdir}/systemd/user/* %{buildroot}%{_userunitdir}/; rm -rf %{buildroot}%{_libdir}/systemd; fi

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprland-quick-style.so
%{_libdir}/libhyprland-quick-style-impl.so
%{_qt6_qmldir}/org/hyprland/

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
