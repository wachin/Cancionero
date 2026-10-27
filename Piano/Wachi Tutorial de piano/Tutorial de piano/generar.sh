#!/usr/bin/env bash
# Regenera tutorial-piano.odt y tutorial-piano.pdf a partir de tutorial-piano.md
# Uso: ./generar.sh
set -euo pipefail
cd "$(dirname "$0")"

if command -v rsvg-convert >/dev/null 2>&1; then
  echo "0/4  SVG -> PNG"
  shopt -s nullglob
  for f in *.svg */*.svg; do
    rsvg-convert -w 1900 "$f" -o "${f%.svg}.png"
  done
else
  echo "0/4  rsvg-convert no está instalado: se usan los PNG existentes"
fi

echo "1/4  Markdown -> ODT"
pandoc tutorial-piano.md -o tutorial-piano.odt

echo "2/4  Aplicando bordes a las tablas"
python3 - <<'PY'
import os, re, tempfile, zipfile

src = "tutorial-piano.odt"
tmp = tempfile.mkdtemp()
with zipfile.ZipFile(src) as z:
    z.extractall(tmp)

path = os.path.join(tmp, "content.xml")
s = open(path, encoding="utf-8").read()

# Pandoc genera las celdas sin borde: se los agregamos para que las tablas se lean mejor
s = s.replace('fo:border="none"', 'fo:border="0.5pt solid #BFBFBF" fo:padding="0.05in"')

# Fila de encabezado con fondo gris claro
s = s.replace(
    '<style:style style:name="TableHeaderRowCell" style:family="table-cell">\n      <style:table-cell-properties',
    '<style:style style:name="TableHeaderRowCell" style:family="table-cell">\n      <style:table-cell-properties fo:background-color="#EDEDED"')

open(path, "w", encoding="utf-8").write(s)

# Las figuras con leyenda se centran (pandoc las deja alineadas a la izquierda)
spath = os.path.join(tmp, "styles.xml")
st = open(spath, encoding="utf-8").read()
for name in ("Figure", "FigureCaption"):
    st = re.sub(r'(<style:style[^>]*style:name="%s"[^>]*>\s*<style:paragraph-properties)' % name,
                r'\1 fo:text-align="center"', st)
# FigureCaption hereda de Caption y no trae propiedades propias: se las agregamos
st = re.sub(r'(<style:style[^>]*style:name="FigureCaption"[^>]*>)\s*</style:style>',
            r'\1<style:paragraph-properties fo:text-align="center"/></style:style>', st)
# Las tablas son cortas: se evita que una fila quede sola en la página siguiente
for name in ("Table_20_Contents", "Table_20_Heading"):
    st = re.sub(r'(<style:style[^>]*style:name="%s"[^>]*>\s*<style:paragraph-properties)' % name,
                r'\1 fo:keep-with-next="always"', st)
open(spath, "w", encoding="utf-8").write(st)

with zipfile.ZipFile(src, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(tmp, "mimetype"), "mimetype", compress_type=zipfile.ZIP_STORED)
    for root, _, files in os.walk(tmp):
        for f in files:
            p = os.path.join(root, f)
            arc = os.path.relpath(p, tmp)
            if arc != "mimetype":
                z.write(p, arc)
PY

echo "3/4  ODT -> PDF"
soffice --headless --convert-to pdf --outdir . tutorial-piano.odt >/dev/null 2>&1

echo "Listo: tutorial-piano.odt y tutorial-piano.pdf"
