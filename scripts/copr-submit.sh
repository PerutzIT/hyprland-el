#!/bin/bash
# Create/update the Fedora COPR project and build every package in dependency
# order. Each package is built by COPR directly from this public git repository
# (method make_srpm, see .copr/Makefile).
#
# Requirements: copr-cli and an API token in ~/.config/copr
#               (https://copr.fedorainfracloud.org/api/).
#
#   ./scripts/copr-submit.sh                 # create project + build everything
#   ./scripts/copr-submit.sh --core          # Hyprland + hypr ecosystem only
#   ./scripts/copr-submit.sh hyprland waybar # rebuild only these packages
#
# Environment:
#   COPR_PROJECT  owner/project or project (default: hyprland-el)
#   COPR_CHROOTS  space separated chroots   (default: epel-10-x86_64)
#   GIT_URL       clone URL                 (default: the public GitHub repo)
#   GIT_REF       branch/tag/commit         (default: main)
set -euo pipefail
cd "$(dirname "$0")/.."

PROJECT="${COPR_PROJECT:-hyprland-el}"
CHROOTS="${COPR_CHROOTS:-epel-10-x86_64}"
GIT_URL="${GIT_URL:-https://github.com/PerutzIT/hyprland-el.git}"
GIT_REF="${GIT_REF:-main}"

# Same order as scripts/build-all.sh
CORE=(
  specs/wayland-protocols specs/libxkbcommon specs/lua5.5 specs/muparser specs/glaze
  specs/hyprutils specs/hyprwayland-scanner specs/hyprlang specs/hyprland-protocols
  specs/hyprwire specs/hyprcursor specs/hyprgraphics specs/aquamarine
  specs/hyprland
  specs/hyprtoolkit specs/xdg-desktop-portal-hyprland specs/hyprpaper specs/hypridle
  specs/hyprlock specs/hyprsunset specs/hyprpicker specs/hyprland-guiutils
  specs/hyprland-qt-support specs/hyprqt6engine specs/hyprlauncher specs/hyprshutdown
  specs/hyprpwcenter specs/hyprsysteminfo specs/hyprpolkitagent
)
EXTRAS=(
  extras/gtk-layer-shell extras/playerctl extras/grim extras/slurp extras/mako
  extras/brightnessctl extras/waybar
)

ALL=("${CORE[@]}" "${EXTRAS[@]}")
LIST=()
if [ "${1:-}" = "--core" ]; then
  LIST=("${CORE[@]}")
elif [ $# -gt 0 ]; then
  for want in "$@"; do
    for s in "${ALL[@]}"; do [ "$(basename "$s")" = "$want" ] && LIST+=("$s"); done
  done
  [ ${#LIST[@]} -eq $# ] || { echo "unknown package in: $*" >&2; exit 1; }
else
  LIST=("${ALL[@]}")
fi

copr-cli whoami >/dev/null

chroot_args=(); for c in $CHROOTS; do chroot_args+=(--chroot "$c"); done
common=(
  --description "Hyprland and its complete ecosystem (hyprpm plugin support, xdg-desktop-portal-hyprland, hyprlock, hypridle, hyprpaper, waybar, ...) for RHEL 10, AlmaLinux 10 and Rocky Linux 10. Sources: $GIT_URL"
  --instructions "Enable EPEL and CRB first: dnf install epel-release && dnf config-manager --set-enabled crb. Then: dnf copr enable $PROJECT && dnf install hyprland. See $GIT_URL for details."
  --repo-priority 90
)
if copr-cli get "$PROJECT" >/dev/null 2>&1; then
  copr-cli modify "$PROJECT" "${common[@]}" "${chroot_args[@]}"
else
  copr-cli create "$PROJECT" "${common[@]}" "${chroot_args[@]}"
fi

# Register/refresh one SCM package per spec
for s in "${LIST[@]}"; do
  n=$(basename "$s")
  args=(--name "$n" --clone-url "$GIT_URL" --commit "$GIT_REF"
        --spec "$s.spec" --method make_srpm --webhook-rebuild off)
  copr-cli edit-package-scm "$PROJECT" "${args[@]}" >/dev/null 2>&1 \
    || copr-cli add-package-scm "$PROJECT" "${args[@]}" >/dev/null
done

# Chain the builds: every package starts after the previous one finished, so
# each layer finds its BuildRequires in the project repository.
prev=""
for s in "${LIST[@]}"; do
  n=$(basename "$s")
  after=(); [ -n "$prev" ] && after=(--after-build-id "$prev")
  out=$(copr-cli build-package "$PROJECT" --name "$n" --nowait "${after[@]}")
  prev=$(sed -n 's/^Created builds: \([0-9]*\).*/\1/p' <<<"$out")
  [ -n "$prev" ] || { echo "$out" >&2; exit 1; }
  printf '%-32s build %s\n' "$n" "$prev"
done
echo "Watch: https://copr.fedorainfracloud.org/coprs/ (project $PROJECT)"
