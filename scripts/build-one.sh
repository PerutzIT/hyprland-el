#!/bin/bash
# Build a single spec with rpmbuild and (optionally) install the resulting binary RPMs.
#   usage: build-one.sh <file.spec> [--install]
set -euo pipefail
spec="$1"; inst="${2:-}"
TOP="${HYPR_TOPDIR:-$HOME/rpmbuild}"
mkdir -p "$TOP"/{SOURCES,SPECS,RPMS,SRPMS,BUILD}
spectool -g -C "$TOP/SOURCES" "$spec"
cp -f "$(dirname "$spec")"/*.sh "$(dirname "$spec")"/*.patch "$TOP/SOURCES/" 2>/dev/null || true
dnf -y builddep "$spec"
rpmbuild --define "_topdir $TOP" -ba "$spec"
if [ "$inst" = "--install" ]; then
  mapfile -t pkgs < <(rpmspec --define "_topdir $TOP" -q --builtrpms --qf '%{arch}/%{name}-%{version}-%{release}.%{arch}.rpm\n' "$spec" | grep -v -- '-debug')
  ( cd "$TOP/RPMS" && dnf -y install "${pkgs[@]}" )
fi
