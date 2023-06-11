import os
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListView,
    QLabel,
    QTableView,
    QAbstractItemView,
    QMessageBox,
    QPushButton,
)
from PyQt6.QtCore import (
    QSize,
    QItemSelectionModel,
    Qt,
)
from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)
from PyQt6 import uic
from . import Deck, engine, DeckTableModel, DeckWidget

from .tests import sample_db_data as dbtest

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Flashcard Master")

        self.model = DeckTableModel()
        # dbtest.add_sample_decks()
        # dbtest.add_sample_flashcards()
        # dbtest.add_sample_decks_with_categories()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "main_window.ui")
        uic.loadUi(ui_path, self)

        self.view: QTableView = self.view
        self.add_button: QPushButton = self.add_button
        self.delete_button: QPushButton = self.delete_button
        self.import_button: QPushButton = self.import_button
        self.export_button: QPushButton = self.export_button
        self.create_playlist_button: QPushButton = self.create_playlist_button
        self.stats_button: QPushButton = self.stats_button

        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.resizeColumnsToContents()
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        # self.view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        self.selection_model = self.view.selectionModel()
        self.delete_button.clicked.connect(self.delete_decks)
        self.view.doubleClicked.connect(self.open_deck_widget)

        self.delete_button.setEnabled(False)
        self.create_playlist_button.setEnabled(False)
        self.export_button.setEnabled(False)

        self.selection_model.selectionChanged.connect(self.toggle_buttons_selection)

        self.model.refresh()

    def refresh_deck_table(self, deck_row):
        # index = self.model.index(deck_row.row(), 1)
        # self.model.dataChanged.emit(index, index)
        # self.model.refresh()
        # self.view.update()
        # self.view.repaint()
        self.model.refresh()
        self.view.resizeColumnsToContents()

    # def sortByColumn(self):
    #     """Sort the model by the selected column"""
    #     col = self.view.horizontalHeader().sortIndicatorSection()
    #     order = self.view.horizontalHeader().sortIndicatorOrder()
    #     self.model.sort(col, order)

    def open_deck_widget(self):
        selected_rows = self.selection_model.selectedRows()

        if not selected_rows:
            return
        if len(selected_rows) != 1:
            return

        clicked_row = selected_rows[0]

        selected_deck = self.model.results[clicked_row.row()]

        if selected_deck is None:
            log.error("Selected deck is None")
            QMessageBox.critical(
                self, "Error", "Selected deck not found in the database."
            )
            return

        deck_widget = DeckWidget(selected_deck.id, clicked_row, parent=self)
        deck_widget.show()

    def toggle_buttons_selection(self):
        """Toggle button enabled state based on selection"""
        self.delete_button.setEnabled(self.selection_model.hasSelection())
        self.create_playlist_button.setEnabled(self.selection_model.hasSelection())
        self.export_button.setEnabled(
            self.selection_model.hasSelection()
            and len(self.selection_model.selectedRows()) == 1
        )

    def delete_decks(self):
        del_rows = self.selection_model.selectedRows()
        self.model._delete_rows(del_rows)
        dbtest.print_all_flashcards()
