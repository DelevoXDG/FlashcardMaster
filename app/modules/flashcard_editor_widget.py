import os

from PyQt6 import QtWidgets, uic

from . import get_universal_session

from .enums import (
    CardType,
    DifficultyLevel,
)


class FlashcardEditorWidget(QtWidgets.QDialog):
    def __init__(self, flashcard, newCard, parent=None):
        super().__init__(parent)
        self.flashcard = flashcard
        self.newCard = newCard
        self.saved = False
        self.load_ui()

    def load_ui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "flashcard_dialog.ui")
        uic.loadUi(ui_path, self)

        self.card_type_choice: QtWidgets.QComboBox = self.card_type_choice
        self.question_writing: QtWidgets.QLineEdit = self.question_writing
        self.answer_writing: QtWidgets.QLineEdit = self.answer_writing
        self.difficulty_choice: QtWidgets.QComboBox = self.difficulty_choice
        self.save_button: QtWidgets.QPushButton = self.save_button
        self.save_button.setEnabled(False)

        # Fill the form with the current flashcard's data
        self.card_type_choice.setCurrentIndex(self.flashcard.card_type)
        self.question_writing.setText(self.flashcard.question)
        self.answer_writing.setText(self.flashcard.answer)
        self.difficulty_choice.setCurrentIndex(self.flashcard.difficulty_level)

        self.setup_connections()

    def setup_connections(self):
        self.save_button.clicked.connect(self.update_flashcard)

        # Connect textChanged signals from input fields to the enable_button method
        self.card_type_choice.currentIndexChanged.connect(self.enable_button)
        self.question_writing.textChanged.connect(self.enable_button)
        self.answer_writing.textChanged.connect(self.enable_button)
        self.difficulty_choice.currentIndexChanged.connect(self.enable_button)

    def enable_button(self):
        if all(
            [
                self.card_type_choice.currentText(),
                self.question_writing.text(),
                self.answer_writing.text(),
                self.difficulty_choice.currentText(),
            ]
        ):
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def update_flashcard(self):
        session = get_universal_session()

        self.flashcard.card_type = self.card_type_choice.currentIndex()
        self.flashcard.question = self.question_writing.text()
        self.flashcard.answer = self.answer_writing.text()
        self.flashcard.difficulty_level = self.difficulty_choice.currentIndex()

        session.commit()

        self.saved = True
        self.close()

    def closeEvent(self, event):
        if not self.saved and self.newCard:
            session = get_universal_session()
            session.delete(self.flashcard)
            session.commit()

        if (
            self.parent() is not None
            and self.parent().refresh_model_and_view is not None
        ):
            self.parent().refresh_model_and_view()

        super().close()
