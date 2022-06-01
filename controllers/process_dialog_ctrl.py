from PySide2.QtCore import QObject, QModelIndex
from PySide2.QtWidgets import QFileDialog

from controllers.property_popup_ctrl import PropertyPopupCtrl
from controllers.property_dialog_ctrl import PropertyDialogCtrl
from views.property_popup_view import PropertyPopupView
from views.property_dialog_view import PropertyDialogView
from models.constants import ProcessCategory, OverviewSelection, DatasetResolution, PyomoVarType, DisplayType
from models.data_structure import List
from models.property import *
from models.element import ProcessCore, Commodity


class ProcessDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, model, commodity_list, time_series_list):
        super(ProcessDialogCtrl, self).__init__()
        self._model = model
        self._commodities = commodity_list
        self._time_series = time_series_list

    def change_variables(self, command, index, model):
        if command == "Add":
            # create model for dialog
            dialog_model = PropertyDialog("Add Variable", [PropertyLineEdit("Name"),
                                                           PropertyLineEdit("Unit"),
                                                           PropertyPopupMenu("Resolution",
                                                                             List(list(DatasetResolution))),
                                                           PropertyPopupMenu("Pyomo Type", List(list(PyomoVarType))),
                                                           PropertyPopupMenu("Display Result",
                                                                             List(list(DisplayType)))])
            if self.show_dialog(dialog_model):
                # retrieve data from dialog model
                name = dialog_model.values[0].value
                unit = dialog_model.values[1].value
                resolution = dialog_model.values[2].value
                pyomo_type = dialog_model.values[3].value
                display_result = dialog_model.values[4].value
                item = PropertyVariable(name, resolution, pyomo_type, unit, display_result)
                # set list view data
                self.add_item(model, item)

        else:
            # create model for dialog
            item = model.retrieve_data()[index]
            dialog_model = PropertyDialog("Edit Variable", [PropertyLineEdit("Unit", item.unit),
                                                            PropertyPopupMenu("Resolution",
                                                                              List(list(DatasetResolution)),
                                                                              item.resolution),
                                                            PropertyPopupMenu("Pyomo Type",
                                                                              List(list(PyomoVarType)),
                                                                              item.type),
                                                            PropertyPopupMenu("Display Result",
                                                                              List(list(DisplayType)),
                                                                              item.display)])
            if self.show_dialog(dialog_model):
                # retrieve data from dialog model
                item.unit = dialog_model.values[0].value
                item.resolution = dialog_model.values[1].value
                item.type = dialog_model.values[2].value
                item.display = dialog_model.values[3].value

    def change_data(self, command, index, model):
        if command == "Add":
            # create model for dialog
            dialog_model = PropertyDialog(command + " Data", [PropertyLineEdit("Name"),
                                                              PropertyLineEdit("Unit"),
                                                              PropertyLineEdit("Value")])
            if self.show_dialog(dialog_model):
                # retrieve data from dialog model
                name = dialog_model.values[0].value
                unit = dialog_model.values[1].value
                value = dialog_model.values[2].value.split(", ")
                item = PropertyValueTimeSeries(name, value, unit) if len(value) > 1 \
                    else PropertyValue(name, value[0], unit)

                # set list view data
                self.add_item(model, item)
        else:
            # create model for dialog
            item = model.retrieve_data()[index]
            value = ", ".join(item.value) if isinstance(item, PropertyValueTimeSeries) else item.value
            dialog_model = PropertyDialog(command + " " + item.name, [PropertyLineEdit("Value", value, item.unit)])

            if self.show_dialog(dialog_model):
                # retrieve model and set list view data
                value = dialog_model.values[0].value
                item.value = value.split(", ") if isinstance(item, PropertyValueTimeSeries) else value

    def change_properties(self, command, _, model):
        # not allowed to edit properties
        if command == "Edit":
            return

        single_value = "Single Value"
        time_series = "Timeseries"
        dialog_model = PropertyDialog(command + " Property", [PropertyLineEdit("Name"),
                                                              PropertyLineEdit("Unit"),
                                                              PropertyPopupMenu("Type",
                                                                                List([single_value, time_series]))])
        if self.show_dialog(dialog_model):
            name = dialog_model.values[0].value
            unit = dialog_model.values[1].value
            prop_type = dialog_model.values[2].value
            item = PropertyPopupMenu(name, self._time_series) if prop_type == time_series \
                else PropertyLineEdit(name, "", unit)
            self.add_item(model, item)

    def change_commodities(self, command, index, model):
        if command == "Add":
            dialog_model = PropertyDialog(command + " Commodity",
                                          [PropertyLineEdit("Name"),
                                           PropertyPopupMenu("Type", self._commodities),
                                           PropertyPopupMenu("Resolution", List(list(DatasetResolution)))])
            if self.show_dialog(dialog_model):
                name = dialog_model.values[0].value
                commodity_type = dialog_model.values[1].value
                resolution = dialog_model.values[2].value
                item = Commodity(name, commodity_type, resolution)
                self.add_item(model, item)
        else:
            item = model.retrieve_data()[index]
            dialog_model = PropertyDialog(command + " Commodity",
                                          [PropertyPopupMenu("Type", self._commodities, item.commodity_type),
                                           PropertyPopupMenu("Resolution",
                                                             List(list(DatasetResolution)),
                                                             item.resolution)])
            if self.show_dialog(dialog_model):
                item.commodity_type = dialog_model.values[0].value
                item.resolution = dialog_model.values[1].value

    def transfer_data(self, new_process, name, section, category, icon,
                      variables_data, data_data, properties_data, inputs_data, outputs_data,
                      objective, constraints):
        if new_process:
            # create new process, add to current list and set it as current
            new_process = ProcessCore()
            self._model.choices.add(new_process)
            self._model.value = new_process

        self._model.value.name = name
        self._model.value.section = OverviewSelection[section.upper()]
        self._model.value.category = ProcessCategory[category.upper()]
        self._model.value.icon = icon
        self._model.value.variables = List(variables_data)
        self._model.value.data = List(data_data)
        self._model.value.properties = List(properties_data)
        self._model.value.inputs = List(inputs_data)
        self._model.value.outputs = List(outputs_data)
        self._model.value.objective_function = objective
        self._model.value.constraints = constraints

    def show_dialog(self, model):
        dialog_ctrl = PropertyDialogCtrl(model)
        dialog_view = PropertyDialogView(model, dialog_ctrl)
        # execute dialog and return boolean defining cancel (false) or accept (true) button
        return dialog_view.exec_()

    def add_item(self, model, item):
        model.insertRow(model.rowCount())
        index = model.index(model.rowCount() - 1)
        model.setData(index, item)
