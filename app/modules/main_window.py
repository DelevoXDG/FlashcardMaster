import os
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListView,
    QLabel,
    QHeaderView,
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
from . import (
    Deck,
    Flashcard,
    engine,
    DeckTableModel,
    DeckWidget,
    PlaylistWidget,
)

from .tests import sample_db_data as dbtest

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = DeckTableModel()
        # dbtest.add_sample_decks()
        # dbtest.add_sample_decks_with_categories()
        # dbtest.add_sample_flashcards()
        # dbtest.print_all_flashcards()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "main_window.ui")
        uic.loadUi(ui_path, self)

        self.view: QTableView = self.view
        self.add_button: QPushButton = self.add_button
        self.delete_button: QPushButton = self.delete_button
        self.merge_button: QPushButton = self.merge_button
        self.import_button: QPushButton = self.import_button
        self.export_button: QPushButton = self.export_button
        self.create_playlist_button: QPushButton = self.create_playlist_button
        self.stats_button: QPushButton = self.stats_button

        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.resizeColumnsToContents()
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setSortIndicator(0, Qt.SortOrder.AscendingOrder)

        self.selection_model = self.view.selectionModel()

        self.delete_button.setEnabled(False)
        self.create_playlist_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.merge_button.setEnabled(False)
        self.stats_button.setEnabled(False)

        self.setup_horizontal_header()
        self.model.refresh()
        self.connect_signals()

    def connect_signals(self):
        self.add_button.clicked.connect(self.add_deck)
        self.delete_button.clicked.connect(self.delete_decks)
        self.merge_button.clicked.connect(self.merge_decks)
        self.create_playlist_button.clicked.connect(self.create_playlist)
        self.view.doubleClicked.connect(self.open_selected_deck_widget)
        self.selection_model.selectionChanged.connect(self.toggle_buttons_selection)

    def refresh_model_and_view(self):
        """Refresh the table view and the model - called after any changes to the records in the model"""
        # index = self.model.index(deck_row.row(), 1)
        # self.model.dataChanged.emit(index, index)
        # self.model.refresh()
        # self.view.update()
        # self.view.repaint()
        self.model.refresh()
        self.view.resizeColumnsToContents()

    def setup_horizontal_header(self):
        hh = self.view.horizontalHeader()
        for i in range(0, self.model.columnCount()):
            hh.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # self.view.setColumnWidth(2, 100)
        hh.setMinimumHeight(30)

        bold_font = hh.font()
        bold_font.setBold(True)
        hh.setFont(bold_font)
        hh.setHighlightSections(True)

        return hh

    def open_selected_deck_widget(self):
        """Open a widget in a new window with the single selected deck"""
        selected_deck_rows = self.selection_model.selectedRows()

        if not selected_deck_rows:
            return
        if len(selected_deck_rows) != 1:
            return

        clicked_row = selected_deck_rows[0]
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
        self.merge_button.setEnabled(
            self.selection_model.hasSelection()
            and len(self.selection_model.selectedRows()) >= 2
        )
        self.export_button.setEnabled(
            self.selection_model.hasSelection()
            and len(self.selection_model.selectedRows()) == 1
        )

    def add_deck(self):
        """Add a new empty deck with default title to the database and open related widget in a new window"""
        new_deck = self.model.insertEmptyRecord()

        session = self.model.session
        new_deck.title = new_deck.default_title()
        session.commit()

        self.refresh_model_and_view()

        deck_widget = DeckWidget(new_deck.id, parent=self)
        deck_widget.show()

    def delete_decks(self):
        """Delete selected decks from the database"""
        del_rows = self.selection_model.selectedRows()
        self.model._delete_rows(del_rows)
        dbtest.print_all_flashcards()

    def merge_decks(self):
        """Merge selected playlists into a new playlist, transfering flashcards to the new playlist and deleting the old ones"""
        selected_deck_rows = self.selection_model.selectedRows()

        if not selected_deck_rows or len(selected_deck_rows) < 2:
            return

        selected_decks = [self.model.results[row.row()] for row in selected_deck_rows]
        category_ids = {deck.Category_id for deck in selected_decks}

        if len(category_ids) > 1:
            log.error("Selected decks must have the same category")
            QMessageBox.critical(
                self, "Merge error", "Selected decks must have the same category"
            )
            return

        category_id = category_ids.pop()

        selected_deck_ids = [deck.id for deck in selected_decks]
        self.model.merge_decks(selected_deck_ids, category_id=category_id)

        self.refresh_model_and_view()

    def create_playlist(self):
        """Create a new playlist from selected decks and open the playlist widget in a new window"""
        selected_deck_rows = self.selection_model.selectedRows()

        if not selected_deck_rows:
            return

        selected_decks = [self.model.results[row.row()] for row in selected_deck_rows]
        selected_deck_ids = [deck.id for deck in selected_decks]

        playlist_widget = PlaylistWidget(selected_deck_ids, parent=self)
        playlist_widget.show()
