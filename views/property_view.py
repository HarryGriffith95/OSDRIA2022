from PySide2.QtWidgets import *

from models.constants import PropType
from views.property_view_ui import Ui_property


class PropertyView(QWidget):
    """view of property in sidebar"""

    def __init__(self, parent, property_model, property_controller):
        super(PropertyView, self).__init__(parent)

        self._model = property_model
        self._property_ctrl = property_controller
        self._ui = Ui_property()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        if self._model.type is PropType.DIALOG:
            self._ui.property_value.clicked.connect(
                self._property_ctrl.open_dialog)

        """listen for model event signals"""

        """initialize view"""
        self._ui.property_name.setText(self._model.name)
        self._ui.property_value.set_model(self._model)
