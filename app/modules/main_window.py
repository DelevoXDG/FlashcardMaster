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
from PyQt6 import uic


from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)

import sys
import os
from sqlalchemy.orm import sessionmaker


# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

from .models import Deck
from .models import engine
from . import DeckTableModel

# from modules.deck_widget import DeckWidget


from tests.sample_db_data import add_sample_decks


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard Master")
        # self.setFixedSize(700, 480)

        self.model = DeckTableModel()
        # self.view = QTableView()
        # self.view.setModel(self.model)
        # main_widget = QWidget(self)
        # layout = QVBoxLayout(main_widget)
        # main_widget.setLayout(layout)
        # self.setCentralWidget(main_widget)
        # test_adding_decks()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "main_window.ui")
        uic.loadUi(ui_path, self)
        # self.setDocumentMode(True)
        # self.model = DeckTableModel()
        self.view.setModel(self.model)
        # self.view.setFixedSize(QSize(400, 250))
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.resizeColumnsToContents()
        # self.view.setColumnHidden(0, True)
        self.model.refresh()
        # layout.addWidget(self.view)

        # self.layout = layout
        # self.setLayout(self.layout)

    # def __init__(self):
    #     super().__init__()

    #     self.setWindowTitle("Flashcard Management App")

    #     main_widget = QWidget(self)
    #     layout = QVBoxLayout(main_widget)

    #     label = QLabel("Deck Collection")
    #     layout.addWidget(label)

    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     # deck1 = Deck(title="Mathematics")
    #     # deck2 = Deck(title="History")
    #     # deck3 = Deck(title="Science")
    #     # session.add_all([deck1, deck2, deck3])
    #     # session.commit()
    #     # all_deck_widget = QWidget(self)
    #     # Create a QListView to display the decks

    #     deck_list_view = QListView(self)
    #     layout.addWidget(deck_list_view)

    #     model = QStandardItemModel(self)
    #     deck_list_view.setModel(model)

    #     decks = session.query(Deck).all()

    #     for deck in decks:
    #         # deck_widget = DeckWidget(deck)
    #         # deck_widget.show()
    #         # deck_layout.addWidget(deck_widget)

    #         item = QStandardItem(deck.title)
    #         model.appendRow(item)

    #     session.close()
    #     main_widget.setLayout(layout)
    #     self.setCentralWidget(main_widget)
