%global debug_package %{nil}
%global toolset gcc-toolset-15

Name:           glaze
Version:        7.2.0
Release:        1%{?dist}
Summary:        Extremely fast, in memory, JSON and reflection library for modern C++
License:        MIT
URL:            https://github.com/stephenberry/glaze
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
%{?enable_gcctoolset15}
BuildRequires:  cmake

%description
Header-only C++ JSON and reflection library (used by Hyprland).

%package devel
Summary:        Header-only C++ JSON and reflection library
Provides:       %{name}-static = %{version}-%{release}
%description devel
Header-only C++ JSON and reflection library (used by Hyprland).

%prep
%autosetup

%build
%cmake -Dglaze_DEVELOPER_MODE=OFF -Dglaze_BUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF -Dglaze_ENABLE_FUZZING=OFF
%cmake_build

%install
%cmake_install

%files devel
%license LICENSE
%{_includedir}/glaze/
%{_datadir}/glaze/

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 7.2.0-1
- Initial package for Hyprland on EL10
