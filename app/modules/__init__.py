from dataclasses import dataclass
from sqlalchemy.sql.schema import Column

from .database_models import *


@dataclass
class AlchemizedColumn:
    column: Column
    column_name: str
    header_display_name: str = None
    flags: dict = None


from .deck_table_model import DeckTableModel
