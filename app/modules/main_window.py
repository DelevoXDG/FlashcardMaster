import os
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListView,
    QLabel,
    QTableView,
    QAbstractItemView,
)
from PyQt6.QtCore import (
    QSize,
)
from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)
from PyQt6 import uic
from . import (
    Deck,
    engine,
    DeckTableModel,
)

from .tests import sample_db_data as dbtest

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard Master")

        self.model = DeckTableModel()
        # dbtest.add_sample_decks()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "main_window.ui")
        uic.loadUi(ui_path, self)

        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.resizeColumnsToContents()

        self.selection_model = self.view.selectionModel()
        self.delete_button.clicked.connect(self.delete_records)
        self.delete_button.setEnabled(False)
        self.create_playlist_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.selection_model.selectionChanged.connect(self.toggle_buttons_selection)

        self.model.refresh()

    def toggle_buttons_selection(self):
        """Toggle button enabled state based on selection"""
        self.delete_button.setEnabled(self.selection_model.hasSelection())
        self.create_playlist_button.setEnabled(self.selection_model.hasSelection())
        self.export_button.setEnabled(
            self.selection_model.hasSelection()
            and len(self.selection_model.selectedRows()) == 1
        )

    def delete_records(self):
        """Delete selected decks"""
        del_rows = self.selection_model.selectedRows()
        self.model.delete_rows(del_rows)
