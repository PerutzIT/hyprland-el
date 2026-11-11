Name:           muparser
Version:        2.3.5
Release:        1%{?dist}
Summary:        Fast math parser library
License:        BSD-2-Clause
URL:            https://github.com/beltoforion/muparser
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake

%description
muParser is an extensible high performance math expression parser library
written in C++.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       muParser-devel = %{version}-%{release}
%description devel
Development files for %{name}.

%prep
%autosetup

%build
%cmake -DENABLE_SAMPLES=OFF -DENABLE_OPENMP=OFF -DENABLE_WIDE_CHAR=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%{_libdir}/libmuparser.so.2*

%files devel
%{_includedir}/muParser*.h
%{_libdir}/libmuparser.so
%{_libdir}/pkgconfig/muparser.pc
%{_libdir}/cmake/muparser/

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 2.3.5-1
- Initial package for Hyprland on EL10
