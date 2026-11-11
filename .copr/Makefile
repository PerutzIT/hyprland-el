# Fedora COPR "make_srpm" entry point.
# COPR runs:  make -f .copr/Makefile srpm outdir=<dir> spec=<path/to/x.spec>
# The SRPM is built on the COPR builder from the public git checkout, so no
# local machine data ends up in the packages.
SPEC   := $(abspath $(spec))
SPECDIR := $(dir $(SPEC))

.PHONY: srpm
srpm:
	command -v spectool >/dev/null || dnf -y install rpmdevtools rpm-build
	spectool -g -C "$(SPECDIR)" "$(SPEC)"
	rpmbuild -bs \
	  --define "_sourcedir $(SPECDIR)" \
	  --define "_srcrpmdir $(outdir)" \
	  --define "dist .el10" \
	  "$(SPEC)"
