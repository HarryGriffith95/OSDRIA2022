from PySide2.QtWidgets import *
from PySide2.QtGui import QFont
from PySide2.QtCore import QPoint

from models.data_structure import List


class PropertyPopupView(QMenu):
    """view of property popup"""

    def __init__(self, parent, popup_model, popup_controller):
        super(PropertyPopupView, self).__init__(parent)
        self._model = popup_model
        self._popup_ctrl = popup_controller

        """connect widgets to controller"""
        self.triggered.connect(self._popup_ctrl.set_popup_value)

        """initialise view"""
        list_without_value = self.get_list_without_value()
        for choice in list_without_value:
            # create and add action with name of choice and index
            # without first element
            popup_action = QAction(str(choice), self.parent())
            popup_action.setData(choice)
            self.addAction(popup_action)
        self.setFont(self.parent().font())

    def get_list_without_value(self):
        """copy list to delete shown list element without affecting original list"""
        # check whether value is reference of element in choices list (probably corrupted by file read)
        if self._model.value not in self._model.choices:
            self._model.value = list(filter(lambda choice: str(choice) == str(self._model.value),
                                            self._model.choices))[0]

        popup_list = self._model.choices.copy()
        popup_list.remove(self._model.value)
        return popup_list

    def show_popup(self):
        """override popup function to define location of popup"""
        height = self.parent().height()
        position = self.parent().mapToGlobal(QPoint(0, height + 5))
        self.popup(position)

