%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

Name:           hyprpwcenter
Version:        0.1.2
Release:        1%{?dist}
Summary:        PipeWire audio control center for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpwcenter
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  hyprutils-devel
BuildRequires:  hyprtoolkit-devel
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)

%description
PipeWire audio control center for Hyprland.

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
%{_bindir}/hyprpwcenter
%{_datadir}/applications/hyprpwcenter.desktop

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
