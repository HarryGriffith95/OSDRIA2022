from math import ceil

from PySide2.QtCore import QRect, QSize, Qt, QAbstractTableModel, QMimeData, QByteArray
from PySide2.QtGui import QPainter, QStandardItemModel, QStandardItem, QPen
from PySide2.QtWidgets import *

from models.constants import PropType, MimeType
from views.draftbar_element_view_ui import Ui_DraftElement

LIST_HEIGHT = 100
ELEMENT_COLUMN_NUMBER = 3
ELEMENT_SIZE = 30


class DraftbarElementView(QWidget):
    """view of draft element category in sidebar"""

    def __init__(self, parent, category_name, element_model, element_controller):
        super(DraftbarElementView, self).__init__(parent)

        self._category = category_name
        self._model = element_model
        self._ctrl = element_controller
        self._ui = Ui_DraftElement()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        self._ui.dropdown_button.hide()
        #self._ui.element_label.clicked.connect(self.toggle_list)
        #self._ui.dropdown_button.clicked.connect(self.toggle_list)

        """listen for model event signals"""

        """initialize view"""
        self._ui.element_label.setText(str(self._category))
        list_model = ElementListModel(self)
        list_model.set_model(self._model)
        self._ui.element_list.setModel(list_model)
        self.toggle_list()

    def toggle_list(self):
        """show or hide element list"""
        # todo toggle list


class ElementListModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(ElementListModel, self).__init__(parent)
        self._thumbnail_size = QSize(ELEMENT_SIZE, ELEMENT_SIZE)
        self._model = None

    def set_model(self, model):
        self._model = model

    def rowCount(self, parent=None, *args, **kwargs):
        return ceil(len(self._model) / ELEMENT_COLUMN_NUMBER)

    def columnCount(self, parent=None, *args, **kwargs):
        return ELEMENT_COLUMN_NUMBER

    def flags(self, index):
        """disable items in last row without any elements"""
        element_index = index.row() * ELEMENT_COLUMN_NUMBER + index.column()
        if element_index >= len(self._model):
            return Qt.NoItemFlags
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled

    def data(self, index, role=None):
        element_index = index.row() * ELEMENT_COLUMN_NUMBER + index.column()
        # last row might contain empty cells
        if element_index >= len(self._model):
            return

        pix_map = self._model[element_index].icon.pixmap(self._thumbnail_size)
        pix_map.scaled(self._thumbnail_size, Qt.KeepAspectRatio)
        if role == Qt.DecorationRole:
            return pix_map

    def mimeData(self, indexes):
        mime_data = QMimeData()
        element_index = indexes[0].row() * ELEMENT_COLUMN_NUMBER + indexes[0].column()
        # send name of process core to QGraphicsScene
        data_array = QByteArray(bytes(self._model[element_index].name, 'UTF-8'))
        mime_data.setData(MimeType.PROCESS_CORE.value, data_array)

        return mime_data
