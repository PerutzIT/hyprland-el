#!/bin/bash
# Build the complete Hyprland stack for Enterprise Linux 10 in dependency order,
# install every layer (needed as BuildRequires of the next one) and publish a
# local dnf repository in ./repo.
#
#   sudo ./scripts/build-all.sh            # everything (core + extras)
#   sudo ./scripts/build-all.sh --core     # Hyprland + hypr ecosystem only
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$PWD
TOP="${HYPR_TOPDIR:-$HOME/rpmbuild}"
export HYPR_TOPDIR="$TOP"

# --- host preparation ------------------------------------------------------
dnf -y install epel-release dnf-plugins-core
dnf config-manager --set-enabled crb
dnf -y install rpm-build rpmdevtools createrepo_c git-core \
    gcc gcc-c++ cmake meson ninja-build \
    gcc-toolset-15-gcc-c++ gcc-toolset-15-runtime gcc-toolset-15-gcc-plugin-annobin

# --- build order -----------------------------------------------------------
CORE=(
  # layer 0: EL10 system libraries that are too old / missing
  specs/wayland-protocols specs/libxkbcommon specs/lua5.5 specs/muparser specs/glaze
  # layer 1: hypr libraries
  specs/hyprutils specs/hyprwayland-scanner specs/hyprlang specs/hyprland-protocols
  specs/hyprwire specs/hyprcursor specs/hyprgraphics specs/aquamarine
  # layer 2: the compositor
  specs/hyprland
  # layer 3: ecosystem
  specs/hyprtoolkit specs/xdg-desktop-portal-hyprland specs/hyprpaper specs/hypridle
  specs/hyprlock specs/hyprsunset specs/hyprpicker specs/hyprland-guiutils
  specs/hyprland-qt-support specs/hyprqt6engine specs/hyprlauncher specs/hyprshutdown
  specs/hyprpwcenter specs/hyprsysteminfo specs/hyprpolkitagent
)
EXTRAS=(
  extras/gtk-layer-shell extras/playerctl extras/grim extras/slurp extras/mako
  extras/brightnessctl extras/waybar
  # complete preconfigured desktop (meta package + defaults)
  specs/hyprland-desktop
)
LIST=("${CORE[@]}")
[ "${1:-}" = "--core" ] || LIST+=("${EXTRAS[@]}")

mkdir -p "$ROOT/logs"
for s in "${LIST[@]}"; do
  n=$(basename "$s")
  printf '%-34s' "$n"
  if "$ROOT/scripts/build-one.sh" "$ROOT/$s.spec" --install > "$ROOT/logs/$n.log" 2>&1; then
    echo OK
  else
    echo "FAILED (see logs/$n.log)"; exit 1
  fi
done

"$ROOT/scripts/make-repo.sh"
