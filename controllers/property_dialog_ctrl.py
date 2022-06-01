from PySide2.QtCore import QObject

from models.constants import PropType
from models.property import PropertyLineEdit, PropertyDialog, PropertyPopupMenu


class PropertyDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, model):
        super(PropertyDialogCtrl, self).__init__()
        self._model = model

    def set_property_values(self, value_list):
        """get some element based on reference by comparing names except of PropertyLineEdit (string)"""
        for model_value, dialog_value in zip(self._model.values, value_list):
            if isinstance(model_value, PropertyLineEdit):
                model_value.value = dialog_value
            elif isinstance(model_value, PropertyDialog):
                model_value.value = list(filter(lambda value: str(value) == dialog_value, model_value.values))[0]
            else:
                model_value.value = list(filter(lambda value: str(value) == dialog_value, model_value.choices))[0]

        # create display value for sub-property properties
        display_text = ", ".join(map(str, value_list))
        self._model.value = display_text
