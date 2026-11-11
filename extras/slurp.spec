Name:           slurp
Version:        1.5.0
Release:        1%{?dist}
Summary:        Select a region in a Wayland compositor
License:        MIT
URL:            https://github.com/emersion/slurp
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  scdoc
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)

%description
Select a region in a Wayland compositor and print it to stdout (used with grim).

%prep
%autosetup

%build
%meson -Dman-pages=enabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/slurp
%{_mandir}/man1/slurp.1*

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
