from . import Deck
from . import (
    get_scoped_session,
    get_universal_session,
)

from . import AlchemizedColumn
from .alchemical_model import AlchemicalTableModel

from PyQt6.QtCore import (
    QVariant,
    Qt,
)

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class DeckTableModel(AlchemicalTableModel):
    def __init__(self):
        col_extra_properties = {
            "title": {"display_name": "Title", "flags": {"editable": False}},
            "Category_id": {"display_name": "Category", "flags": {}},
            "id": {"display_name": "№", "flags": {"editable": False}},
        }

        cols = [
            AlchemizedColumn(
                column=alchemy_col, column_name=alchemy_col.name, flags=dict()
            )
            for alchemy_col in Deck.__table__.columns
        ]

        for col in cols:
            for name, extra_properties in col_extra_properties.items():
                if name == col.column_name:
                    col.header_display_name = extra_properties.get("display_name", "")
                    col.flags = extra_properties.get("flags", dict())
        super().__init__(Deck, Deck.Flashcards, cols)

    def data(self, index, role):
        if not index.isValid() or role not in (
            Qt.ItemDataRole.DisplayRole,
            Qt.ItemDataRole.EditRole,
        ):
            return QVariant()
        row = self.results[index.row()]
        title = self.fields[index.column()].column_name

        if title == self.column_name_w_foreign_key:
            # Get the category name instead of category_id
            value = row.Category.name if row.Category else ""
        else:
            value = str(getattr(row, title))

        return QVariant(value)
