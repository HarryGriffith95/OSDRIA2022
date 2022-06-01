from PySide2.QtCore import Qt
from PySide2.QtWidgets import *

from models.property import PropertyPopupMenu, PropertyLineEdit
from models.data_structure import List
from models.constants import DatasetResolution

from views.dataset_dialog_view_ui import Ui_DatasetDialog
from views.components.dataset_table_view import DatasetModel


class DatasetDialogView(QDialog):
    """Dataset Dialog View"""

    def __init__(self, dataset_dialog_model, dataset_dialog_controller):
        settings = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        super(DatasetDialogView, self).__init__(None, settings)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._model = dataset_dialog_model
        self._unit_model = PropertyLineEdit("Unit")
        self._resolution_popup_model = PropertyPopupMenu("Resolution", List(list(DatasetResolution)))
        self._table_view_model = DatasetModel([])
        self._ctrl = dataset_dialog_controller
        self._ui = Ui_DatasetDialog()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        self._ui.dataset_name.clicked.connect(self.gather_data)
        self._ui.button_add.clicked.connect(self.on_add_click)
        self._ui.cancel_button.clicked.connect(self.reject)
        self._ui.apply_button.clicked.connect(self.accept)
        self.accepted.connect(self.gather_data)
        #self._ui.dataset_value.keyPressed.connect(self._ui.dataset_value.keyPressEvent())

        """listen for model event signals"""
        self._model.value_changed.connect(self.on_dataset_change)
        self._resolution_popup_model.value_changed.connect(self.on_resolution_change)

        """initialize view"""
        self._new_dataset = False
        self._ui.dataset_name.set_model(self._model)
        self._ui.dataset_name.setReadOnly(False)
        self._ui.unit_value.set_model(self._unit_model)
        self._ui.resolution_value.set_model(self._resolution_popup_model)
        self._ui.dataset_value.setModel(self._table_view_model)
        self._ui.dataset_graph.set_model(self._table_view_model)
        if not self._model.value:
            self._new_process = True
            self.init_content()
        else:
            self.load_content(self._model.value)

    def init_content(self):
        """initialise new process with empty inputs"""
        self._ui.dataset_name.setText("Dataset Name")
        self._ui.unit_value.setText("Unit")
        self._resolution_popup_model.value = self._resolution_popup_model.choices[0]
        self._table_view_model.change_data([""] * self._resolution_popup_model.value.value)
        self._new_dataset = True

    def load_content(self, dataset):
        dataset_resolution = len(dataset.value)
        if dataset_resolution == 0:
            dataset_resolution = 8760

        self._ui.unit_value.setText(dataset.unit)
        self._resolution_popup_model.value = DatasetResolution(dataset_resolution)
        self._table_view_model.change_data(dataset.value)

    def on_resolution_change(self):
        self._ui.resolution_value.setText(str(self._resolution_popup_model.value))
        self._table_view_model.change_data([""] * self._resolution_popup_model.value.value)

    def on_dataset_change(self):
        self._ui.dataset_name.setText(str(self._model.value))
        self.load_content(self._model.value)

    def on_add_click(self):
        """save process and initialise new one"""
        self.gather_data()
        self.init_content()

    def gather_data(self):
        """transfer edited data to model"""
        self._ctrl.transfer_data(
            self._new_dataset,
            self._ui.dataset_name.text(),
            self._ui.unit_value.text(),
            self._ui.resolution_value.text(),
            self._table_view_model.retrieve_data()
        )
        self._new_dataset = False

    def keyPressEvent(self, event):
        """prevent dialog closing with enter or return key"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return

        super().keyPressEvent(event)


