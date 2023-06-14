import os

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListView,
    QLabel,
    QTableView,
    QAbstractItemView,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDialog
)

from PyQt6 import uic

from . import (
    Deck,
    Flashcard,
    FlashcardTableModel,
    get_scoped_session,
)

from .playlist import Playlist

class PlaylistWidget(QDialog):
    def __init__(self, deck_ids, parent=None):
        super().__init__(parent)
        self.deck_ids = deck_ids
        self.load_ui()

    def load_ui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "playlist_dialog.ui")
        uic.loadUi(ui_path, self)

        self.difficulty_choice: QComboBox = self.difficulty_choice
        self.study_type_choice: QComboBox = self.study_type_choice
        self.flip_mode_button: QPushButton = self.flip_mode_button
        self.flip_mode_button.setAutoDefault(False)
        self.flip_mode_button.clicked.connect(self.start_study_session)
        self.quiz_mode_button: QPushButton = self.quiz_mode_button
        self.quiz_mode_button.setAutoDefault(False)
        self.quiz_mode_button.setEnabled(False)

    def get_selected_difficulty(self):
        return self.difficulty_choice.currentText()

    def get_selected_study_type(self):
        return self.study_type_choice.currentText()

    def start_study_session(self):
        difficulty = self.get_selected_difficulty()
        study_type = self.get_selected_study_type()
        playlist = Playlist(self.deck_ids, difficulty, study_type)
        # Dalej połączmy ze study_widget
