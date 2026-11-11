Name:           brightnessctl
Version:        0.5.1
Release:        1%{?dist}
Summary:        Read and control device brightness (backlight, LEDs)
License:        MIT
URL:            https://github.com/Hummer12007/brightnessctl
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libsystemd)

%description
A program to read and control device brightness via logind (no setuid needed).

%prep
%autosetup

%build
%set_build_flags
%make_build ENABLE_SYSTEMD=1

%install
%make_install PREFIX=%{_prefix} ENABLE_SYSTEMD=1 MANDIR=%{_mandir}

%files
%license LICENSE
%doc README.md
%{_bindir}/brightnessctl

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
