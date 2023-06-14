from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import (
    QAbstractTableModel,
    QVariant,
    QModelIndex,
    Qt,
)
from sqlalchemy.orm import joinedload
from . import (
    get_scoped_session,
    get_universal_session,
)
import logging
from modules import AlchemizedColumn


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# https://gist.github.com/harvimt/4699169
class AlchemicalTableModel(QAbstractTableModel):
    """A Qt Table Model that binds to an SQL Alchemy ORM."""

    def __init__(self, db_object_model, relationship, columns):
        super().__init__()
        # TODO: session and model might not be needed if just an instance of 'DBInteractions' is passed
        # self.session = session
        self.relationship = relationship
        self.db_object_model = db_object_model

        self._session = get_universal_session()
        self.query = self._session.query(db_object_model)

        log.debug(f"Passed columns: {columns}")
        self.fields: list[AlchemizedColumn] = columns

        self.results = None
        self.count = None
        # self.sort = None
        self._sort_column = None
        self._sort_order = None
        self.filter = None
        # The relation between 'question'->'user' table is done through the foreign key "user_id" on the question table
        # If more foreign keys are added into the Question model, consider changing this conditional
        self.column_name_w_foreign_key = (
            AlchemicalTableModel.get_column_name_w_foreign_key(db_object_model)
        )
        # session.remove()
        self.refresh()

    @property
    def session(self):
        return self._session

    # @property
    # def query(self):
    #     session = self.session
    #     return self.query(self.db_object_model)

    @staticmethod
    def get_column_name_w_foreign_key(model) -> str:
        for column in model.__table__.columns:
            if model.__table__.foreign_keys == column.foreign_keys:
                column_name_w_foreign_key = column.name
                log.debug(f"{column_name_w_foreign_key}")
                return column_name_w_foreign_key
        log.warning(f"No foreign key reference was found for the model: {model}")
        return "UNKNOWN"

    def _delete_rows(self, del_rows):
        success = True

        del_rows.sort(reverse=True)
        for index in del_rows:
            success = self.removeRow(index.row())
            if not success:
                break
        if success:
            log.info("Delete successful")
        else:
            log.error("Delete failed")
        # self.model.refresh()

    def headerData(self, column, orientation, role):
        if role == Qt.ItemDataRole.InitialSortOrderRole:
            self._sort_order = Qt.SortOrder.AscendingOrder
            return Qt.SortOrder.AscendingOrder
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            header = (
                self.fields[column].column_name
                if not self.fields[column].header_display_name
                else self.fields[column].header_display_name
            )
            return QVariant(header)
        return QVariant()

    def setFilter(self, filter):
        """Sets or clears the filter, clear the filter by default is set to None"""
        log.info(f"Setting filter to: {filter}")
        self.filter = filter
        self.refresh()

    def refresh(self, query=None):
        # if query is not None:
        # self.query = query
        # else:
        # session = get_scoped_session()
        # session = self.session
        # self.query = session.query(self.db_object_model)
        session = self.session

        """Recalculates self.results and self.count"""
        log.info("Refreshing the table")
        self.layoutAboutToBeChanged.emit()
        query = self.query
        # if self.sort is not None:
        #     order, column = self.sort
        #     column = self.fields[column].column
        #     if order == Qt.SortOrder.DescendingOrder:
        #         column = column.desc()
        #     else:
        #         column = column.asc()
        # else:
        #     column = None
        if self._sort_column is not None:
            # order, column = self.sort
            column = self._sort_column
            column = self.fields[column].column
            order = self._sort_order
            if order == Qt.SortOrder.DescendingOrder:
                column = column.desc()
            else:
                column = column.asc()
        else:
            column = None

        if self.filter is not None:
            query = query.filter(self.filter)

        if column is not None:
            query = query.order_by(column)

        self.results = query.options(
            joinedload(self.relationship, innerjoin=False)
        ).all()
        # self.results = query.all()

        self.count = query.count()
        self.layoutChanged.emit()
        # session.remove()

    def flags(self, index):
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        # if self.sort is not None:
        #     # order, column = self.sort

        #     if self.fields[column].flags.get("dnd", False) and index.column() == column:
        #         flags |= Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled

        if self.fields[index.column()].flags.get("editable", False):
            flags |= Qt.ItemFlag.ItemIsEditable

        return flags

    def supportedDropActions(self):
        return Qt.DropAction.MoveAction

    def rowCount(self, parent=QModelIndex()):
        return self.count or 0

    def columnCount(self, parent=QModelIndex()):
        return len(self.fields)

    def data(self, index, role):
        if not index.isValid() or role not in (
            Qt.ItemDataRole.DisplayRole,
            Qt.ItemDataRole.EditRole,
        ):
            return QVariant()
        row = self.results[index.row()]
        title = self.fields[index.column()].column_name

        # TODO: find a programmatical way to find the user name reference
        # if title == self.column_name_w_foreign_key:
        #     value = row.Deck.title
        # else:

        value = str(getattr(row, title))

        return QVariant(value)

    def setData(self, index, value, role=None) -> bool:
        session = self.session
        # session = get_scoped_session()

        row = self.results[index.row()]
        name = self.fields[index.column()].column_name

        try:
            setattr(row, name, str(value))
            session.commit()
        except Exception as e:
            QMessageBox.critical(None, "SQL Input Error", str(e))
            # session.remove()
            return False
        else:
            self.dataChanged.emit(index, index)
            # session.remove()
            return True

    def removeRow(self, row):
        if 0 <= row < len(self.results):
            item = self.results[row]
            # session = get_scoped_session()
            session = self.session
            try:
                session.delete(item)
                session.commit()
                # self.refresh()
            except Exception as e:
                QMessageBox.critical(None, "SQL Delete Error", str(e))
                # session.remove()
                return False
            else:
                self.beginRemoveRows(QModelIndex(), row, row)
                del self.results[row]
                self.count -= 1
                self.endRemoveRows()
                # session.remove()
                self.refresh()

                return True

        return False

    def removeRows(self, rows):
        rows.sort(reverse=True)

        for row in rows:
            if 0 <= row < len(self.results):
                item = self.results[row]
                try:
                    session = self.session
                    # session = get_scoped_session()
                    session.delete(item)
                    session.commit()
                    del self.results[row]
                    self.count -= 1
                except Exception as e:
                    QMessageBox.critical(None, "SQL Delete Error", str(e))
                    return False

        self.beginRemoveRows(QModelIndex(), rows[0], rows[-1])
        self.endRemoveRows()
        self.refresh()

        return True

    # def setSorting(self, column, order=Qt.SortOrder.DescendingOrder):
    #     """Sort table by given column number."""
    #     self.sort = order, column
    #     self.refresh()

    def sort(self, column, order):
        sort_enabled = True

        if sort_enabled:
            self._sort_column = column
            self._sort_order = order
            self.layoutAboutToBeChanged.emit()
            super().sort(self._sort_column, self._sort_order)
            self.layoutChanged.emit()
            self.refresh()
