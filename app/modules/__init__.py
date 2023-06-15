from dataclasses import dataclass
import os
from sqlalchemy.sql.schema import Column


@dataclass
class AlchemizedColumn:
    column: Column
    column_name: str
    header_display_name: str = None
    flags: dict = None


from .enums import DifficultyLevel
from .database_models import *
from .deck_table_model import DeckTableModel
from .flashcard_table_model import FlashcardTableModel
from .deck_widget import DeckWidget
from .study_widget import StudyWidget
from .playlist_widget import PlaylistWidget


def full_path(relative_path):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    return cur_dir + os.path.sep + relative_path
