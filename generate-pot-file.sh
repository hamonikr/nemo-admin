#!/bin/sh
# This script generates the po/nautilus-admin.pot file
FILEPATH="$(readlink -f "$0")"
DIR="$(dirname "$FILEPATH")"
cd "$DIR"
xgettext --package-name=nemo-extension-admin \
         --package-version=1.0.0 \
         --copyright-holder='Kevin Kim <chaeya@gmail.com>' \
         --msgid-bugs-address='https://github.com/chaeya/nemo-extension-admin/issues' \
         -cTRANSLATORS \
         -s -o "po/nemo-extension-admin.pot" \
         "extension/nemo-extension-admin.py"