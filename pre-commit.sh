#!/bin/sh

set -euo pipefail

exec 1>&2

pkgname='primula'
scripts=

mypy \
	--check-untyped-defs \
	--no-implicit-optional \
	primula

flake8 \
	${pkgname} ${scripts}

pycodestyle-3 \
	${pkgname} ${scripts}

python -m unittest
