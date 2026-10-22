#!/bin/sh
# Reconstruit tout le dossier logo/ : les trois SVG, puis les neuf PNG.
set -e
cd "$(dirname "$0")"

python3 dessine.py
python3 icone.py
python3 logotype.py

for f in ../logo/kyanite-logo.svg ../logo/kyanite-icon.svg ../logo/kyanite-logotype.svg; do
  svgo --config svgo.config.mjs -i "$f" -o "$f" -q
  printf '%-24s %7d o\n' "$(basename "$f")" "$(stat -c%s "$f")"
done

python3 exporte.py
python3 optimise.py
