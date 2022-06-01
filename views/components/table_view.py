from PySide2.QtWidgets import *
from PySide2.QtCore import *


class TableView(QTableView):
    """define hover functionality of TableView"""
    hover_index_changed = Signal(QModelIndex)

    def __init__(self, parent):
        super(TableView, self).__init__(parent)
        self.hover_index = QModelIndex()

    def mouseMoveEvent(self, event):
        """define view index of mouse over for delete buttons"""
        index = self.indexAt(event.pos())
        if self.hover_index != index:
            self.hover_index = index
            self.hover_index_changed.emit(index)

    def leaveEvent(self, event):
        """define leave event to reset view index of mouse over"""
        self.hover_index_changed.emit(QModelIndex())
