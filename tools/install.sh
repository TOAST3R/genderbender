#!/bin/sh
# Copia los plugins (GenderBender y GenderBender Melo) y sus estilos a REAPER. Por defecto la ruta de macOS; otra con REAPER_DIR=...
# Uso: sh tools/install.sh
set -e
cd "$(dirname "$0")/.."
R="${REAPER_DIR:-$HOME/Library/Application Support/REAPER}"
[ -d "$R" ] || { echo "no existe $R (indica la ruta con REAPER_DIR=...)" >&2; exit 1; }
mkdir -p "$R/Effects/GenderBender" "$R/Data/drum_styles_v" "$R/Effects/GenderBenderMelo" "$R/Data/melo_styles"
cp GenderBender/* "$R/Effects/GenderBender/"
cp drum_styles_v/*.txt "$R/Data/drum_styles_v/"
cp GenderBenderMelo/*.jsfx "$R/Effects/GenderBenderMelo/"
cp melo_styles/*.txt "$R/Data/melo_styles/"
mkdir -p "$R/Data/melo_index" && cp melo_index/estilos.txt "$R/Data/melo_index/"
echo "ok -> $R"
