import os
import typing
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
)
from PyQt6.uic import loadUi
from .answer_widget_factory import AnswerWidgetFactory


class FlashcardWidget(QWidget):
    def __init__(self, flashcard, parent=None):
        super().__init__(parent)
        self.flashcard = flashcard
        self.load_ui()

    def load_ui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "flashcard_widget.ui")

        loadUi(ui_path, self)
        answer_widget_factory = AnswerWidgetFactory.get_correct_answer_widget_factory(
            self.flashcard
        )

        self.layout: QVBoxLayout = self.layout
        self.question_label: QLabel = self.question_label
        self.answer_widget: QWidget = self.answer_widget
        # self.question_label: QLabel = self.frame_1.question_label
        # self.answer_widget: QWidget = self.frame_2.answer_widget

        self.question_label.setText(self.flashcard.question)

        answer_widget = answer_widget_factory.create(self.flashcard, parent=self)
        # answer_widget.setParent(self.answer_widget)

        placeholder: QWidget = self.answer_widget
        self.layout.replaceWidget(placeholder, answer_widget)
        self.answer_widget = answer_widget

        # TrueFalseAnswerWidget("0", self.answer_widget)
        # self.answer_widget = answer_widget

        # self.flip_button.clicked.connect(answer_widget.flip)


# Do testów
if __name__ == "__main__":

    class Flashcard:
        def __init__(self, question, answer, card_type) -> None:
            self.question = question
            self.answer = answer
            self.card_type = card_type

    import sys

    app = QApplication(sys.argv)

    text_flashcard = Flashcard("pytanie text", "odpowiedz text", 0)
    true_false_flashcard = Flashcard("pytanie true false", "0", 1)
    multiple_choice_flashcard = Flashcard(
        "pytanie multiple choice", '{"name":0, "age":0, "car":1}', 2
    )

    widget = FlashcardWidget(text_flashcard)
    # widget = FlashcardWidget(true_false_flashcard)
    # widget = FlashcardWidget(multiple_choice_flashcard)

    widget.show()
    app.exec()
