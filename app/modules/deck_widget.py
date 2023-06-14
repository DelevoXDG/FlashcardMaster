import os
from PyQt6.QtWidgets import (
    QWidget,
    QTableView,
    QAbstractItemView,
    QPushButton,
    QLineEdit,
    QComboBox,
)
from PyQt6.QtCore import QSize, QItemSelectionModel, Qt

from PyQt6 import uic
from . import (
    Deck,
    Flashcard,
    FlashcardTableModel,
    get_scoped_session,
    get_universal_session,
)

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class DeckWidget(QWidget):
    def __init__(
        self,
        deck_id,
        deck_row=None,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.Window)

        session = get_universal_session()
        self.deck = session.query(Deck).filter_by(id=deck_id).first()
        self.deck_row = deck_row

        self.model = FlashcardTableModel(deck_id)
        self.set_window_title(self.deck.title)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "deck_widget.ui")
        uic.loadUi(ui_path, self)

        self.view: QTableView = self.view
        self.add_button: QPushButton = self.add_button
        self.delete_button: QPushButton = self.delete_button
        self.name_line: QLineEdit = self.name_line
        self.category_combo_box: QComboBox = self.category_combo_box
        self.save_button: QPushButton = self.save_button

        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_deck_name)
        self.name_line.setText(self.deck.title)
        self.name_line.textChanged.connect(self.enable_save_button)

        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.resizeColumnsToContents()
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        self.view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        self.selection_model = self.view.selectionModel()

        self.model.refresh()

        columns_to_hide = set(["Deck_id"])
        self.hide_columns_by_name(columns_to_hide)

    def hide_columns_by_name(self, column_names):
        header = self.view.horizontalHeader()

        for i, column_index in enumerate(Flashcard.__table__.columns):
            if column_index.name in column_names:
                header.hideSection(i)

    def set_window_title(self, deck_title):
        self.setWindowTitle(f"Deck editor: {deck_title}")

    def enable_save_button(self, text):
        current_name = self.deck.title
        text = self.name_line.text()

        if text != current_name:
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def save_deck_name(self):
        new_name = self.name_line.text()
        if not new_name:
            log.warning("Deck name cannot be empty.")
            return

        if new_name == self.deck.title:
            log.info("No changes made to the deck name.")
            self.save_button.setEnabled(False)
            return

        try:
            session = get_universal_session()

            self.deck = session.query(Deck).filter_by(id=self.deck.id).first()
            self.deck.title = new_name
            # session.query(Deck).filter_by(id=self.deck.id).update(
            #     {Deck.title: new_name}
            # )
            session.commit()
            # session.refresh(self.deck)
            # session.flush()
            # session.remove()
        except Exception as e:
            log.error(f"Failed to save deck name: {str(e)}")
        else:
            if self.parent() is not None:
                self.parent().refresh_deck_table()

            self.set_window_title(self.deck.title)
            log.info("Deck name saved successfully")
            self.save_button.setEnabled(False)
