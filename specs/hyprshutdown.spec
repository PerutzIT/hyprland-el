%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprshutdown
Version:        0.1.2
Release:        1%{?dist}
Summary:        Graceful shutdown/logout utility for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprshutdown
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprutils-devel
BuildRequires:  hyprtoolkit-devel
BuildRequires:  glaze-devel
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)

%description
Graceful shutdown/logout utility for Hyprland.

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
%{_bindir}/hyprshutdown

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
