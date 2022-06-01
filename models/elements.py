from PySide2.QtCore import *
from models.data_structure import List


class Elements(QObject):
    """stores a specific list of elements
    @param: commodity_list
    @param: process_list
    @function: add_commodity(Commodity)
    @function: remove_commodity(Int)
    @function: add_process(Process)
    @function: remove_process(index)"""

    def __init__(self, commodity_list, process_list):
        super(Elements, self).__init__()
        self._commodity_list = List(commodity_list)
        self._process_list = List(process_list)

    def write(self, output):
        """write data to output stream"""
        self._commodity_list.write(output)
        self._process_list.write(output)

    def read(self, input_):
        """read data from input stream"""
        self._commodity_list.read(input_)
        self._process_list.read(input_)

    def add_commodity(self, commodity):
        self._commodity_list.add(commodity)

    def remove_commodity(self, index):
        self._commodity_list.remove(index)

    def add_process(self, process):
        self._process_list.add(process)

    def remove_process(self, index):
        self._process_list.remove(index)

    @property
    def commodity_list(self):
        return self._commodity_list

    @property
    def process_list(self):
        return self._process_list
