from collections import OrderedDict
import os
from PyQt6.QtWidgets import (
    QWidget,
    QTableView,
    QAbstractItemView,
    QPushButton,
    QLineEdit,
    QComboBox,
    QInputDialog,
)
from PyQt6.QtCore import QSize, QItemSelectionModel, Qt

from PyQt6 import uic
import sqlalchemy

from .enums import (
    CardType,
    DifficultyLevel,
)
from . import (
    Deck,
    Flashcard,
    Category,
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

        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "deck_widget.ui")
        uic.loadUi(ui_path, self)

        self.view: QTableView = self.view
        self.add_button: QPushButton = self.add_button
        self.delete_button: QPushButton = self.delete_button
        self.name_line: QLineEdit = self.name_line
        self.category_combo_box: QComboBox = self.category_combo_box
        self.save_button: QPushButton = self.save_button

        session = get_universal_session()
        deck = session.query(Deck).filter_by(id=deck_id).first()
        self.deck = deck
        self.deck_row = deck_row

        self.model = FlashcardTableModel(deck_id)

        self.set_window_title(deck.title)

        self.save_button.setEnabled(False)
        self.name_line.setText(deck.title)

        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.resizeColumnsToContents()
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setSortIndicator(0, Qt.SortOrder.AscendingOrder)

        self.selection_model = self.view.selectionModel()

        self.load_categories()
        self.load_deck_category()

        self.model.refresh()

        columns_to_hide = set(["Deck_id"])
        self.hide_columns_by_name(columns_to_hide)

        self.connect_signals()

    def connect_signals(self):
        self.save_button.clicked.connect(self.save_deck_name)
        self.save_button.clicked.connect(self.save_deck_category)

        self.name_line.textChanged.connect(self.enable_save_button)
        self.category_combo_box.currentIndexChanged.connect(self.enable_save_button)
        self.category_combo_box.currentIndexChanged.connect(self.handle_category_change)

        self.add_button.clicked.connect(self.add_flashcard)
        self.delete_button.clicked.connect(self.delete_selected_flashcards)

    def hide_columns_by_name(self, column_names):
        header = self.view.horizontalHeader()

        for i, column_index in enumerate(Flashcard.__table__.columns):
            if column_index.name in column_names:
                header.hideSection(i)

    def set_window_title(self, deck_title):
        self.setWindowTitle(f"Deck editor: {deck_title}")

    def refresh_model_and_view(self):
        """Refresh the table view and the model - called after any changes to the records in the model"""

        self.model.refresh()
        self.view.resizeColumnsToContents()
        if (
            self.parent() is not None
            and self.parent().refresh_model_and_view is not None
        ):
            self.parent().refresh_model_and_view()

    def enable_save_button(self, new_name):
        cur_name = self.deck.title
        new_name = self.name_line.text()

        cur_category_id = self.deck.Category_id
        new_category_id = self.category_combo_box.currentData()

        cur_properties = [cur_name, cur_category_id]
        new_properties = [new_name, new_category_id]

        if cur_properties != new_properties:
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

        except Exception as e:
            log.error(f"Failed to save deck name: {str(e)}")
        else:
            if (
                self.parent() is not None
                and self.parent().refresh_model_and_view is not None
            ):
                self.parent().refresh_model_and_view()

            self.set_window_title(self.deck.title)
            log.info("Deck name saved successfully")
            self.save_button.setEnabled(False)

    def load_categories(self):
        session = (
            self.model.session if self.model is not None else get_universal_session()
        )

        categories = session.query(Category).all()

        self.category_combo_box.clear()

        for category in categories:
            self.category_combo_box.addItem(category.name, userData=category.id)

    @property
    def _add_category_text(self):
        return "+ Add Category"

    @property
    # def _reserved_category_names(self):
    #     return {0: (self._add_category_text, None), 1: ("None", sqlalchemy.null())}
    def _reserved_category_names(self):
        return OrderedDict(
            {
                "None": {"index": 0, "userData": sqlalchemy.null()},
                self._add_category_text: {"index": 1, "userData": None},
            }
        )

    def load_categories(self):
        self.delete_unused_categories()
        session = (
            self.model.session if self.model is not None else get_universal_session()
        )

        categories = session.query(Category).all()

        self.category_combo_box.clear()

        # self.category_combo_box.addItem(self._add_category_text, userData=None)
        # self.category_combo_box.addItem("None", userData=sqlalchemy.null())
        for category_name, category_data in self._reserved_category_names.items():
            self.category_combo_box.addItem(
                category_name, userData=category_data["userData"]
            )

        for category_data in categories:
            self.category_combo_box.addItem(
                category_data.name, userData=category_data.id
            )

    def load_deck_category(self):
        category = self.deck.Category

        if category is not None:
            index = self.category_combo_box.findData(category.id)

            special_indexes = [-1]
            special_indexes.extend(
                [x for x in range(0, len(self._reserved_category_names))]
            )

            if index not in special_indexes:
                self.category_combo_box.setCurrentIndex(index)
            else:
                self.category_combo_box.setCurrentIndex(1)

    def handle_category_change(self):
        selected_index = self.category_combo_box.currentIndex()
        if (
            selected_index
            == self._reserved_category_names[self._add_category_text]["index"]
        ):
            self.add_category()

    def add_category(self):
        category_name, ok = QInputDialog.getText(
            self,
            "Create Category",
            "Enter category name:",
        )
        if ok and category_name:
            session = (
                self.model.session
                if self.model is not None
                else get_universal_session()
            )
            category = Category(name=category_name)

            session.add(category)
            session.commit()
            self.category_combo_box.addItem(category.name, category.id)
            new_category_combo_box_index = self.category_combo_box.count() - 1
            self.category_combo_box.setCurrentIndex(new_category_combo_box_index)

    def delete_unused_categories(self):
        """Delete categories that are not assigned to any decks."""
        session = (
            self.model.session if self.model is not None else get_universal_session()
        )

        unused_categories = session.query(Category).filter(~Category.Decks.any()).all()

        for category in unused_categories:
            session.delete(category)

        session.commit()
        log.info("Unused categories deleted")
        if len(unused_categories) > 0:
            # self.load_categories()
            index = self.category_combo_box.findData(category.id)
            if index != -1:
                self.category_combo_box.removeItem(index)

    def save_deck_category(self):
        session = (
            self.model.session if self.model is not None else get_universal_session()
        )

        category_id = self.category_combo_box.currentData()
        if category_id is None:
            log.warning("Category cannot be empty.")
            return
        else:
            if self.deck.Category_id == category_id:
                log.info("No changes made to the deck category.")
                return

            self.deck.Category_id = category_id
            session.commit()
            self.delete_unused_categories()

            log.info("Deck category saved successfully")
            self.save_button.setEnabled(False)

    def add_flashcard(self):
        """Add a new empty flashcard with default title to the database and open related widget in a new window"""
        session = (
            self.model.session if self.model is not None else get_universal_session()
        )
        new_flascard = Flashcard(
            Deck_id=self.deck.id,
            card_type=CardType.Text,
            difficulty_level=DifficultyLevel.Medium,
        )
        session.add(new_flascard)
        session.commit()

        self.refresh_model_and_view()
        # TODO open flashcard editor widget in a new window

    def delete_selected_flashcards(self):
        """Delete selected flashcards from the database"""
        del_rows = self.selection_model.selectedRows()
        self.model._delete_rows(del_rows)

    def close(self):
        self.delete_unused_categories()

        super().close()
