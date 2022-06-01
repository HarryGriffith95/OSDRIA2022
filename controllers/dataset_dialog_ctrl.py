from PySide2.QtCore import QObject

from models.data_structure import List
from models.property import PropertyValueTimeSeries


class DatasetDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, model):
        super(DatasetDialogCtrl, self).__init__()
        self._model = model

    def transfer_data(self, new_dataset, name, unit, resolution, dataset_values):
        if new_dataset:
            # create new dataset, add to current list and set it as current
            new_dataset = PropertyValueTimeSeries()
            self._model.choices.add(new_dataset)
            self._model.value = new_dataset

        self._model.value.name = name
        self._model.value.value = List(dataset_values)
        self._model.value.unit = unit
