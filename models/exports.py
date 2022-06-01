from PySide2.QtCore import *
from models.data_structure import List


class Exports(List):
    """stores a specific list of export properties
    @param: folder_name
    @param: export_list
    @signal: folder_name_changed(str)"""
    folder_name_changed = Signal(str)

    def __init__(self, folder_name, export_list):
        super(Exports, self).__init__(export_list)
        self._folder_name = folder_name

    @property
    def folder_name(self):
        return self._folder_name

    @folder_name.setter
    def folder_name(self, value):
        self._folder_name = value
        self.folder_name_changed.emit(value)


class Export(QObject):
    """data stored for one export property
    @param: element
    @param: graph
    @param: dataset
    @param: period
    @signal: element_changed(Element)
    @signal: graph_changed(str)
    @signal: dataset_changed(str)
    @signal: period_changed(str)"""
    element_changed = Signal(QObject)
    graph_changed = Signal(str)
    data_set_changed = Signal(str)
    period_changed = Signal(str)

    def __init__(self, element, graph, data_set, period):
        super(Export, self).__init__()
        self._element = element
        self._graph = graph
        self._data_set = data_set
        self._period = period

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        self._element = value
        self.element_changed.emit(value)

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, value):
        self._graph = value
        self.graph_changed.emit(value)

    @property
    def data_set(self):
        return self._data_set

    @data_set.setter
    def data_set(self, value):
        self._data_set = value
        self.data_set_changed.emit(value)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = value
        self.period_changed.emit(value)
