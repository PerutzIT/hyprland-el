# Lua 5.5, parallel-installable next to the system Lua 5.4 (used by rpm/dnf)
%global major 5.5

Name:           lua5.5
Version:        5.5.1
Release:        1%{?dist}
Summary:        Lua %{major} programming language (parallel installable)
License:        MIT
URL:            https://www.lua.org/
Source0:        https://www.lua.org/ftp/lua-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  readline-devel

%description
Lua is a powerful, efficient, lightweight, embeddable scripting language.
This package provides Lua %{major} installed side by side with the
distribution's default Lua so it does not interfere with rpm or dnf.
Hyprland >= 0.57 uses Lua %{major} for its configuration.

%package libs
Summary:        Shared library for Lua %{major}
%description libs
Shared library liblua-%{major}.so.

%package devel
Summary:        Development files for Lua %{major}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Headers, pkg-config file (lua5.5.pc / lua-5.5.pc) and linker symlink for Lua %{major}.

%prep
%autosetup -n lua-%{version}

%build
cd src
CORE="lapi lcode lctype ldebug ldo ldump lfunc lgc llex lmem lobject lopcodes lparser lstate lstring ltable ltm lundump lvm lzio"
LIB="lauxlib lbaselib lcorolib ldblib liolib lmathlib loadlib loslib lstrlib ltablib lutf8lib linit"
CF="%{optflags} -fPIC -std=gnu99 -DLUA_COMPAT_5_4 -DLUA_USE_LINUX"
for f in $CORE $LIB; do gcc $CF -c $f.c -o $f.o; done
gcc -shared -Wl,-soname,liblua-%{major}.so %{build_ldflags} -o liblua-%{major}.so $(for f in $CORE $LIB; do echo $f.o; done) -lm -ldl
gcc $CF -DLUA_USE_READLINE -c lua.c -o lua.o
gcc %{build_ldflags} -o lua%{major} lua.o -L. -llua-%{major} -lm -ldl -lreadline
# luac needs internal symbols -> link statically against the objects
gcc $CF -c luac.c -o luac.o
gcc %{build_ldflags} -o luac%{major} luac.o $(for f in $CORE $LIB; do echo $f.o; done) -lm -ldl

%install
install -Dm755 src/liblua-%{major}.so %{buildroot}%{_libdir}/liblua-%{major}.so
install -Dm755 src/lua%{major} %{buildroot}%{_bindir}/lua%{major}
install -Dm755 src/luac%{major} %{buildroot}%{_bindir}/luac%{major}
install -d %{buildroot}%{_includedir}/lua%{major}
install -m644 src/lua.h src/luaconf.h src/lualib.h src/lauxlib.h src/lua.hpp %{buildroot}%{_includedir}/lua%{major}/
install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/lua%{major}.pc <<PC
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/lua%{major}

Name: Lua
Description: An Extensible Extension Language (%{major})
Version: %{version}
Libs: -L\${libdir} -llua-%{major} -lm -ldl
Cflags: -I\${includedir}
PC
ln -s lua%{major}.pc %{buildroot}%{_libdir}/pkgconfig/lua-%{major}.pc
install -d %{buildroot}%{_datadir}/lua/%{major} %{buildroot}%{_libdir}/lua/%{major}

%files
%{_bindir}/lua%{major}
%{_bindir}/luac%{major}

%files libs
%license README
%{_libdir}/liblua-%{major}.so
%dir %{_datadir}/lua/%{major}
%dir %{_libdir}/lua/%{major}

%files devel
%{_includedir}/lua%{major}/
%{_libdir}/pkgconfig/lua%{major}.pc
%{_libdir}/pkgconfig/lua-%{major}.pc

%changelog
* Wed Nov 11 2026 Hypr-EL <hypr-el@localhost> - 5.5.1-1
- Initial package for Hyprland on EL10
