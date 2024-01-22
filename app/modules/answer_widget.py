from abc import abstractmethod

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QSizePolicy
from PyQt6.QtCore import Qt
import json


class AnswerWidget(QWidget):
    def __init__(self, answer, parent=None):
        super().__init__(parent=parent)
        self.answer = answer
        self.reveal_answer = False
        self.setup_ui()

    @abstractmethod
    def setup_ui(self):
        pass

    @abstractmethod
    def flip(self):
        pass


class TextAnswerWidget(AnswerWidget):
    def __init__(self, answer, parent=None):
        self.hidden_answer_text = "What's you answer?"

        super().__init__(answer=answer, parent=parent)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.text_answer_label = QLabel(self.hidden_answer_text)
        self.text_answer_label.setStyleSheet("font-size: 16px")

        self.text_answer_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.text_answer_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.text_answer_label)

        self.setLayout(layout)

    def flip(self):
        self.reveal_answer = not self.reveal_answer

        if self.reveal_answer:
            self.text_answer_label.setText(self.answer)
        else:
            self.text_answer_label.setText(self.hidden_answer_text)


class TrueFalseAnswerWidget(AnswerWidget):
    def __init__(self, answer, parent=None):
        super().__init__(answer=answer, parent=parent)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.answer_true_label = QLabel("True")
        self.answer_true_label.setStyleSheet("font-size: 16px")

        self.answer_false_label = QLabel("False")
        self.answer_false_label.setStyleSheet("font-size: 16px")

        layout.addWidget(self.answer_true_label)
        layout.addWidget(self.answer_false_label)

        self.setLayout(layout)

    def flip(self):
        if not self.answer == "False":
            self.answer_false_label.setVisible(not self.answer_false_label.isVisible())
        else:
            self.answer_true_label.setVisible(not self.answer_true_label.isVisible())


class MultipleChoiceAnswer(AnswerWidget):
    def __init__(self, answer, parent=None):
        super().__init__(answer=answer, parent=parent)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.possibleAnswers = json.loads(self.answer)

        self.possible_answer_labels = []
        for key in self.possibleAnswers.keys():
            possible_answer_label = QLabel(key)
            possible_answer_label.setStyleSheet("font-size: 16px")
            self.possible_answer_labels.append(possible_answer_label)
            layout.addWidget(possible_answer_label)

        self.setLayout(layout)

    def flip(self):
        for label in self.possible_answer_labels:
            if self.possibleAnswers[label.text()] == 0:
                label.setVisible(not label.isVisible())


# Do testów
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    widget = TextAnswerWidget("text")
    # widget = TrueFalseAnswerWidget("False")
    # widget = MultipleChoiceAnswer('{"name":0, "age":0, "car":1}')
    widget.show()
    sys.exit(app.exec())
