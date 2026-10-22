#!/bin/sh
# Rebuilds the whole logo/ directory: six SVGs (three per ground), then
# the twenty PNGs.
set -e
cd "$(dirname "$0")"

python3 draw.py
python3 icon.py
python3 logotype.py

for f in ../logo/kyanite-logo.svg       ../logo/kyanite-logo-light.svg \
         ../logo/kyanite-icon.svg       ../logo/kyanite-icon-light.svg \
         ../logo/kyanite-logotype.svg   ../logo/kyanite-logotype-light.svg; do
  svgo --config svgo.config.mjs -i "$f" -o "$f" -q
  printf '%-30s %7d B\n' "$(basename "$f")" "$(stat -c%s "$f")"
done

python3 export.py
python3 optimize.py
