Name:           brightnessctl
Version:        0.5.1
Release:        2%{?dist}
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
%make_install PREFIX=%{_prefix} ENABLE_SYSTEMD=1 MANDIR=%{buildroot}%{_mandir}

%files
%license LICENSE
%doc README.md
%{_bindir}/brightnessctl
%{_mandir}/man1/brightnessctl.1*

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 0.5.1-2
- Install the man page into the buildroot (fixes non-root builds)

* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - %{version}-1
- Initial package for EL10
