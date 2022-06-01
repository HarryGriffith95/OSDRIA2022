from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QIcon

from models.constants import ProcessCategory, OverviewSelection, DatasetResolution
from models.property import *
from models.data_structure import *

COMMODITY_NAME = "Commodity Name"


class ProcessCore(QObject):
    """data representing the process core
    @signal: name_changed()
    @signal: icon_changed()
    @signal: category_changed()
    @signal: section_changed()
    @signal: objective_function_changed()
    @signal: constraints_changed()"""
    name_changed = Signal()
    icon_changed = Signal()
    category_changed = Signal()
    section_changed = Signal()
    objective_function_changed = Signal()
    constraints_changed = Signal()

    def __init__(self):
        super(ProcessCore, self).__init__()
        self._name = ""
        self._icon = QIcon()
        self._category = ProcessCategory.SUPPLY
        self._section = OverviewSelection.ENERGY
        self.variables = List([])
        self.data = List([])
        self.properties = List([])
        self.inputs = List([])
        self.outputs = List([])
        self._objective_function = ""
        self._constraints = ""

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        output << self._icon
        output.writeUInt32(self._category.value)
        output.writeUInt32(self._section.value)
        self.variables.write(output)
        self.data.write(output)
        self.properties.write(output)
        self.inputs.write(output)
        self.outputs.write(output)
        output.writeString(self._objective_function)
        output.writeString(self._constraints)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        input_ >> self._icon
        self._category = ProcessCategory(input_.readUInt32())
        self._section = OverviewSelection(input_.readUInt32())
        self.variables.read(input_)
        self.data.read(input_)
        self.properties.read(input_)
        self.inputs.read(input_)
        self.outputs.read(input_)
        self._objective_function = input_.readString()
        self._constraints = input_.readString()

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit()

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.icon_changed.emit()

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        if value in OverviewSelection:
            self._section = value
            self.section_changed.emit()
        else:
            raise AttributeError

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value in ProcessCategory:
            self._category = value
            self.category_changed.emit()
        else:
            raise AttributeError

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

    @property
    def objective_function(self):
        return self._objective_function

    @objective_function.setter
    def objective_function(self, value):
        self._objective_function = value
        self.objective_function_changed.emit()

    @property
    def constraints(self):
        return self._constraints

    @constraints.setter
    def constraints(self, value):
        self._constraints = value
        self.constraints_changed.emit()


class Process(QObject):
    """data representing process object
    @param: name(str)
    @param: coordinate(QVector2D)
    @param: process_core(ProcessCore)
    @signal: name_changed()
    @signal: coordinate_changed()
    @signal: core_changed()"""
    coordinate_changed = Signal()

    def __init__(self, name="", coordinate=QPoint(), process_core=ProcessCore()):
        super(Process, self).__init__()
        self._coordinate = coordinate
        self.core = process_core
        self.inputs = List([])
        self.outputs = List([])
        self.optimization_output = Dict({})

        property_name = self.core.category.name.title() + " Name"
        name_property = PropertyLineEdit(property_name, name)
        self.properties = List([name_property])
        self.define_core_properties()

    def write(self, output):
        """write data to output stream"""
        output.writeFloat(self._coordinate.x())
        output.writeFloat(self._coordinate.y())
        output.writeString(self.core.name)
        self.inputs.write(output)
        self.outputs.write(output)
        self.properties.write(output)
        self.optimization_output.write(output)

    def read(self, input_):
        """read data from input stream"""
        x_coordinate = input_.readFloat()
        y_coordinate = input_.readFloat()
        self._coordinate = QPoint(x_coordinate, y_coordinate)
        self.core = input_.readString()
        self.inputs.read(input_)
        self.outputs.read(input_)
        self.properties.read(input_)
        self.optimization_output.read(input_)

    def __str__(self):
        return self.name

    def define_core_properties(self):
        """initialise properties of ProcessCore as templates"""
        for prop in self.core.properties:
            self.properties.add(prop.copy())

    @property
    def name(self):
        return self.properties[0].value

    @property
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, value):
        self._coordinate = value
        self.coordinate_changed.emit()


class CommodityType(QObject):
    """data representing commodity object
    @param: name
    @param: sub_commodities=[]
    @function: add_sub_commodity(SubCommodity)
    @function: remove_sub_commodity(int)
    @signal: sub_commodities_changed()"""

    def __init__(self, name=""):
        super(CommodityType, self).__init__()
        self._name = name
        # represents x value in respective section
        self.locations = Dict({})
        self.properties = List([])
        self.properties.add(
            PropertyLineEdit(COMMODITY_NAME, name))

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        self.locations.write(output)
        self.properties.write(output)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        self.locations.read(input_)
        self.properties.read(input_)

    def __str__(self):
        return self.properties[0].value


class Commodity(QObject):
    """data representing a sub commodity
    @param: name
    @param: com_type(CommodityType)
    @signal: name_changed()
    @signal: type_changed()"""
    name_changed = Signal()
    type_changed = Signal()

    def __init__(self, name="", commodity_type=CommodityType(), resolution=DatasetResolution.YEARLY):
        super(Commodity, self).__init__()
        self._name = name
        self._type = commodity_type
        self._id = id(self)
        self.resolution = resolution
        self.optimization_output = Dict({'input_processes': Dict({}), 'output_processes': Dict({})})
        self.connection_count = Dict({})

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        output.writeString(str(self._type))
        output.writeUInt64(self._id)
        self.optimization_output.write(output)
        self.connection_count.write(output)
        output.writeUInt32(self.resolution.value)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        self._type = input_.readString()
        self._id = input_.readUInt64()
        self.optimization_output.read(input_)
        self.connection_count.read(input_)
        self.resolution = DatasetResolution(input_.readUInt32())

    def __str__(self):
        return self._name

    def __eq__(self, other):
        return (self.commodity_type == other.commodity_type) & (self.name == other.name)

    def copy(self):
        return Commodity(self.name, self.commodity_type, self.resolution)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit()

    @property
    def commodity_type(self):
        return self._type

    @commodity_type.setter
    def commodity_type(self, value):
        self._type = value
        self.type_changed.emit()

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        self._section = value

    @property
    def unique_id(self):
        return self._id
