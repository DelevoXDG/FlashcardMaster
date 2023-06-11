from dataclasses import dataclass
from sqlalchemy.sql.schema import Column


@dataclass
class AlchemizedColumn:
    column: Column
    column_name: str
    header_display_name: str = None
    flags: dict = None


from .database_models import *
from .deck_table_model import *
from .flashcard_table_model import *
from .deck_widget import *
