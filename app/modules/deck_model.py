from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QColor, QPixmap

from modules.models import Deck

from modules import AlchemizedModelColumn
from .models import Flashcard
from .models import get_scoped_session
from .alchemical_model import AlchemicalTableModel


def get_deck_table_model():
    """Return a list of tuples on which each tuple is composed of:
    (column: sqlalchemy.sql.schema.Column,
        sql_alchemy_column_name: str,
        header_display_name: str,
        flags: dict)
    """
    # TODO: have this as a constant at the top of this module
    # Basically changing a column name to be something else

    column_extra_header_display_flags = {
        "created_ts": {"display_name": "Asked@", "flags": {"editable": True}}
    }

    columns = [
        AlchemizedModelColumn(column=column, column_name=column.name, flags=dict())
        for column in Flashcard.__table__.columns
    ]

    # for column in columns:
    #     for column_name, extra_values in column_extra_header_display_flags.items():
    #         if column_name == column.column_name:
    #             column.header_display_name = extra_values.get("display_name", "")
    #             column.flags = extra_values.get("flags", dict())

    return AlchemicalTableModel(
        session=get_scoped_session(),
        model=Deck,
        relationship=Deck.Flashcards,
        columns=columns,
    )
