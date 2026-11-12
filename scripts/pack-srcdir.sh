#!/bin/bash
# Pack specs/<name>/ into <outdir>/<name>-<version>.tar.gz for specs that keep
# their sources in this repository (e.g. hyprland-desktop). Deterministic and
# free of local metadata: fixed mtime, numeric root owner, gzip without name/time.
#   usage: pack-srcdir.sh <file.spec> <outdir>
set -euo pipefail
spec="$1"; out="$2"
name=$(basename "$spec" .spec)
dir="$(dirname "$spec")/$name"
[ -d "$dir" ] || exit 0
ver=$(rpmspec -q --srpm --qf '%{version}' "$spec" 2>/dev/null)
mkdir -p "$out"
tar --sort=name --mtime='2026-01-01 00:00:00Z' --owner=0 --group=0 --numeric-owner \
    --transform "s,^\.,$name," -C "$dir" -cf - . | gzip -n9 > "$out/$name-$ver.tar.gz"
