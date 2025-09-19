#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import curses
import locale
import subprocess
from pathlib import Path

locale.setlocale(locale.LC_ALL, '')

HELP_TEXT = "↑/k y ↓/j: mover  |  ESPACIO: seleccionar  |  a: seleccionar todo  |  i: invertir  |  ENTER: convertir  |  q: salir"

def list_txt_files(directory: Path):
    files = []
    for name in sorted(os.listdir(directory)):
        if name.startswith('.'):
            continue  # ocultos fuera
        p = directory / name
        if p.is_file() and name.lower().endswith('.txt'):
            files.append(p)
    return files

def draw_menu(stdscr, files, selected, idx, top):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = "Selecciona archivos .txt para convertir a .cho (ChordPro)"
    stdscr.addstr(0, 0, title[:w-1], curses.A_BOLD)
    stdscr.addstr(1, 0, HELP_TEXT[:w-1], curses.A_DIM)

    # área de lista desde la línea 3
    visible_rows = max(1, h - 4)
    bottom = min(len(files), top + visible_rows)

    for i, path in enumerate(files[top:bottom], start=top):
        mark = "[x]" if i in selected else "[ ]"
        line = f"{mark} {path.name}"
        y = 3 + (i - top)
        if i == idx:
            stdscr.addstr(y, 0, line[:w-1], curses.A_REVERSE)
        else:
            stdscr.addstr(y, 0, line[:w-1])

    status = f"{len(selected)} seleccionados  |  {len(files)} .txt encontrados"
    stdscr.addstr(h-1, 0, status[:w-1], curses.A_DIM)
    stdscr.refresh()

def picker(stdscr, files):
    curses.curs_set(0)
    stdscr.keypad(True)
    idx = 0
    top = 0
    selected = set()

    while True:
        h, w = stdscr.getmaxyx()
        visible_rows = max(1, h - 4)
        # ajustar ventana
        if idx < top:
            top = idx
        elif idx >= top + visible_rows:
            top = idx - visible_rows + 1

        draw_menu(stdscr, files, selected, idx, top)

        ch = stdscr.getch()
        if ch in (curses.KEY_UP, ord('k')):
            if idx > 0:
                idx -= 1
        elif ch in (curses.KEY_DOWN, ord('j')):
            if idx < len(files) - 1:
                idx += 1
        elif ch == ord(' '):  # toggle
            if idx in selected:
                selected.remove(idx)
            else:
                selected.add(idx)
        elif ch == ord('a'):  # select all
            selected = set(range(len(files)))
        elif ch == ord('i'):  # invert selection
            selected = set(range(len(files))) - selected
        elif ch in (10, 13, curses.KEY_ENTER):  # Enter
            return [files[i] for i in sorted(selected)]
        elif ch in (ord('q'), 27):  # q o ESC
            return []
        # ignorar otras teclas

def convert_files(paths):
    results = []
    for p in paths:
        out = p.with_suffix('.cho')
        if out.exists():
            results.append((p, out, 'skip-exists'))
            continue
        try:
            # Ejecuta: chordpro "input.txt" -o "output.cho"
            completed = subprocess.run(
                ["chordpro", str(p), "-o", str(out)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if completed.returncode == 0:
                results.append((p, out, 'ok'))
            else:
                results.append((p, out, f'error: {completed.stderr.strip()}'))
        except FileNotFoundError:
            results.append((p, out, 'error: no se encontró el comando "chordpro" en PATH'))
        except Exception as e:
            results.append((p, out, f'error: {e}'))
    return results

def main():
    # Carpeta objetivo: actual o pasada como argumento
    target_dir = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else Path.cwd()
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Carpeta no válida: {target_dir}", file=sys.stderr)
        sys.exit(1)

    files = list_txt_files(target_dir)
    if not files:
        print("No se encontraron archivos .txt (no ocultos) en la carpeta.", file=sys.stderr)
        sys.exit(1)

    selected = curses.wrapper(picker, files)

    if not selected:
        print("No se seleccionó ningún archivo. Saliendo.")
        sys.exit(0)

    print(f"\nConvirtiendo {len(selected)} archivo(s) con chordpro...\n")
    results = convert_files(selected)

    ok = 0
    skipped = 0
    failed = 0
    for src, dst, status in results:
        if status == 'ok':
            ok += 1
            print(f"✔ OK  -> {src.name}  →  {dst.name}")
        elif status == 'skip-exists':
            skipped += 1
            print(f"⏭ Omitido (ya existe) -> {dst.name}")
        else:
            failed += 1
            print(f"✖ Error -> {src.name}: {status}")

    print("\nResumen:")
    print(f"  Convertidos: {ok}")
    print(f"  Omitidos (existían): {skipped}")
    print(f"  Fallidos: {failed}")

    if failed > 0:
        print("\nSugerencias:")
        print("  • Asegúrate de tener instalado chordpro y que esté en el PATH.")
        print("  • Ejecuta manualmente un archivo problemático para ver el error:")
        print('      chordpro "archivo.txt" -o "archivo.cho"')

if __name__ == "__main__":
    main()
