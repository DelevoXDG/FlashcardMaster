import sys

from PyQt6.QtWidgets import QApplication
from modules.main_window import MainWindow
from modules.deck_widget import DeckWidget
from modules.models import Base, engine

# Create the database tables (if they don't exist)
# Base.metadata.create_all(engine)


def main():
    app = QApplication(sys.argv)
    # Create the application

    # Create the main window
    window = MainWindow()
    window.show()

    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
