import sys

from PyQt6.QtWidgets import QApplication
from modules.main_window import MainWindow
from modules.deck_widget import DeckWidget
from modules.models import Base, engine


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
