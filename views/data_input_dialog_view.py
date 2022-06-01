from PySide2.QtCore import Qt
from PySide2.QtWidgets import *

from views.data_input_dialog_view_ui import Ui_DataInputDialog
from views.components.property_edit import PropertyEdit


class DataInputDialogView(QDialog):
    """Data Input Dialog View"""

    def __init__(self, data_input_dialog_model, data_input_dialog_controller):
        settings = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        super(DataInputDialogView, self).__init__(None, settings)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._model = data_input_dialog_model
        self._ctrl = data_input_dialog_controller
        self._ui = Ui_DataInputDialog()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        self.accepted.connect(self.on_dialog_accepted)
        self._ui.cancel_button.clicked.connect(self.reject)
        self._ui.apply_button.clicked.connect(self.accept)
        #self._ui.data_table.textChanged.connect

        """initialize view"""
        self._ui.title.setText(self._model.name)
        self._line_edits = []
        for item in self._model.values:
            label = QLabel(self._ui.frame)
            label.setText(item.name)
            line_edit = PropertyEdit(self._ui.frame)
            line_edit.set_unit(item.unit)
            line_edit.setText(item.value)
            self._line_edits.append(line_edit)
            self._ui.form_layout.addRow(label, line_edit)
        self._ui.frame.updateGeometry()

    def on_dialog_accepted(self):
        """transfer edited data to model"""
        value_list = [line_edit.text() for line_edit in self._line_edits]
        self._property_ctrl.set_property_values(value_list)

    def keyPressEvent(self, event):
        """prevent dialog closing with enter or return key"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        super().keyPressEvent(event)


