from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, QObject, QAbstractItemModel, Qt, QModelIndex
from PySide2.QtGui import QKeySequence


class DatasetTableView(QTableView):
    """define functionality of table view in dataset dialog"""
    edit_add = Signal([str, int, QObject])

    def __init__(self, parent):
        super(DatasetTableView, self).__init__(parent)
        self.setAttribute(Qt.WA_MacShowFocusRect, 0)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            clipboard_string = QApplication.clipboard().text()
            delimiters = ["\r\n", "\r"]
            for delimiter in delimiters:
                clipboard_string = clipboard_string.replace(delimiter, "\n")
            string_list = clipboard_string.split("\n")

            self.model().change_data(string_list)
        else:
            super().keyPressEvent(event)


class DatasetModel(QAbstractItemModel):
    """define model for variables list views"""

    def __init__(self, data=[]):
        super(DatasetModel, self).__init__()
        self._data = data

    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, *args, **kwargs):
        return 1

    def parent(self, index):
        return QModelIndex()

    def data(self, index, role=None):
        item = self._data[index.row()]

        if role == Qt.DisplayRole:
            return item
        elif role == Qt.EditRole:
            return item

    def headerData(self, section, orientation, role):
        if (orientation == Qt.Horizontal) & (role == Qt.DisplayRole):
            return "Data"
        else:
            header = super().headerData(section, orientation, role)
            return header

    def setData(self, index, value, role=None):
        self._data[index.row()] = value
        self.dataChanged.emit(index, index)
        return True

    def insertRow(self, row, parent=None, *args, **kwargs):
        self._data.insert(row, "")
        return True

    def removeRow(self, row, parent=None, *args, **kwargs):
        del(self._data[row])
        self.dataChanged.emit(self.index(row), self.index(row))
        return True

    def retrieve_data(self):
        return self._data

    def change_data(self, data_list):
        self.beginResetModel()
        self._data = data_list
        self.endResetModel()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
