from PySide2.QtCore import QObject

from models.constants import PropType


class PropertyPopupCtrl(QObject):
    """controller for property popup view"""
    def __init__(self, popup_model):
        super(PropertyPopupCtrl, self).__init__()
        self._model = popup_model

    def set_popup_value(self, action):
        """move selected item to beginning of list and set """
        selected_value_name = str(action.data())
        self._model.value = list(filter(lambda choice: str(choice) == selected_value_name, self._model.choices))[0]
