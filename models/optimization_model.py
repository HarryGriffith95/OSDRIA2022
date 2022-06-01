from PySide2.QtCore import *


class OptimizationModel(QObject):
    """stores data specified for optimization process
    @param: process_list
    """
    text_changed = Signal(str)

    def __init__(self, model):
        super(OptimizationModel, self).__init__()
        self._process_list = model.process_list
        self._commodity_list = model.commodity_list
        self._optimization_text = ""

    @property
    def process_list(self):
        return self._process_list

    @property
    def commodity_list(self):
        return self._commodity_list

    @property
    def optimization_text(self):
        return self._optimization_text

    @optimization_text.setter
    def optimization_text(self, value):
        self._optimization_text = value
        self.text_changed.emit(value)
