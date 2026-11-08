#!/bin/sh
# Copia los plugins (GenderBender y GenderBender Melo) y sus estilos a REAPER. Por defecto la ruta de macOS; otra con REAPER_DIR=...
# Uso: sh tools/install.sh [--test]
#   --test  instala ademas el banco de pruebas (tools/reaper_test) en Effects/GenderBenderTest y Scripts/GenderBenderTest
set -e
cd "$(dirname "$0")/.."
TEST=0
case "${1:-}" in
  "") ;;
  --test) TEST=1 ;;
  *) echo "uso: sh tools/install.sh [--test]" >&2; exit 1 ;;
esac
R="${REAPER_DIR:-$HOME/Library/Application Support/REAPER}"
[ -d "$R" ] || { echo "no existe $R (indica la ruta con REAPER_DIR=...)" >&2; exit 1; }
mkdir -p "$R/Effects/GenderBender" "$R/Data/drum_styles_v" "$R/Effects/GenderBenderMelo" "$R/Data/melo_styles"
cp GenderBender/* "$R/Effects/GenderBender/"
cp drum_styles_v/*.txt "$R/Data/drum_styles_v/"
cp GenderBenderMelo/*.jsfx "$R/Effects/GenderBenderMelo/"
cp melo_styles/*.txt "$R/Data/melo_styles/"
mkdir -p "$R/Data/melo_index" && cp melo_index/estilos.txt "$R/Data/melo_index/"
if [ "$TEST" = 1 ]; then
  T="$R/Effects/GenderBenderTest"; S="$R/Scripts/GenderBenderTest"
  mkdir -p "$T" "$S/scenarios" "$S/out"
  cp tools/reaper_test/gbtest_log.jsfx "$T/"
  python3 tools/reaper_test/make_test_jsfx.py GenderBenderMelo/genderbender_melo.jsfx "$T/genderbender_melo_test.jsfx" > /dev/null
  cp tools/reaper_test/lib.lua tools/reaper_test/stop.lua "$S/"
  cp tools/reaper_test/scenarios/*.lua "$S/scenarios/"
  for f in tools/reaper_test/scenarios/*.lua; do
    cp tools/reaper_test/run.lua "$S/run_$(basename "$f" .lua).lua"
  done
  echo "test -> $T"
  echo "test -> $S"
fi
echo "ok -> $R"
