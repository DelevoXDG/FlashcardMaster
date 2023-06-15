import os
import typing
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QLabel, QMessageBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from .flashcard_widget import FlashcardWidget
from .playlist import Playlist
from . import Flashcard
from . import answer_widget


class StudyWidget(QWidget):
    def __init__(self, playlist, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.Window)

        self.playlist: Playlist = playlist
        self.load_ui()
        self.flipped = False

    def load_ui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ui", "study_widget.ui")
        loadUi(ui_path, self)

        self.correct_button: QPushButton = self.correct_button
        self.wrong_button: QPushButton = self.wrong_button
        self.flashcard_widget: QWidget = self.flashcard_widget
        self.flip_button: QPushButton = self.flip_button

        self.correct_button.clicked.connect(self.correct_button_action)
        self.wrong_button.clicked.connect(self.wrong_button_action)
        self.flip_button.clicked.connect(self.show_buttons)
        self.flip_button.clicked.connect(self.flip)

        self.load_next_flashcard()

    def show_buttons(self):
        # self.correct_button.show()
        # self.wrong_button.show()
        self.correct_button.setEnabled(True)
        self.wrong_button.setEnabled(True)

    def load_next_flashcard(self):
        # self.correct_button.hide()
        # self.wrong_button.hide()
        self.correct_button.setEnabled(False)
        self.wrong_button.setEnabled(False)

        if self.playlist.has_next():
            flashcard = self.playlist.next()
            flashcard_widget = FlashcardWidget(flashcard)
            # flip_button: QPushButton = flashcard_widget.flip_button
            # flip_button.clicked.connect(self.show_buttons)

            layout: QVBoxLayout = self.layout
            placeholder: QWidget = self.flashcard_widget
            layout.replaceWidget(placeholder, flashcard_widget)
            # flashcard_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.flashcard_widget = flashcard_widget
            placeholder.deleteLater()
        else:
            if not len(self.playlist):
                QMessageBox.information(
                    self, "Information", "You finished"
                )
                self.close()
                return
            # label = QLabel("Nothing left")
            # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # layout: QVBoxLayout = self.layout
            # placeholder: QWidget = self.flashcard_widget
            # layout.replaceWidget(placeholder, label)
            # self.flashcard_widget = label
            # placeholder.deleteLater()

    def handle_visibility_button(self):
        upper_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        if self.flipped:
            flip_icon_path = os.path.join(upper_dir, "assets", "hide.png")
        else:
            flip_icon_path = os.path.join(upper_dir, "assets", "visible.png")
        self.flip_button.setIcon(QIcon(flip_icon_path))

    def flip(self):
        self.flipped = not self.flipped
        self.handle_visibility_button()

        self.flashcard_widget.answer_widget.flip()

    def reset_gui(self):
        self.flipped = False
        self.handle_visibility_button()

    def correct_button_action(self):
        self.reset_gui()
        self.playlist.handle_cur(True)
        self.load_next_flashcard()

    def wrong_button_action(self):
        self.reset_gui()
        self.playlist.handle_cur(False)
        self.load_next_flashcard()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    playlist = Playlist([])

    text_flashcard = Flashcard()
    text_flashcard.answer = "cos"
    text_flashcard.card_type = 0
    text_flashcard.question = "pytanie text"

    true_false_flashcard = Flashcard()
    true_false_flashcard.answer = "0"
    true_false_flashcard.card_type = 1
    true_false_flashcard.question = "pytanie true false"

    multiple_choice_flashcard = Flashcard()
    multiple_choice_flashcard.answer = '{"name":0, "age":0, "car":1}'
    multiple_choice_flashcard.card_type = 2
    multiple_choice_flashcard.question = "pytanie multiple choice"

    playlist.flashcard_ids.append(text_flashcard)
    playlist.flashcard_ids.append(true_false_flashcard)
    playlist.flashcard_ids.append(multiple_choice_flashcard)

    widget = StudyWidget(playlist)
    widget.show()
    sys.exit(app.exec())
