%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprqt6engine
Version:        0.1.0
Release:        1%{?dist}
Summary:        Qt6 theme provider for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprqt6engine
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprutils-devel
BuildRequires:  hyprlang-devel
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6BuildInternals)
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6IconThemes)

%description
Qt6 platform theme / style engine for Hyprland (QT_QPA_PLATFORMTHEME=hyprqt6engine).

%prep
%autosetup
# Qt >= 6.10 requires private modules to be requested explicitly
sed -i 's/COMPONENTS BuildInternals Core Widgets)/COMPONENTS BuildInternals Core Widgets GuiPrivate WidgetsPrivate)/' CMakeLists.txt

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
%{_libdir}/libhyprqt6engine-common.so
%{_qt6_plugindir}/platformthemes/libhyprqt6engine.so
%{_qt6_plugindir}/styles/libhypr-style.so

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
