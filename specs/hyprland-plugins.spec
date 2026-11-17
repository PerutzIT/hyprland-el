%global toolset gcc-toolset-15
%{?enable_gcctoolset15}

# Official hyprwm plugins at the revision hyprpm uses for Hyprland 0.57.x
%global commit      2e03a09a92ba8b0adcd2840a69d84ffc2174b886
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapdate    20261116

# Plugins use Hyprland's internal C++ API: they must be built against, and run
# with, exactly the same Hyprland build.
%global hyprland_evr %(rpm -q --qf '%%{EPOCH}:%%{VERSION}-%%{RELEASE}' hyprland-devel 2>/dev/null | sed 's/^(none)://')

%global plugins borders-plus-plus csgo-vulkan-fix hyprbars hyprfocus

Name:           hyprland-plugins
Version:        0.57.0^%{snapdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        Official Hyprland plugins (hyprbars, hyprfocus, borders-plus-plus, csgo-vulkan-fix)
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-plugins
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  %{toolset}-gcc-c++
BuildRequires:  %{toolset}-runtime
BuildRequires:  %{toolset}-gcc-plugin-annobin
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  hyprland-devel

Requires:       hyprland%{?_isa} = %{hyprland_evr}

%description
The official plugins maintained by the Hyprland developers, built for the
hyprland package of this repository:

  hyprbars           title bars with buttons (close, maximize, minimize, ...)
  hyprfocus          flash animation on focus changes
  borders-plus-plus  additional window borders
  csgo-vulkan-fix    fake resolution for CS2 / games that misbehave on scaling

Load a plugin from the Lua config, e.g.:
  hl.plugin.load("%{_libdir}/hyprland/plugins/hyprbars.so")

%prep
%autosetup -n %{name}-%{commit}

%build
%set_build_flags
for p in %{plugins}; do
    # flags via the environment: the Makefiles append -shared -fPIC -std=...
    CXX=g++ CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" %make_build -C "$p" all
done

%install
for p in %{plugins}; do
    install -Dpm 0755 "$p/$p.so" %{buildroot}%{_libdir}/hyprland/plugins/$p.so
done
for p in %{plugins}; do
    cp -p "$p/README.md" "README-$p.md"
done

%files
%license LICENSE
%doc README.md README-*.md
%dir %{_libdir}/hyprland
%dir %{_libdir}/hyprland/plugins
%{_libdir}/hyprland/plugins/*.so

%changelog
* Tue Nov 17 2026 Hypr-EL <hypr-el@localhost> - 0.57.0^20261116git2e03a09-1
- Initial package (hyprbars, hyprfocus, borders-plus-plus, csgo-vulkan-fix)
