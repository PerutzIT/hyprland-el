Name:           grim
Version:        1.5.0
Release:        1%{?dist}
Summary:        Grab images from a Wayland compositor (screenshots)
License:        MIT
URL:            https://gitlab.freedesktop.org/emersion/grim
Source0:        %{url}/-/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  scdoc
BuildRequires:  bash-completion
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)

%description
Grab images from a Wayland compositor. Works with Hyprland and slurp.

%prep
%autosetup -n %{name}-v%{version}

%build
%meson -Djpeg=enabled -Dman-pages=enabled -Dbash-completions=true -Dfish-completions=true
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/grim
%{_mandir}/man1/grim.1*
%{_datadir}/bash-completion/completions/grim.bash
%{_datadir}/fish/vendor_completions.d/grim.fish

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
