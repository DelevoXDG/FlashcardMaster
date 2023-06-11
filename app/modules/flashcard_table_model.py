from . import Flashcard
from . import get_scoped_session

from . import AlchemizedColumn
from .alchemical_model import AlchemicalTableModel
from PyQt6.QtCore import (
    Qt,
    QVariant,
)

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class FlashcardTableModel(AlchemicalTableModel):
    def __init__(self, deck_id):
        self.deck_id = deck_id

        col_extra_properties = {
            "question": {"display_name": "Question", "flags": {"editable": True}},
            "difficulty_level": {
                "display_name": "Difficulty",
                "flags": {"editable": True},
            },
        }

        cols = [
            AlchemizedColumn(
                column=alchemy_col, column_name=alchemy_col.name, flags=dict()
            )
            for alchemy_col in Flashcard.__table__.columns
        ]

        for col in cols:
            for name, extra_properties in col_extra_properties.items():
                if name == col.column_name:
                    col.header_display_name = extra_properties.get("display_name", "")
                    col.flags = extra_properties.get("flags", dict())

        super().__init__(Flashcard, Flashcard.Deck, cols)
        # self.setFilter({"Deck_id": self.deck_id})

    def refresh(self):
        self.layoutAboutToBeChanged.emit()
        session = get_scoped_session()
        query = session.query(Flashcard)

        query = query.filter_by(Deck_id=self.deck_id)

        # filter_var = Deck_id = self.deck_id

        # self.fields = self.cols

        super().refresh(query)
        session.remove()

    def data(self, index, role):
        if not index.isValid() or role not in (
            Qt.ItemDataRole.DisplayRole,
            Qt.ItemDataRole.EditRole,
        ):
            return QVariant()
        row = self.results[index.row()]
        title = self.fields[index.column()].column_name
        column = self.fields[index.column()].column

        if title == "difficulty_level":
            # Get the category name instead of category_id
            value = {0: "easy", 1: "medium", 2: "hard"}.get(
                int(getattr(row, title)), ""
            )
        else:
            value = str(getattr(row, title))

        return QVariant(value)
