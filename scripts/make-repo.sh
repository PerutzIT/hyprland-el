#!/bin/bash
# Collect built RPMs into ./repo/el10 and (re)generate the dnf metadata.
set -euo pipefail
cd "$(dirname "$0")/.."
TOP="${HYPR_TOPDIR:-$HOME/rpmbuild}"
R=$PWD/repo/el10
mkdir -p "$R/x86_64" "$R/SRPMS"
cp -u "$TOP"/RPMS/x86_64/*.rpm "$TOP"/RPMS/noarch/*.rpm "$R/x86_64/"
cp -u "$TOP"/SRPMS/*.src.rpm "$R/SRPMS/"
createrepo_c --update "$R/x86_64"
createrepo_c --update "$R/SRPMS"
cat > /etc/yum.repos.d/hypr-el-local.repo <<REPO
[hypr-el-local]
name=Hyprland for Enterprise Linux 10 (local build)
baseurl=file://$R/x86_64
enabled=1
gpgcheck=0
priority=50
REPO
echo "Local repository ready: $R  (/etc/yum.repos.d/hypr-el-local.repo)"
