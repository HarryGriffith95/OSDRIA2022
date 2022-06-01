from PySide2.QtCore import QObject

from models.element import CommodityType
from models.data_structure import List


class ListDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, model):
        super(ListDialogCtrl, self).__init__()
        self._model = model

    def transfer_data(self, name_list):
        name_list_length = name_list.rowCount()
        model_length = len(self._model)

        # update model with new date until list length reached
        for row in range(min(name_list_length, model_length)):
            name = name_list.data(name_list.index(row, 0))
            self._model[row] = CommodityType(name)

        # append additional commodities to model
        for row in range(model_length, name_list_length):
            name = name_list.data(name_list.index(row, 0))
            self._model.add(CommodityType(name))

        # delete removed commodities
        for row in range(name_list_length, model_length):
            del(self._model[row])
