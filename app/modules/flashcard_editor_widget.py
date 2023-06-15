import os

from PyQt6 import QtWidgets, uic

from . import get_universal_session

from .enums import (
    CardType,
    DifficultyLevel,
)


class FlashcardEditorWidget(QtWidgets.QDialog):
    def __init__(self, flashcard, parent=None):
        super().__init__(parent)
        self.flashcard = flashcard
        self.load_ui()

    def load_ui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "flashcard_dialog.ui")
        uic.loadUi(ui_path, self)

        self.card_type_choice: QtWidgets.QComboBox = self.card_type_choice
        self.question_writing: QtWidgets.QLineEdit = self.question_writing
        self.answer_writing: QtWidgets.QLineEdit = self.answer_writing
        self.difficulty_choice: QtWidgets.QComboBox = self.difficulty_choice
        self.add_card_button: QtWidgets.QPushButton = self.add_card_button

        # Fill the form with the current flashcard's data
        self.card_type_choice.setCurrentText(CardType.get_name(self.flashcard.card_type))
        self.question_writing.setText(self.flashcard.question)
        self.answer_writing.setText(self.flashcard.answer)
        self.difficulty_choice.setCurrentText(DifficultyLevel.get_name(self.flashcard.difficulty_level))

        self.setup_connections()

    def setup_connections(self):
        self.add_card_button.clicked.connect(self.update_flashcard)

        # Connect textChanged signals from input fields to the enable_button method
        self.card_type_choice.currentIndexChanged.connect(self.enable_button)
        self.question_writing.textChanged.connect(self.enable_button)
        self.answer_writing.textChanged.connect(self.enable_button)
        self.difficulty_choice.currentIndexChanged.connect(self.enable_button)

    def enable_button(self):
        if all([self.card_type_choice.currentText(),
                self.question_writing.text(),
                self.answer_writing.text(),
                self.difficulty_choice.currentText()]):
            self.add_card_button.setEnabled(True)
        else:
            self.add_card_button.setEnabled(False)

    def update_flashcard(self):
        self.flashcard.card_type = CardType.get_name(self.card_type_choice.currentText())
        self.flashcard.question = self.question_writing.text()
        self.flashcard.answer = self.answer_writing.text()
        self.flashcard.difficulty_level = DifficultyLevel.get_name(self.difficulty_choice.currentText())

        session = get_universal_session()  # or another way you obtain the session
        session.add(self.flashcard)
        session.commit()

        # Close the dialog after saving the flashcard
        self.close()
