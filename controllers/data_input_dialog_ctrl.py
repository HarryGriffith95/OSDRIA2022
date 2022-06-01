from PySide2.QtCore import QObject

from models.constants import PropType


class PropertyDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, model):
        super(PropertyDialogCtrl, self).__init__()
        self._model = model

    def set_property_values(self, value_list):
        for model_value, dialog_value in zip(self._model.values, value_list):
            model_value.value = dialog_value

        # create display value for sub-property properties
        display_text = ", ".join(map(str, value_list))
        self._model.value = display_text
