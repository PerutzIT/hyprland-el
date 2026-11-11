%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprsysteminfo
Version:        0.2.0
Release:        1%{?dist}
Summary:        Tiny system info application for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprsysteminfo
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         hyprsysteminfo-0001-pciutils-extern-c.patch

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprutils-devel
BuildRequires:  hyprtoolkit-devel
BuildRequires:  glaze-devel
BuildRequires:  pkgconfig(libpci)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)

%description
Tiny system info application for Hyprland.

%prep
%autosetup -p1

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
%{_bindir}/hyprsysteminfo
%{_datadir}/applications/hyprsysteminfo.desktop

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
