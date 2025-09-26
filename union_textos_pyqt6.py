#!/usr/bin/env python3
"""
Unionador de archivos de texto - PyQt6

Guarda este archivo como union_textos_pyqt6.py y ejecútalo con Python 3
Requisitos: PyQt6

Características:
- Arrastrar y soltar varios archivos de texto dentro de la lista.
- Botón "Añadir" para abrir un diálogo y seleccionar archivos.
- Muestra rutas completas en la lista.
- Campo para nombre de archivo de salida (por defecto "merged.txt").
- Muestra la carpeta donde se guardará (por defecto la carpeta del primer archivo añadido).
- Botón para cambiar carpeta de salida.
- Botón "Unir" para crear el archivo combinado.

Soporta URIs tipo file:/// y rutas directas.
"""

from __future__ import annotations
import sys
import os
from pathlib import Path
from typing import List

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QFrame,
)


class FileListWidget(QListWidget):
    """QListWidget que acepta archivos mediante arrastrar y soltar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(self.SelectionMode.ExtendedSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        paths = []
        for u in urls:
            if isinstance(u, QUrl):
                # QUrl.toLocalFile() maneja file:/// y rutas normales
                p = u.toLocalFile()
            else:
                p = str(u)
            if p:
                paths.append(p)
        self.parent().add_files(paths)
        event.acceptProposedAction()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Unir archivos de texto - PyQt6')
        self.resize(800, 500)

        self.files: List[Path] = []
        self.output_folder: Path | None = None

        main_layout = QVBoxLayout(self)

        # Instrucciones
        instruct = QLabel('Arrastra aquí archivos de texto o usa "Añadir". Selecciona el orden antes de unir.')
        main_layout.addWidget(instruct)

        # Lista de archivos
        self.list_widget = FileListWidget(self)
        self.list_widget.setFrameShape(QFrame.Shape.Box)
        main_layout.addWidget(self.list_widget, stretch=1)

        # Botones de añadir / eliminar
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('Añadir')
        add_btn.clicked.connect(self.on_add)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton('Eliminar selección')
        remove_btn.clicked.connect(self.on_remove_selected)
        btn_layout.addWidget(remove_btn)

        clear_btn = QPushButton('Vaciar lista')
        clear_btn.clicked.connect(self.on_clear)
        btn_layout.addWidget(clear_btn)

        # Botón para mover arriba/abajo
        up_btn = QPushButton('Mover arriba')
        up_btn.clicked.connect(self.on_move_up)
        btn_layout.addWidget(up_btn)

        down_btn = QPushButton('Mover abajo')
        down_btn.clicked.connect(self.on_move_down)
        btn_layout.addWidget(down_btn)

        main_layout.addLayout(btn_layout)

        # Output filename y carpeta
        out_layout = QHBoxLayout()

        form_layout = QVBoxLayout()
        lbl_name = QLabel('Nombre de archivo de salida:')
        form_layout.addWidget(lbl_name)
        self.output_name_edit = QLineEdit('merged.txt')
        form_layout.addWidget(self.output_name_edit)
        out_layout.addLayout(form_layout, stretch=2)

        # Carpeta de salida y botón
        folder_layout = QVBoxLayout()
        lbl_folder = QLabel('Carpeta de salida:')
        folder_layout.addWidget(lbl_folder)
        self.folder_label = QLabel('(ninguna - se establecerá cuando añadas archivos)')
        self.folder_label.setWordWrap(True)
        folder_layout.addWidget(self.folder_label)
        choose_btn = QPushButton('Seleccionar carpeta...')
        choose_btn.clicked.connect(self.on_choose_folder)
        folder_layout.addWidget(choose_btn)
        out_layout.addLayout(folder_layout, stretch=3)

        main_layout.addLayout(out_layout)

        # Botón unir
        join_layout = QHBoxLayout()
        join_layout.addStretch(1)
        self.join_btn = QPushButton('Unir')
        self.join_btn.clicked.connect(self.on_join)
        join_layout.addWidget(self.join_btn)
        main_layout.addLayout(join_layout)

    # ----------------- acciones -----------------
    def on_add(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Seleccionar archivos de texto', str(Path.home()), 'Text Files (*.txt);;All Files (*)')
        if files:
            self.add_files(files)

    def add_files(self, paths: List[str]):
        # Normaliza y filtra solo archivos existentes
        added_any = False
        for p in paths:
            if p.startswith('file://'):
                # QUrl.toLocalFile() normalmente ya habría limpiado esto, pero por si acaso
                p = p.replace('file://', '')
                # En Linux puede iniciar con an extra slash
                if p.startswith('///'):
                    p = p[2:]
            path = Path(p)
            if path.exists() and path.is_file():
                # Evitar duplicados
                if path not in self.files:
                    self.files.append(path)
                    item = QListWidgetItem(str(path))
                    self.list_widget.addItem(item)
                    added_any = True
        if added_any and self.output_folder is None:
            # Establece carpeta de salida por defecto a la carpeta del primer archivo
            first_folder = self.files[0].parent
            self.set_output_folder(first_folder)

    def on_remove_selected(self):
        selected = list(self.list_widget.selectedItems())
        if not selected:
            return
        for it in selected:
            row = self.list_widget.row(it)
            self.list_widget.takeItem(row)
            try:
                del self.files[row]
            except IndexError:
                pass
        # Si lista vacía limpiar carpeta por defecto
        if not self.files:
            self.set_output_folder(None)

    def on_clear(self):
        self.list_widget.clear()
        self.files = []
        self.set_output_folder(None)

    def on_move_up(self):
        rows = sorted({self.list_widget.row(i) for i in self.list_widget.selectedItems()})
        for r in rows:
            if r > 0:
                item = self.list_widget.takeItem(r)
                self.list_widget.insertItem(r - 1, item)
                self.files.insert(r - 1, self.files.pop(r))
                item.setSelected(True)

    def on_move_down(self):
        rows = sorted({self.list_widget.row(i) for i in self.list_widget.selectedItems()}, reverse=True)
        count = self.list_widget.count()
        for r in rows:
            if r < count - 1:
                item = self.list_widget.takeItem(r)
                self.list_widget.insertItem(r + 1, item)
                self.files.insert(r + 1, self.files.pop(r))
                item.setSelected(True)

    def on_choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Seleccionar carpeta de salida', str(Path.home()))
        if folder:
            self.set_output_folder(Path(folder))

    def set_output_folder(self, folder: Path | None):
        self.output_folder = folder
        if folder is None:
            self.folder_label.setText('(ninguna - se establecerá cuando añadas archivos)')
        else:
            self.folder_label.setText(str(folder))

    def on_join(self):
        if not self.files:
            QMessageBox.warning(self, 'Error', 'No hay archivos para unir.')
            return
        out_name = self.output_name_edit.text().strip()
        if not out_name:
            QMessageBox.warning(self, 'Error', 'Escribe un nombre de archivo de salida.')
            return
        # Asegurar extensión .txt si no la tiene
        if not out_name.lower().endswith('.txt'):
            out_name += '.txt'
        out_folder = self.output_folder or self.files[0].parent
        out_path = out_folder / out_name

        try:
            # Abrir y escribir en modo utf-8; intentar detectar errores y avisar
            with out_path.open('w', encoding='utf-8') as fout:
                for i, p in enumerate(self.files):
                    try:
                        with p.open('r', encoding='utf-8') as fin:
                            content = fin.read()
                    except UnicodeDecodeError:
                        # Si falla utf-8, intentar con latin-1
                        with p.open('r', encoding='latin-1') as fin:
                            content = fin.read()
                    # Escribir separador entre archivos (opcional)
                    if i != 0:
                        fout.write('\n\n---- FIN DE ARCHIVO ----\n\n')
                    fout.write(f"<!-- Inicio: {p.name} -->\n")
                    fout.write(content)
                    fout.write(f"\n<!-- Fin: {p.name} -->\n")

            QMessageBox.information(self, 'Completado', f'Archivo creado:\n{out_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error al escribir archivo', str(e))


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
