import os

from PyQt6 import QtWidgets, uic

from . import get_universal_session

from .enums import (
    CardType,
    DifficultyLevel,
)

import re

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def is_valid_answer(card_type, answer):
    if card_type == CardType.TrueFalse:
        return answer in ['True', 'False', 'true', 'false', '0', '1', '+', '-']
    elif card_type == CardType.MultipleChoice:
        pattern = r'^\{\s*("[^"\s]+?"\s*:\s*[01]\s*(?:,\s*|\s*\}\s*))*$'
        return re.match(pattern, answer) is not None
    return True  # For card_type == CardType.Text, all answers are valid


def is_true_or_false(answer):
    if answer in ['True', 'true', '1', '+']:
        return "True"
    else:
        return "False"


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

        self.update_placeholder_text()

        self.setup_connections()

    def setup_connections(self):
        self.save_button.clicked.connect(self.update_flashcard)

        # Connect textChanged signals from input fields to the enable_button method
        self.card_type_choice.currentIndexChanged.connect(self.enable_button)
        self.card_type_choice.currentIndexChanged.connect(self.update_placeholder_text)
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

    def update_placeholder_text(self):
        card_type_index = self.card_type_choice.currentIndex()
        if card_type_index == CardType.Text:
            self.question_writing.setPlaceholderText('What is your name?')
            self.answer_writing.setPlaceholderText('Michael')
        elif card_type_index == CardType.TrueFalse:
            self.question_writing.setPlaceholderText('My name is Michael.')
            self.answer_writing.setPlaceholderText('True')
        elif card_type_index == CardType.MultipleChoice:
            self.question_writing.setPlaceholderText('What is your name?')
            self.answer_writing.setPlaceholderText('{"Michael": 1, "Herman": 0, "Maksim": 0,  "Krzysztof": 0}')

    def update_flashcard(self):
        session = get_universal_session()

        card_type = self.card_type_choice.currentIndex()
        question = self.question_writing.text()
        answer = self.answer_writing.text()
        difficulty_level = self.difficulty_choice.currentIndex()

        if not is_valid_answer(card_type, answer):
            log.error("The entered answer is not valid for the selected card type")
            QtWidgets.QMessageBox.critical(self, "Error",
                                           "The entered answer is not valid for the selected card type")
            return

        if card_type == CardType.TrueFalse:
            answer = is_true_or_false(answer)

        self.flashcard.card_type = card_type
        self.flashcard.question = question
        self.flashcard.answer = answer
        self.flashcard.difficulty_level = difficulty_level

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
