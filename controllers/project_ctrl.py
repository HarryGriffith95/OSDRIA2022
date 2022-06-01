from PySide2.QtCore import QObject

from models.constants import OverviewSelection, PageType, SelectConnect, PropType
from models.property import PropertyPopupMenu
from models.optimization_model import OptimizationModel

from controllers.dataset_dialog_ctrl import DatasetDialogCtrl
from controllers.process_dialog_ctrl import ProcessDialogCtrl
from controllers.list_dialog_ctrl import ListDialogCtrl
from controllers.optimization_dialog_ctrl import OptimizationDialogCtrl

from views.dataset_dialog_view import DatasetDialogView
from views.process_dialog_view import ProcessDialogView
from views.list_dialog_view import ListDialogView
from views.optimization_dialog_view import OptimizationDialogView


class ProjectCtrl(QObject):
    """controller for project view"""
    def __init__(self, model):
        super(ProjectCtrl, self).__init__()
        self._model = model
        self.connect_model_data(self._model)

    @staticmethod
    def connect_model_data(model):
        """connect model data with references to other model data when model is loaded from file"""

        # connect process core in Process instance to ProcessCore instance
        for process_core in model.process_cores:
            # get commodity type from commodity list
            for input_data in process_core.inputs:
                input_data.commodity_type = list(filter(lambda commodity_type:
                                                        str(commodity_type) == str(input_data.commodity_type),
                                                        model.commodities))[0]

            for output in process_core.outputs:
                output.commodity_type = list(filter(lambda commodity_type:
                                                    str(commodity_type) == str(output.commodity_type),
                                                    model.commodities))[0]

            # link popup list of properties to project time series
            for prop in process_core.properties:
                if prop.type == PropType.POPUP_MENU:
                    prop.choices = model.time_series
                    if model.time_series:
                        prop.value = list(filter(
                            lambda time_serie: str(time_serie) == str(prop.value), model.time_series))[0]

        # connect commodity type in Commodity instance with CommodityType in commodities
        for commodity in model.project_elements.commodity_list:
            commodity.commodity_type = list(filter(lambda commodity_type:
                                                   str(commodity_type) == str(commodity.commodity_type),
                                                   model.commodities))[0]

        # connect process core in Process instance with ProcessCore in process_cores
        # connect input/output commodity in Process instance with Commodity in commodity_list
        for process in model.project_elements.process_list:
            # set process core to identity of model's process cores
            process.core = list(filter(lambda core: core.name == process.core, model.process_cores))[0]

            # input commodities
            for index, input_com in enumerate(process.inputs):
                process.inputs[index] = list(filter(lambda commodity:
                                                    str(commodity) == str(input_com),
                                                    model.project_elements.commodity_list))[0]

            # output commodities
            for index, output in enumerate(process.outputs):
                liste1 = list(filter(lambda commodity:
                                                     str(commodity) == str(output),
                                                     model.project_elements.commodity_list))
                if liste1:
                    process.outputs[index] = liste1[0]
                if not liste1:
                    pass

            # link popup list of properties to project time series
            for prop in process.properties:
                if prop.type == PropType.POPUP_MENU:
                    prop.choices = model.time_series
                    if model.time_series:
                        prop.value = list(filter(
                            lambda time_series: str(time_series) == str(prop.value), model.time_series))[0]

        # todo add necessary model connectors

    def save_model(self):
        self._model.save()

    def open_time_series_dialog(self):
        time_series_model = PropertyPopupMenu("Datasets", self._model.time_series)
        time_series_ctrl = DatasetDialogCtrl(time_series_model)
        time_series_view = DatasetDialogView(time_series_model, time_series_ctrl)
        time_series_view.exec_()

    def open_commodity_dialog(self):
        commodities_ctrl = ListDialogCtrl(self._model.commodities)
        commodities_view = ListDialogView(self._model.commodities, commodities_ctrl)
        commodities_view.exec_()

    def open_process_dialog(self):
        dialog_model = PropertyPopupMenu("Process Cores", self._model.process_cores)
        process_ctrl = ProcessDialogCtrl(dialog_model, self._model.commodities, self._model.time_series)
        process_view = ProcessDialogView(dialog_model, process_ctrl)
        process_view.exec_()

    def open_scenario_dialog(self):
        print("open_scenario_dialog")

    def run_optimization(self):
        dialog_model = OptimizationModel(self._model.project_elements)
        optimization_ctrl = OptimizationDialogCtrl(dialog_model, self._model.project_file)
        optimization_view = OptimizationDialogView(dialog_model, optimization_ctrl)
        optimization_view.show()

    def open_export_dialog(self):
        print("open_export_dialog")

    def toggle_sidebar(self, page, out=None):
        if page is PageType.OVERVIEW:
            self._model.overview_sidebar_out = not self._model.overview_sidebar_out if out is None else out
        elif page is PageType.SECTIONS:
            self._model.sections_sidebar_out = not self._model.sections_sidebar_out if out is None else out
        elif page is PageType.DRAFT:
            self._model.draft_sidebar_out = not self._model.draft_sidebar_out if out is None else out

    def change_icon(self, selection_type):
        self._model.overview_selection = OverviewSelection(selection_type)

    def change_page(self, page):
        self._model.current_section = self._model.overview_selection
        if page == PageType.OVERVIEW:
            self._model.overview_selection = OverviewSelection.OVERVIEW

        self._model.current_page = page

        if page == PageType.DRAFT:
            self._model.draft_select_mode = SelectConnect.SELECT

    def toggle_select_connect(self, select_type):
        self._model.draft_select_mode = select_type

    def change_graph_commodity(self, index):
        """first entry of commodity combo box is commodity,
        others are sub commodities"""
        if index > 1:
            com = self._model.current_commodity.sub_commodities[index - 1]
        else:
            com = self._model.current_graph_commodity

        self._model.current_graph_commodity = com

    def change_zoom_mode(self, zoom_type):
        self._model.graph_zoom_mode = zoom_type

    def set_current_commodity(self, commodity):
        self._model.current_commodity = commodity
