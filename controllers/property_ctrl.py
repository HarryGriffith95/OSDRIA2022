from PySide2.QtCore import QObject
from views.property_dialog_view import PropertyDialogView
from views.property_popup_view import PropertyPopupView
from controllers.property_dialog_ctrl import PropertyDialogCtrl
from controllers.property_popup_ctrl import PropertyPopupCtrl


class PropertyCtrl(QObject):
    """controller for property view"""
    def __init__(self, model):
        super(PropertyCtrl, self).__init__()
        self._model = model

    def open_dialog(self):
        dialog_ctrl = PropertyDialogCtrl(self._model)
        dialog_view = PropertyDialogView(self._model, dialog_ctrl)
        dialog_view.exec_()
