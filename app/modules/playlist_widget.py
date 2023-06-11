from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListView,
    QLabel,
    QTableView,
    QAbstractItemView,
    QPushButton,
    QLineEdit,
    QComboBox,
)


class PlaylistWidget(QWidget):
    def __init__(self, decks, parent=None):
        super().__init__(parent)
