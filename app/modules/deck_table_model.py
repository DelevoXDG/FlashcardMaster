from . import (
    Deck,
    Flashcard,
    AlchemizedColumn,
    get_scoped_session,
    get_universal_session,
)

from .alchemical_model import AlchemicalTableModel

from PyQt6.QtCore import (
    QModelIndex,
    QVariant,
    Qt,
)
import sqlalchemy
from sqlalchemy.orm import joinedload

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class DeckTableModel(AlchemicalTableModel):
    def __init__(self):
        col_extra_properties = {
            "title": {"display_name": "Title", "flags": {"editable": False}},
            "Category_id": {"display_name": "Category", "flags": {}},
            "id": {"display_name": "№", "flags": {"editable": False}},
            "flashcards_count": {"display_name": "Count", "flags": {"editable": False}},
        }

        cols = [
            AlchemizedColumn(
                column=alchemy_col, column_name=alchemy_col.name, flags=dict()
            )
            for alchemy_col in Deck.__table__.columns
        ]
        cols.append(
            AlchemizedColumn(column=None, column_name="flashcards_count", flags=dict())
        )

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
        elif title == "flashcards_count":
            deck_id = getattr(row, "id")
            flashcards_count = (
                self.session.query(Flashcard)
                .filter(Flashcard.Deck_id == deck_id)
                .count()
            )
            value = str(flashcards_count)
        else:
            value = str(getattr(row, title))

        return QVariant(value)

    def merge_decks(self, deck_ids, category_id=None, title=None):
        """
        Merge decks into a new deck
        """
        new_deck: Deck = self.insertEmptyRecord()

        session = self.session
        if category_id is None:
            category_id = sqlalchemy.null()
        if title is None:
            title = new_deck.default_title()

        new_deck.Category_id = category_id
        new_deck.title = title

        session.commit()

        flashcards_to_update = (
            session.query(Flashcard).filter(Flashcard.Deck_id.in_(deck_ids)).all()
        )
        for flashcard in flashcards_to_update:
            flashcard.Deck_id = new_deck.id
        session.commit()

        for deck_id in deck_ids:
            deck = session.query(Deck).filter_by(id=deck_id).first()
            if deck:
                session.delete(deck)
        session.commit()

        self.refresh()

        return new_deck

    def columnCount(self, parent=...):
        return super().columnCount(parent)

    def refresh(self):
        # if query is not None:
        # self.query = query
        # else:
        # session = get_scoped_session()
        # session = self.session
        # self.query = session.query(self.db_object_model)
        session = self.session

        """Recalculates self.results and self.count"""
        log.info("Refreshing the table")
        self.layoutAboutToBeChanged.emit()
        query = self.query
        alch_col = None
        if self._sort_column is not None:
            # order, column = self.sort
            # alchemical_col = self._sort_column
            alchemized_col = self.fields[self._sort_column]
            col_name = alchemized_col.column_name
            order = self._sort_order
            # if col_name == "flashcards_count":
            #     # subquery = (
            #     #     session.query(
            #     #         Flashcard.Deck_id,
            #     #         sqlalchemy.func.count(Flashcard.id).label("flashcards_count"),
            #     #     )
            #     #     .group_by(Flashcard.Deck_id)
            #     #     .subquery()
            #     # )
            #     # alch_col = sqlalchemy.case(
            #     #     (subquery.c.Deck_id.is_(None), 0), else_=subquery.c.flashcards_count
            #     # )
            #     # # alch_col = alchemized_col.column
            #     # if order == Qt.SortOrder.DescendingOrder:
            #     #     alch_col = alch_col.desc()
            #     # else:
            #     #     alch_col = alch_col.asc()
            # else:
            #     alch_col = alchemized_col.column
            #     if order == Qt.SortOrder.DescendingOrder:
            #         alch_col = alch_col.desc()
            #     else:
            #         alch_col = alch_col.asc()

            # if col_name == "flashcards_count":
            #     alch_col = sqlalchemy.func.count(Flashcard.id)
            # else:
            #     alch_col = alchemized_col.column

            # if order == Qt.SortOrder.DescendingOrder:
            #     alch_col = alch_col.desc()
            # else:
            #     alch_col = alch_col.asc()
            if col_name == "flashcards_count":
                flashcards_count = sqlalchemy.func.count(Flashcard.id).label(
                    "flashcards_count"
                )
                query = query.outerjoin(Flashcard).group_by(self.db_object_model.id)

                if order == Qt.SortOrder.DescendingOrder:
                    query = query.order_by(flashcards_count.desc())
                else:
                    query = query.order_by(flashcards_count)
            else:
                alch_col = alchemized_col.column

                if order == Qt.SortOrder.DescendingOrder:
                    query = query.order_by(alch_col.desc())
                else:
                    query = query.order_by(alch_col)
        else:
            alch_col = None

        if self.filter is not None:
            query = query.filter(self.filter)

        if alch_col is not None:
            query = query.order_by(alch_col)

        self.results = query.options(
            joinedload(self.relationship, innerjoin=False)
        ).all()
        # self.results = query.all()

        self.count = query.count()
        self.layoutChanged.emit()
