%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprtoolkit
Version:        0.6.0
Release:        1%{?dist}
Summary:        Modern C++ Wayland-native GUI toolkit for the Hypr ecosystem
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprtoolkit
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# EL10 ships Pango 1.54, PANGO_WRAP_NONE needs 1.56
Patch0:         hyprtoolkit-0001-pango-1.54-compat.patch

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprwayland-scanner >= 0.4.0
BuildRequires:  aquamarine-devel >= 0.10.0
BuildRequires:  hyprgraphics-devel >= 0.3.0
BuildRequires:  hyprutils-devel >= 0.14.2
BuildRequires:  hyprlang-devel >= 0.6.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  libglvnd-devel
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  iniparser-devel
BuildRequires:  abseil-cpp-devel

%description
A modern C++ Wayland-native GUI toolkit used by hyprlauncher,
hyprpolkitagent, hyprland-guiutils and other Hypr apps.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       aquamarine-devel hyprgraphics-devel hyprutils-devel
%description devel
Development files for %{name}.

%prep
%autosetup -p1

%build
# EL10's iniparser-devel ships no pkg-config file -> provide one for the build
mkdir -p el-pc
cat > el-pc/iniparser.pc <<PC
Name: iniparser
Description: iniparser (EL10 compat)
Version: 4.1
Libs: -liniparser
Cflags: -I%{_includedir}/iniparser
PC
export PKG_CONFIG_PATH=$PWD/el-pc${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}
%cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
# EL10 has no iniparser.pc: replace the private pkg-config requirement with a plain linker flag
sed -i -e 's/, iniparser,/,/' -e '/^Libs:/a Libs.private: -liniparser' %{buildroot}%{_libdir}/pkgconfig/hyprtoolkit.pc
# some projects install user units into lib64 or the wrong prefix
if [ -d %{buildroot}%{_libdir}/systemd/user ]; then install -d %{buildroot}%{_userunitdir}; mv %{buildroot}%{_libdir}/systemd/user/* %{buildroot}%{_userunitdir}/; rm -rf %{buildroot}%{_libdir}/systemd; fi

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprtoolkit.so.*

%files devel
%{_includedir}/hyprtoolkit/
%{_libdir}/libhyprtoolkit.so
%{_libdir}/pkgconfig/hyprtoolkit.pc

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
