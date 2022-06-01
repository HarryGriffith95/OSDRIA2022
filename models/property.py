from PySide2.QtCore import *

from models.data_structure import List
from models.constants import PropType, PyomoVarType, DatasetResolution, DisplayType


class PropertyValue(QObject):
    """data stored for property value with unit information
    @param: name(str)
    @param: value(str)
    @param: unit(str)
    @signal: value_changed(str)"""
    name_changed = Signal(str)
    value_changed = Signal(str)

    def __init__(self, name="", value="", unit=""):
        super().__init__()
        self._name = name
        self._value = value
        self._unit = unit

    def __str__(self):
        """create display value if string is requested"""
        display_value = str(self._value)
        if self._unit != "":
            display_value += " " + self._unit
        return display_value

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        output.writeString(str(self._value))
        output.writeString(self._unit)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        self._value = input_.readString()
        self._unit = input_.readString()

    def copy(self):
        """return a new property with the same features"""
        return PropertyValue(self._name, self._value, self._unit)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.value_changed.emit(value)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value


class PropertyVariable(QObject):
    """data stored for property variable
        @param: name(str)
        @param: resolution(DatasetResolution)
        @param: pyomo_type(PyomoVarType)
        @param: unit(str)"""

    def __init__(self, name="", resolution=DatasetResolution.YEARLY, pyomo_type=PyomoVarType.REALS,
                 unit="", display=DisplayType.NO):
        super().__init__()
        self._name = name
        self.resolution = resolution
        self.type = pyomo_type
        self.unit = unit
        self.display = display

    def __str__(self):
        return self._name

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        output.writeUInt32(self.resolution.value)
        output.writeString(self.type.value)
        output.writeString(self.unit)
        output.writeUInt32(self.display.value)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        self.resolution = DatasetResolution(input_.readUInt32())
        self.type = PyomoVarType(input_.readString())
        self.unit = input_.readString()
        self.display = DisplayType(input_.readUInt32())

    @property
    def name(self):
        return self._name


class PropertyValueTimeSeries(PropertyValue):
    """data stored for property value representing a times series
    @param: name
    @param: value(List)
    @param: unit
    @signal: name_changed(str)
    @signal: value_changed()"""
    name_changed = Signal(str)
    value_changed = Signal()

    def __init__(self, name="", value=[], unit=""):
        super().__init__(name, "", unit)
        self._value = List(value)

    def write(self, output):
        """write data to output stream"""
        output.writeString(super().name)
        self._value.write(output)
        output.writeString(super().unit)

    def read(self, input_):
        """read data from input stream"""
        PropertyValue.name.fset(self, input_.readString())
        self._value.read(input_)
        PropertyValue.unit.fset(self, input_.readString())

    def __str__(self):
        return super().name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class PropertyLineEdit(PropertyValue):
    """data stored for property of line edit
    @param: name
    @param: value
    @param: unit
    @signal: name_changed(str)
    @signal: value_changed(str)"""
    name_changed = Signal(str)
    value_changed = Signal(str)
    type = PropType.LINE_EDIT

    def __init__(self, name="", value="", unit=""):
        super().__init__(name, value, unit)
        self.read_only = False

    def copy(self):
        return PropertyLineEdit(self.name, self.value, self.unit)


class PropertyDialog(PropertyValue):
    """data stored for property with dialog input
    @param: name(str)
    @param: values({name: PropertyValue})
    @signal: name_changed(str)
    @signal: values_changed(List)"""
    name_changed = Signal(str)
    values_changed = Signal(List)
    type = PropType.DIALOG

    def __init__(self, name="", values=[]):
        super().__init__(name)
        self._values = List(values)
        # create display value for sub-property properties
        display_text = ", ".join(map(str, values))
        PropertyDialog.value.fset(self, display_text)

    def write(self, output):
        """write data to output stream"""
        super().write(output)
        self._values.write(output)

    def read(self, input_):
        """read data from input stream"""
        super().read(input_)
        self._values.read(input_)

    def copy(self):
        """return new PropertyDialog based on original values"""
        values = List()
        for value in self.values:
            values.add(PropertyValue(value.name, value.value, value.unit))
        return PropertyDialog(super().name, values)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value
        self.values_changed.emit(value)


class PropertyPopupMenu(PropertyValue):
    """data stored for property with popup input
    @param: name
    @param: choices(List)
    @signal: name_changed(str)
    @signal: value_changed(str)
    @signal: choices_changed()"""
    name_changed = Signal(str)
    value_changed = Signal(str)
    choices_changed = Signal()
    type = PropType.POPUP_MENU

    def __init__(self, name="", choices=List(), value=None):
        if choices.list:
            if value:
                super().__init__(name, value)
            else:
                super().__init__(name, choices[0])
        else:
            super().__init__(name)
        self._choices = choices

    def write(self, output):
        """write data to output stream"""
        super().write(output)
        self._choices.write(output)

    def read(self, input_):
        """read data from input stream"""
        super().read(input_)
        self._choices.read(input_)
        # get object from choices list based on saved name in value
        if self._choices:
            value_list = list(filter(lambda x: str(x) == super(PropertyPopupMenu, self).value, self._choices))
            if value_list:
                value = value_list[0]
            else:
                value = self._choices[0]
        else:
            value = ""
        PropertyValue.value.fset(self, value)

    def copy(self):
        """return new PropertyPopupMenu based on original data"""
        return PropertyPopupMenu(self.name, self.choices)

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        self._choices = value
        self.choices_changed.emit()
