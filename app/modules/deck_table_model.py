from . import Deck
from . import get_scoped_session

from . import AlchemizedColumn
from .alchemical_model import AlchemicalTableModel

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class DeckTableModel(AlchemicalTableModel):
    def __init__(self):
        col_extra_properties = {
            "title": {"display_name": "Title", "flags": {"editable": True}}
        }

        cols = [
            AlchemizedColumn(column=col, column_name=col.name, flags=dict())
            for col in Deck.__table__.columns
        ]

        for col in cols:
            for name, extra_values in col_extra_properties.items():
                if name == col.column_name:
                    col.header_display_name = extra_values.get("display_name", "")
                    col.flags = extra_values.get("flags", dict())

        session = get_scoped_session()
        super().__init__(session, Deck, Deck.Flashcards, cols)

    def delete_rows(self, del_rows):
        success = True

        del_rows.sort(reverse=True)
        for index in del_rows:
            success = self.removeRow(index.row())
            if not success:
                break
        if success:
            log.info("Delete successful")
        else:
            log.error("Delete failed")
        # self.model.refresh()
