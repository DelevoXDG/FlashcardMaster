from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QListView, QLabel, QPushButton
import json

class AnswerWidget(QWidget):
    def __init__(self, answer):
        super().__init__()
        self.answer = answer

    def setup_ui(self):
        pass

    def flip(self):
        pass

class TextAnswerWidget(AnswerWidget):
    def __init__(self, answer):
        super().__init__(answer=answer)
    
    def setup_ui(self):
        layout = QVBoxLayout()

        # Dodajemy etykietę dla odpowiedzi
        self.answer_label = QLabel(self.answer)
        self.answer_label.hide()
        layout.addWidget(self.answer_label)

        self.setLayout(layout)
    
    def flip(self):
        self.answer_label.setVisible(not self.answer_label.isVisible())

class TrueFalseAnswerWidget(AnswerWidget):
    def __init__(self, answer):
        super().__init__(answer=answer)
    
    def setup_ui(self):
        layout = QVBoxLayout()

        self.answer_true_label = QLabel("True")
        self.answer_false_label = QLabel("False")

        layout.addWidget(self.answer_true_label)
        layout.addWidget(self.answer_false_label)

        self.setLayout(layout)
    
    def flip(self):
        if self.answer == "0":
            self.answer_true_label.setVisible(not self.answer_true_label.isVisible())
        else:
            self.answer_false_label.setVisible(not self.answer_false_label.isVisible())

class MultipleChoiceAnswer(AnswerWidget):
    def __init__(self, answer):
        super().__init__(answer=answer)
    
    def setup_ui(self):
        layout = QVBoxLayout()

        self.possibleAnswers = json.loads(self.answer)
        
        self.possible_answer_labels = []
        for key in self.possibleAnswers.keys():
            possible_answer_label = QLabel(key)
            self.possible_answer_labels.append(possible_answer_label)
            layout.addWidget(possible_answer_label)

        self.setLayout(layout)
    
    def flip(self):
        for label in self.possible_answer_labels:
            if self.possibleAnswers[label.text()] == 0:
                label.setVisible(not label.isVisible())
    