from PySide2.QtCore import *
from models.property import PropertyValue
from models.element import Process
from models.data_structure import List


class Scenario(List):
    """stores data for scenario
    @param: name
    @param: property_list
    @signal: name_changed(str)"""
    name_changed = Signal(str)

    def __init__(self, name="", property_list=[]):
        super(Scenario, self).__init__(property_list)
        self._name = name

    def __str__(self):
        return self._name

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        super().write(output)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        super().read(input_)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)


class ScenarioProperty(QObject):
    """stores data for a property change in scenario
    @param: element
    @param: operator
    @param: prop
    @signal: element_changed(Element)
    @signal: operator_changed(str)
    @signal: property_changed(Property)"""
    element_changed = Signal()
    operator_changed = Signal()
    property_changed = Signal()

    def __init__(self, element=Process(), operator="", prop=PropertyValue()):
        super(ScenarioProperty, self).__init__()
        self._element = element
        self._operator = operator
        self._prop = prop

    def write(self, output):
        """write data to output stream"""
        self._element.write(output)
        output.writeString(self._operator)
        self._prop.write(output)

    def read(self, input_):
        """read data from input stream"""
        self._element.read(input_)
        self._operator = input_.readString()
        self._prop.read(input_)

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        self._element = value
        self.element_changed.emit()

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        self._operator = value
        self.operator_changed.emit()

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value
        self.property_changed.emit()
