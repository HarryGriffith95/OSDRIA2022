from PySide2.QtCore import Qt, QObject, QSize, QModelIndex, Signal
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap
from PySide2.QtWidgets import QDialog, QStyledItemDelegate, QPushButton, QWidget, QStyle, QHeaderView

from views.components.tool_button import ToolButton
from views.list_dialog_view_ui import Ui_ListDialog
from models.property import PropertyLineEdit
from models.element import CommodityType


class ListDialogView(QDialog):
    """Property Dialog View"""
    hover_index_changed = Signal(QModelIndex)

    def __init__(self, dialog_model, dialog_controller):
        settings = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        super(ListDialogView, self).__init__(None, settings)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._model = dialog_model
        self._dialog_ctrl = dialog_controller
        self._ui = Ui_ListDialog()
        self._ui.setupUi(self)

        delete_button_delegate = DeleteButtonDelegate(self)
        self._commodity_model = QStandardItemModel(0, 2, self._ui.commodity_list)
        for commodity in self._model:
            self._commodity_model.appendRow([QStandardItem(str(commodity)), QStandardItem()])

        """connect widgets to controller"""
        self._ui.button_add.clicked.connect(self.add_list_item)
        self._ui.commodity_list.clicked.connect(self.remove_list_item)
        self._ui.commodity_list.hover_index_changed.connect(delete_button_delegate.on_hover_index_changed)
        self.accepted.connect(self.on_dialog_accepted)
        self._ui.cancel_button.clicked.connect(self.reject)
        self._ui.apply_button.clicked.connect(self.accept)

        """initialize view"""
        self._ui.commodity_name.set_model(PropertyLineEdit(""))
        self._ui.commodity_list.setModel(self._commodity_model)
        self._ui.commodity_list.setItemDelegateForColumn(1, delete_button_delegate)
        self._ui.commodity_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self._ui.commodity_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self._ui.commodity_list.setColumnWidth(1, 22)

    def add_list_item(self):
        if self._ui.commodity_name.text() != "":
            self._commodity_model.appendRow([QStandardItem(self._ui.commodity_name.text()), QStandardItem()])
            self._ui.commodity_name.set_model(PropertyLineEdit(""))

    def remove_list_item(self, index):
        if index.column() == 1:
            self._commodity_model.removeRow(index.row())

    def on_dialog_accepted(self):
        """transfer edited data to model"""
        self._dialog_ctrl.transfer_data(self._commodity_model)

    def keyPressEvent(self, event):
        """prevent dialog closing with enter or return key"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        super().keyPressEvent(event)


class DeleteButtonDelegate(QStyledItemDelegate):
    """custom list view appearance to show delete button"""
    def __init__(self, parent):
        super(DeleteButtonDelegate, self).__init__(parent)
        self._mouse_index = QModelIndex()
        self._normal_pix_map = QPixmap(":/icons/img/minus_select@2x.png")
        self._select_pix_map = QPixmap(":/icons/img/minus_normal@2x.png")

    def on_hover_index_changed(self, index):
        """set table index of current mouse location"""
        self._mouse_index = index
        self.parent().update()

    def paint(self, painter, option, index):
        pix_map = self._select_pix_map if self._mouse_index == index else self._normal_pix_map
        painter.drawPixmap(option.rect.x(), option.rect.y(), pix_map)
