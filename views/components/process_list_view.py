from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, QObject, QAbstractListModel, Qt, QModelIndex


class ProcessListView(QListView):
    """define functionality of list views in process dialog"""
    edit_add = Signal([str, int, QObject])

    def __init__(self, parent):
        super(ProcessListView, self).__init__(parent)
        self.setAttribute(Qt.WA_MacShowFocusRect, 0)

    def contextMenuEvent(self, event):
        """define context menu within list view
        - add
        - edit
        - delete"""
        local_position = event.pos()
        global_position = event.globalPos()
        item = self.indexAt(local_position)
        context_menu = QMenu()
        if item.isValid():
            edit_action = context_menu.addAction("Edit")
            edit_action.triggered.connect(lambda: self.edit_add.emit("Edit", item.row(), self.model()))
            delete_action = context_menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self.model().removeRow(item.row()))
        add_action = context_menu.addAction("Add")
        add_action.triggered.connect(lambda: self.edit_add.emit("Add", QModelIndex(), self.model()))

        context_menu.exec_(global_position)


class ListModel(QAbstractListModel):
    """define model for variables list views"""

    def __init__(self, data=[]):
        super(ListModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def data(self, index, role=None):
        item = self._data[index.row()]
        # turn display name to model name for objective function and constraints
        display_name = item if isinstance(item, str) else item.name
        model_name = display_name.lower().replace(" ", "_")

        if role == Qt.DisplayRole:
            return model_name
        elif role == Qt.EditRole:
            return model_name

    def setData(self, index, value, role=None):
        self._data[index.row()] = value
        self.dataChanged.emit(index, index)
        return True

    def insertRow(self, row, parent=None, *args, **kwargs):
        self._data.insert(row, "")
        return True

    def removeRow(self, row, parent=None, *args, **kwargs):
        self._data.remove(self._data[row])
        self.dataChanged.emit(self.index(row), self.index(row))
        return True

    def retrieve_data(self):
        return self._data

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsAutoTristate
