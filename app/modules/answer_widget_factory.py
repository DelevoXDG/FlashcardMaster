from abc import abstractmethod

from . import enums
from .answer_widget import (
    AnswerWidget,
    TextAnswerWidget,
    TrueFalseAnswerWidget,
    MultipleChoiceAnswer,
)
from PyQt6.QtWidgets import QApplication


class AnswerWidgetFactory:
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def create(self, flashcard, parent=None):
        pass

    @staticmethod
    def get_correct_answer_widget_factory(flashcard):
        if flashcard.card_type == enums.CardType.Text:
            return TextAnswerWidgetFactory()
        elif flashcard.card_type == enums.CardType.TrueFalse:
            return TrueFalseAnswerWidgetFactory()
        else:
            return MultipleChoiceAnswerWidgetFactory()


class TextAnswerWidgetFactory(AnswerWidgetFactory):
    def __init__(self) -> None:
        super().__init__()

    def create(self, flashcard, parent=None):
        return TextAnswerWidget(flashcard.answer, parent)


class TrueFalseAnswerWidgetFactory(AnswerWidgetFactory):
    def __init__(self) -> None:
        super().__init__()

    def create(self, flashcard, parent=None):
        return TrueFalseAnswerWidget(flashcard.answer, parent)


class MultipleChoiceAnswerWidgetFactory(AnswerWidgetFactory):
    def __init__(self) -> None:
        super().__init__()

    def create(self, flashcard, parent=None):
        return MultipleChoiceAnswer(flashcard.answer, parent)


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
    true_false_flashcard = Flashcard("pytanie true false", "False", 1)
    multiple_choice_flashcard = Flashcard(
        "pytanie multiple choice", '{"name":0, "age":0, "car":1}', 2
    )

    factory = AnswerWidgetFactory.get_correct_answer_widget_factory(text_flashcard)
    # factory = AnswerWidgetFactory.getCorrectAnswerWidgetFactory(true_false_flashcard)
    # factory = AnswerWidgetFactory.getCorrectAnswerWidgetFactory(multiple_choice_flashcard)

    widget = factory.create(text_flashcard)
    # widget = factory.create(true_false_flashcard)
    # widget = factory.create(multiple_choice_flashcard)

    widget.show()
    sys.exit(app.exec())
