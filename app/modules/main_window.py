from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListView,
    QLabel,
    QTableView,
    QAbstractItemView,
)

from PyQt6.QtGui import QStandardItemModel, QStandardItem

import sys
import os
from sqlalchemy.orm import sessionmaker


# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

from .models import Deck
from .models import engine
from .alchemical_model import AlchemicalTableModel
from .deck_model import get_deck_table_model

# from modules.deck_widget import DeckWidget


# class DeckTableModel(QStandardItemModel):
#     def __init__(self, decks):
#         super().__init__()
#         self.decks = decks

#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             deck = self.decks[index.row()]
#             return deck.title


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard Master")

        self.setFixedSize(700, 480)
        self.model = get_deck_table_model()
        self.model.refresh()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()

        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

        self.layout = layout
        self.setLayout(self.layout)

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
